import math
import re
from html import escape

import pandas as pd
import streamlit as st

from ui.tema import CORES_SEGMENTOS, PALETA_RESERVA

_HEX_VALIDO = re.compile(r"^[0-9A-Fa-f]{6}$")


def formatar_tempo_volta(segundos: float | None) -> str:
    if segundos is None or (isinstance(segundos, float) and math.isnan(segundos)):
        return "-"
    minutos, resto = divmod(segundos, 60)
    if minutos:
        return f"{int(minutos)}:{resto:06.3f}"
    return f"{resto:.3f}"


def formatar_data_local(sessao: dict) -> str:
    data_inicio = sessao.get("date_start")
    if not data_inicio:
        return "-"
    try:
        data = pd.to_datetime(data_inicio)
        offset = sessao.get("gmt_offset")
        if offset:
            data = data + pd.to_timedelta(offset)
            return data.strftime("%d/%m/%Y · %H:%M") + " local"
        return data.strftime("%d/%m/%Y · %H:%M UTC")
    except (ValueError, TypeError):
        return str(data_inicio)[:10]


def cor_equipe(piloto: dict, indice: int) -> str:
    cor = piloto.get("team_colour")
    if cor and _HEX_VALIDO.match(cor):
        return f"#{cor.upper()}"
    return PALETA_RESERVA[indice % len(PALETA_RESERVA)]


def _html(conteudo: str) -> None:
    st.markdown(conteudo, unsafe_allow_html=True)


def marca_sidebar() -> None:
    _html(
        '<div class="of1-brand"><div class="of1-brand__mark"></div><div>'
        '<div class="of1-brand__name">Open<span>F1</span></div>'
        '<div class="of1-brand__sub">Data Explorer</div>'
        "</div></div>"
    )


def rodape_sidebar() -> None:
    _html(
        '<div class="of1-sidebar-footer">'
        'Dados da <a href="https://openf1.org" target="_blank">OpenF1 API</a>, '
        "coletados para o MongoDB <code>openf1_data</code>.</div>"
    )


def cabecalho_sessao(sessao: dict) -> None:
    tipo = escape(str(sessao.get("session_type") or "Sessão"))
    ano = escape(str(sessao.get("year") or ""))
    pais = escape(str(sessao.get("country_name") or "-"))
    local = escape(str(sessao.get("location") or ""))
    nome = escape(str(sessao.get("session_name") or ""))
    chaves = "".join(
        f'<span class="of1-key">{rotulo}=<b>{escape(str(sessao[rotulo]))}</b></span>'
        for rotulo in ("session_key", "meeting_key", "circuit_key")
        if sessao.get(rotulo) is not None
    )
    _html(
        '<div class="of1-hero">'
        f'<div class="of1-hero__eyebrow"><span class="of1-badge">{tipo}</span>'
        f"<span>{ano} · {escape(formatar_data_local(sessao))}</span></div>"
        f'<div class="of1-hero__title">{pais}</div>'
        f'<div class="of1-hero__subtitle">{local} — {nome}</div>'
        f'<div class="of1-hero__keys">{chaves}</div>'
        "</div>"
    )


def indicadores(itens: list[tuple[str, str]]) -> None:
    blocos = "".join(
        f'<div class="of1-stat"><div class="of1-stat__label">{escape(rotulo)}</div>'
        f'<div class="of1-stat__value" title="{escape(valor)}">{escape(valor)}</div></div>'
        for rotulo, valor in itens
    )
    _html(f'<div class="of1-stats">{blocos}</div>')


def titulo_secao(titulo: str, subtitulo: str = "") -> None:
    _html(
        f'<div class="of1-section"><h3>{escape(titulo)}</h3>'
        f"<span>{escape(subtitulo)}</span></div>"
    )


def cartoes_pilotos(pilotos: list[dict]) -> None:
    """Cada piloto: dict com dados da OpenF1 + chaves 'cor', 'melhor_volta', 'media', 'velocidade_maxima', 'mais_rapido'."""
    cartoes = []
    for piloto in pilotos:
        acronimo = escape(piloto.get("name_acronym") or "")
        foto = piloto.get("headshot_url")
        if foto:
            imagem = f'<img class="of1-driver__photo" src="{escape(foto)}" alt="{acronimo}">'
        else:
            imagem = f'<div class="of1-driver__photo of1-driver__photo--empty">{acronimo}</div>'
        classe_melhor = ' class="of1-purple"' if piloto["mais_rapido"] else ""
        velocidade = piloto["velocidade_maxima"]
        cartoes.append(
            f'<div class="of1-driver" style="--team: {piloto["cor"]}">{imagem}'
            '<div class="of1-driver__info">'
            f'<div class="of1-driver__head"><span class="of1-driver__acronym">{acronimo}</span>'
            f'<span class="of1-driver__number">{piloto["driver_number"]}</span></div>'
            f'<div class="of1-driver__name">{escape(piloto.get("full_name") or "")}</div>'
            f'<div class="of1-driver__team">{escape(piloto.get("team_name") or "")}</div>'
            '<div class="of1-driver__stats">'
            f"<div>Melhor<b{classe_melhor}>{formatar_tempo_volta(piloto['melhor_volta'])}</b></div>"
            f"<div>Média<b>{formatar_tempo_volta(piloto['media'])}</b></div>"
            f"<div>Speed trap<b>{'-' if pd.isna(velocidade) else f'{velocidade:.0f} km/h'}</b></div>"
            "</div></div></div>"
        )
    _html(f'<div class="of1-drivers">{"".join(cartoes)}</div>')


def _barras_setor(segmentos) -> str:
    if not isinstance(segmentos, list) or not segmentos:
        return '<div class="of1-segrow__sector"><i style="background:#3A3A48"></i></div>'
    barras = "".join(
        f'<i style="background:{CORES_SEGMENTOS.get(valor or 0, CORES_SEGMENTOS[0])[0]}"></i>'
        for valor in segmentos
    )
    return f'<div class="of1-segrow__sector">{barras}</div>'


def mini_setores(linhas: list[dict]) -> None:
    """Cada linha: {'acronimo', 'cor', 'segmentos': [s1, s2, s3], 'tempo'}."""
    cabecalho = (
        '<div class="of1-segrow of1-segrow--head"><div>Piloto</div>'
        "<div>Setor 1</div><div>Setor 2</div><div>Setor 3</div>"
        '<div style="text-align:right">Tempo</div></div>'
    )
    corpo = "".join(
        f'<div class="of1-segrow"><div class="of1-segrow__driver" style="--team: {linha["cor"]}">'
        f'{escape(linha["acronimo"])}</div>'
        + "".join(_barras_setor(setor) for setor in linha["segmentos"])
        + f'<div class="of1-segrow__time">{formatar_tempo_volta(linha["tempo"])}</div></div>'
        for linha in linhas
    )
    legenda = "".join(
        f'<span><i style="background:{cor}"></i>{escape(rotulo)}</span>'
        for codigo, (cor, rotulo) in CORES_SEGMENTOS.items()
        if codigo
    )
    _html(
        f'<div class="of1-segments">{cabecalho}{corpo}</div>'
        f'<div class="of1-legend">{legenda}</div>'
    )
