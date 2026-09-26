import streamlit as st
import pandas as pd
from services.openf1_data_service import OpenF1DataService
from ui.tema import aplicar_tema
from ui.componentes import (
    cabecalho_sessao,
    cartoes_pilotos,
    cor_equipe,
    formatar_tempo_volta,
    indicadores,
    marca_sidebar,
    mini_setores,
    rodape_sidebar,
    titulo_secao,
)
from ui.grafico import grafico_tempo_volta

st.set_page_config(page_title="OpenF1 Data Explorer", page_icon="🏎️", layout="wide")
aplicar_tema()

@st.cache_resource
def obter_servico() -> OpenF1DataService:
    return OpenF1DataService()

servico = obter_servico()

with st.sidebar:
    marca_sidebar()

    anos_disponiveis = servico.listar_anos_disponiveis()
    if not anos_disponiveis:
        st.warning(
            "Nenhuma sessão encontrada no banco `openf1_data`. "
            "Execute o coletor de dados antes de usar o explorer."
        )
        st.stop()

    ano_selecionado = st.selectbox("Temporada", anos_disponiveis)

    sessoes = servico.listar_sessoes_por_ano(ano_selecionado)
    if not sessoes:
        st.warning("Nenhuma sessão encontrada para o ano selecionado.")
        st.stop()

    opcoes_sessao = {
        f"{sessao.get('country_name', '')} · {sessao.get('location', '')} — {sessao.get('session_name', 'Sessão')}": sessao["session_key"]
        for sessao in sessoes
    }
    nome_sessao_selecionada = st.selectbox("Sessão", opcoes_sessao.keys())
    session_key = opcoes_sessao[nome_sessao_selecionada]

    rodape_sidebar()

sessao = servico.obter_detalhes_sessao(session_key)
pilotos = servico.listar_pilotos_por_sessao(session_key)

cabecalho_sessao(sessao)
indicadores([
    ("Circuito", sessao.get("circuit_short_name") or "-"),
    ("Local", sessao.get("location") or "-"),
    ("País", f"{sessao.get('country_name', '-')} ({sessao.get('country_code', '-')})"),
    ("Pilotos", str(len(pilotos))),
    ("Voltas registradas", str(servico.contar_voltas_por_sessao(session_key))),
])

if not pilotos:
    st.info("Nenhum piloto encontrado para esta sessão.")
    st.stop()

pilotos_por_numero = {piloto["driver_number"]: piloto for piloto in pilotos}
cores_por_numero = {
    piloto["driver_number"]: cor_equipe(piloto, indice) for indice, piloto in enumerate(pilotos)
}

def rotulo_piloto(numero: int) -> str:
    piloto = pilotos_por_numero[numero]
    return piloto.get("name_acronym") or f"#{numero}"

titulo_secao("Pilotos", "Cores de equipe conforme o campo team_colour da OpenF1")
numeros_pilotos_selecionados = st.multiselect(
    "Selecione os pilotos para comparar",
    list(pilotos_por_numero.keys()),
    default=list(pilotos_por_numero.keys())[:2],
    format_func=lambda numero: (
        f"{rotulo_piloto(numero)} · {pilotos_por_numero[numero].get('full_name', '')} "
        f"(#{numero}, {pilotos_por_numero[numero].get('team_name', '')})"
    ),
    label_visibility="collapsed",
    placeholder="Selecione os pilotos para comparar",
)

if not numeros_pilotos_selecionados:
    st.info("Selecione ao menos um piloto para visualizar o desempenho.")
    st.stop()

voltas = servico.obter_voltas_por_sessao_e_pilotos(session_key, numeros_pilotos_selecionados)
if not voltas:
    st.info("Nenhum dado de volta encontrado para os pilotos selecionados.")
    st.stop()

df_voltas = pd.DataFrame(voltas).drop(columns="_id", errors="ignore")
for coluna in ("duration_sector_1", "duration_sector_2", "duration_sector_3", "st_speed", "lap_duration"):
    if coluna not in df_voltas:
        df_voltas[coluna] = None
    df_voltas[coluna] = pd.to_numeric(df_voltas[coluna], errors="coerce")
if "is_pit_out_lap" not in df_voltas:
    df_voltas["is_pit_out_lap"] = False
df_voltas["is_pit_out_lap"] = df_voltas["is_pit_out_lap"].fillna(False).astype(bool)

df_voltas["piloto"] = df_voltas["driver_number"].map(rotulo_piloto)
df_voltas["equipe"] = df_voltas["driver_number"].map(
    lambda numero: pilotos_por_numero[numero].get("team_name") or "-"
)
# Companheiros de equipe compartilham a mesma cor: o segundo piloto recebe linha tracejada.
primeiro_por_equipe = {}
for numero in numeros_pilotos_selecionados:
    primeiro_por_equipe.setdefault(pilotos_por_numero[numero].get("team_name"), numero)
