import altair as alt
import pandas as pd

from ui.tema import BORDA, TEXTO, TEXTO_SECUNDARIO

# Eixo Y em m:ss.s, como nas transmissões da F1.
_ROTULO_TEMPO = (
    "floor(datum.value / 60) + ':' + "
    "(datum.value % 60 < 10 ? '0' : '') + format(datum.value % 60, '.1f')"
)


def grafico_tempo_volta(df_voltas: pd.DataFrame, cores: dict[str, str]) -> alt.Chart:
    """df_voltas precisa das colunas: piloto, equipe, tracejado, lap_number, lap_duration, tempo_formatado."""
    pilotos = list(cores.keys())
    cor = alt.Color(
        "piloto:N",
        scale=alt.Scale(domain=pilotos, range=[cores[p] for p in pilotos]),
        legend=alt.Legend(title=None, orient="top", direction="horizontal"),
    )
    x = alt.X("lap_number:Q", title="Volta", axis=alt.Axis(tickMinStep=1, format="d"))
    y = alt.Y(
        "lap_duration:Q",
        title="Tempo de volta",
        scale=alt.Scale(zero=False, nice=True),
        axis=alt.Axis(labelExpr=_ROTULO_TEMPO),
    )

    hover = alt.selection_point(
        on="pointerover", nearest=True, fields=["lap_number"], empty=False, clear="pointerout"
    )

    linhas = (
        alt.Chart(df_voltas)
        .mark_line(strokeWidth=2.2)
        .encode(
            x=x,
            y=y,
            color=cor,
            strokeDash=alt.StrokeDash(
                "tracejado:N",
                scale=alt.Scale(domain=[False, True], range=[[1, 0], [6, 3]]),
                legend=None,
            ),
            detail="piloto:N",
        )
    )

    pontos = (
        alt.Chart(df_voltas)
        .mark_circle(size=70, stroke="#15151E", strokeWidth=1.5)
        .encode(
            x=x,
            y=y,
            color=cor,
            opacity=alt.condition(hover, alt.value(1), alt.value(0)),
            tooltip=[
                alt.Tooltip("piloto:N", title="Piloto"),
                alt.Tooltip("equipe:N", title="Equipe"),
                alt.Tooltip("lap_number:Q", title="Volta"),
                alt.Tooltip("tempo_formatado:N", title="Tempo"),
                alt.Tooltip("duration_sector_1:Q", title="S1 (s)", format=".3f"),
                alt.Tooltip("duration_sector_2:Q", title="S2 (s)", format=".3f"),
                alt.Tooltip("duration_sector_3:Q", title="S3 (s)", format=".3f"),
                alt.Tooltip("st_speed:Q", title="Speed trap (km/h)"),
            ],
        )
        .add_params(hover)
    )

    regua = (
        alt.Chart(df_voltas)
        .mark_rule(color=TEXTO_SECUNDARIO, strokeDash=[2, 3])
        .encode(x=x)
        .transform_filter(hover)
    )

    return (
        alt.layer(linhas, regua, pontos)
        .properties(height=440, background="transparent")
        .configure_view(stroke=None)
        .configure_axis(
            labelColor=TEXTO_SECUNDARIO,
            titleColor=TEXTO_SECUNDARIO,
            gridColor=BORDA,
            domainColor=BORDA,
            tickColor=BORDA,
            labelFont="Titillium Web",
            titleFont="Titillium Web",
            labelFontSize=12,
            titleFontSize=12,
            titleFontWeight=700,
        )
        .configure_legend(
            labelColor=TEXTO,
            labelFont="Titillium Web",
            labelFontSize=13,
            labelFontWeight=700,
            symbolStrokeWidth=4,
            symbolType="stroke",
        )
    )