df_voltas["tracejado"] = df_voltas["driver_number"].map(
    lambda numero: primeiro_por_equipe[pilotos_por_numero[numero].get("team_name")] != numero
)
df_voltas["tempo_formatado"] = df_voltas["lap_duration"].map(formatar_tempo_volta)

melhor_volta_geral = df_voltas["lap_duration"].min()
cartoes = []
for numero in numeros_pilotos_selecionados:
    voltas_piloto = df_voltas[df_voltas["driver_number"] == numero]
    voltas_validas = voltas_piloto[~voltas_piloto["is_pit_out_lap"]]["lap_duration"].dropna()
    melhor = voltas_piloto["lap_duration"].min()
    cartoes.append({
        **pilotos_por_numero[numero],
        "cor": cores_por_numero[numero],
        "melhor_volta": melhor,
        "media": voltas_validas.median() if not voltas_validas.empty else None,
        "velocidade_maxima": voltas_piloto["st_speed"].max(),
        "mais_rapido": pd.notna(melhor) and melhor == melhor_volta_geral,
    })
cartoes_pilotos(cartoes)
st.caption("Melhor volta geral em roxo · Média = mediana das voltas, excluindo voltas de saída dos boxes.")

titulo_secao("Desempenho por volta", "lap_duration × lap_number")
coluna_pit, coluna_107, _ = st.columns([1.3, 1, 1.7])
ocultar_pit_out = coluna_pit.toggle("Ocultar voltas de saída dos boxes", value=False)
aplicar_107 = coluna_107.toggle(
    "Regra dos 107%",
    value=False,
    help="Oculta voltas mais lentas que 107% da melhor volta entre os pilotos selecionados.",
)

df_grafico = df_voltas.dropna(subset=["lap_duration"])
if ocultar_pit_out:
    df_grafico = df_grafico[~df_grafico["is_pit_out_lap"]]
if aplicar_107 and pd.notna(melhor_volta_geral):
    df_grafico = df_grafico[df_grafico["lap_duration"] <= melhor_volta_geral * 1.07]

if df_grafico.empty:
    st.info("Nenhuma volta restante com os filtros aplicados.")
else:
    cores_grafico = {rotulo_piloto(numero): cores_por_numero[numero] for numero in numeros_pilotos_selecionados}
    st.altair_chart(grafico_tempo_volta(df_grafico, cores_grafico), theme=None, width="stretch")

titulo_secao("Mini-setores", "segments_sector_1 · segments_sector_2 · segments_sector_3")
voltas_disponiveis = sorted(df_voltas["lap_number"].dropna().astype(int).unique())
volta_mais_rapida = df_voltas.loc[df_voltas["lap_duration"].idxmin(), "lap_number"] if pd.notna(melhor_volta_geral) else voltas_disponiveis[0]
volta_selecionada = (
    st.select_slider("Volta", options=voltas_disponiveis, value=int(volta_mais_rapida))
    if len(voltas_disponiveis) > 1
    else voltas_disponiveis[0]
)
linhas_setores = []
for numero in numeros_pilotos_selecionados:
    registro = df_voltas[(df_voltas["driver_number"] == numero) & (df_voltas["lap_number"] == volta_selecionada)]
    if registro.empty:
        continue
    volta = registro.iloc[0]
    linhas_setores.append({
        "acronimo": rotulo_piloto(numero),
        "cor": cores_por_numero[numero],
        "segmentos": [volta.get(f"segments_sector_{indice}") for indice in (1, 2, 3)],
        "tempo": volta["lap_duration"],
    })
if linhas_setores:
    mini_setores(linhas_setores)
else:
    st.info("Nenhum piloto selecionado registrou esta volta.")

with st.expander("Ver tabela de dados"):
    st.dataframe(
        df_voltas[[
            "piloto", "equipe", "lap_number", "lap_duration",
            "duration_sector_1", "duration_sector_2", "duration_sector_3",
            "st_speed", "is_pit_out_lap",
        ]].sort_values(["piloto", "lap_number"]),
        width="stretch",
        hide_index=True,
        column_config={
            "piloto": "Piloto",
            "equipe": "Equipe",
            "lap_number": st.column_config.NumberColumn("Volta", format="%d"),
            "lap_duration": st.column_config.NumberColumn("Tempo (s)", format="%.3f"),
            "duration_sector_1": st.column_config.NumberColumn("S1 (s)", format="%.3f"),
            "duration_sector_2": st.column_config.NumberColumn("S2 (s)", format="%.3f"),
            "duration_sector_3": st.column_config.NumberColumn("S3 (s)", format="%.3f"),
            "st_speed": st.column_config.NumberColumn("Speed trap (km/h)", format="%d"),
            "is_pit_out_lap": st.column_config.CheckboxColumn("Saída dos boxes"),
        },
    )
