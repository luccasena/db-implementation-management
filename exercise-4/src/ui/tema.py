import streamlit as st

VERMELHO_F1 = "#E10600"
FUNDO = "#15151E"
SUPERFICIE = "#1F1F2B"
BORDA = "#2E2E3C"
TEXTO = "#F5F5F7"
TEXTO_SECUNDARIO = "#9A9AAE"

# Cores usadas pela F1 para classificar mini-setores (campo segments_sector_* da OpenF1).
CORES_SEGMENTOS = {
    0: ("#3A3A48", "Sem dado"),
    2048: ("#FFD12E", "Mais lento que a melhor pessoal"),
    2049: ("#00D26A", "Melhor pessoal"),
    2051: ("#B138DD", "Melhor geral"),
    2064: ("#2B8CFF", "Pit lane"),
}

# Usada quando o piloto não possui team_colour na OpenF1.
PALETA_RESERVA = ["#E10600", "#2B8CFF", "#00D26A", "#FFD12E", "#B138DD", "#FF8700", "#6CD3BF", "#F596C8"]

CSS = f"""
<style>
:root {{
    --of1-red: {VERMELHO_F1};
    --of1-bg: {FUNDO};
    --of1-surface: {SUPERFICIE};
    --of1-border: {BORDA};
    --of1-text: {TEXTO};
    --of1-muted: {TEXTO_SECUNDARIO};
}}

.block-container {{ padding-top: 2.5rem; max-width: 1400px; }}

[data-testid="stSidebar"] {{ border-right: 1px solid var(--of1-border); }}
[data-testid="stSidebar"] label p {{
    text-transform: uppercase; letter-spacing: .08em; font-size: .72rem;
    font-weight: 700; color: var(--of1-muted);
}}

.of1-brand {{
    display: flex; align-items: center; gap: .6rem; margin-bottom: 1.4rem;
    padding-bottom: 1rem; border-bottom: 1px solid var(--of1-border);
}}
.of1-brand__mark {{
    width: 34px; height: 22px; background: var(--of1-red);
    clip-path: polygon(22% 0, 100% 0, 78% 100%, 0 100%);
}}
.of1-brand__name {{ font-weight: 900; font-size: 1.25rem; letter-spacing: .02em; line-height: 1; }}
.of1-brand__name span {{ color: var(--of1-red); }}
.of1-brand__sub {{ color: var(--of1-muted); font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; }}

.of1-sidebar-footer {{ margin-top: 2rem; color: var(--of1-muted); font-size: .78rem; line-height: 1.5; }}
.of1-sidebar-footer a {{ color: var(--of1-text); }}

.of1-hero {{
    position: relative; overflow: hidden;
    padding: 1.6rem 1.8rem; margin-bottom: 1.2rem;
    background: linear-gradient(115deg, var(--of1-surface) 0%, var(--of1-surface) 62%, rgba(225, 6, 0, .18) 100%);
    border: 1px solid var(--of1-border); border-left: 6px solid var(--of1-red);
    border-radius: 6px;
}}
.of1-hero__eyebrow {{
    display: flex; flex-wrap: wrap; align-items: center; gap: .5rem;
    color: var(--of1-muted); text-transform: uppercase; letter-spacing: .12em;
    font-size: .75rem; font-weight: 700;
}}
.of1-hero__title {{
    margin: .35rem 0 .15rem; font-size: 2.6rem; font-weight: 900;
    line-height: 1.05; text-transform: uppercase; letter-spacing: -.01em;
}}
.of1-hero__subtitle {{ font-size: 1.1rem; color: var(--of1-muted); font-weight: 600; }}
.of1-hero__keys {{ margin-top: 1rem; display: flex; flex-wrap: wrap; gap: .4rem; }}

.of1-badge {{
    display: inline-block; padding: .15rem .55rem; border-radius: 3px;
    background: var(--of1-red); color: #fff; font-weight: 700; letter-spacing: .08em;
}}
.of1-key {{
    font-family: "JetBrains Mono", monospace; font-size: .75rem;
    padding: .15rem .5rem; border-radius: 3px;
    background: rgba(255, 255, 255, .05); border: 1px solid var(--of1-border); color: var(--of1-muted);
}}
.of1-key b {{ color: var(--of1-text); font-weight: 600; }}

.of1-stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: .75rem; margin-bottom: 1.6rem; }}
.of1-stat {{
    background: var(--of1-surface); border: 1px solid var(--of1-border);
    border-radius: 6px; padding: .8rem 1rem;
}}
.of1-stat__label {{ color: var(--of1-muted); font-size: .7rem; text-transform: uppercase; letter-spacing: .1em; font-weight: 700; }}
.of1-stat__value {{ font-size: 1.35rem; font-weight: 700; margin-top: .15rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}

.of1-section {{
    display: flex; align-items: baseline; gap: .75rem;
    margin: 1.8rem 0 .8rem; padding-bottom: .4rem; border-bottom: 1px solid var(--of1-border);
}}
.of1-section h3 {{ margin: 0; padding: 0; font-size: 1.15rem; font-weight: 900; text-transform: uppercase; letter-spacing: .06em; }}
.of1-section h3::before {{ content: ""; display: inline-block; width: 4px; height: .9em; background: var(--of1-red); margin-right: .55rem; vertical-align: -1px; }}
.of1-section span {{ color: var(--of1-muted); font-size: .85rem; }}

.of1-drivers {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: .75rem; }}
.of1-driver {{
    position: relative; display: flex; gap: .8rem; align-items: stretch;
    background: var(--of1-surface); border: 1px solid var(--of1-border);
    border-top: 4px solid var(--team); border-radius: 6px; padding: .8rem .9rem .8rem .8rem; overflow: hidden;
}}
.of1-driver__photo {{
    width: 64px; height: 64px; flex: none; border-radius: 4px; object-fit: cover; object-position: top;
    background: linear-gradient(180deg, var(--team) 0%, transparent 140%);
}}
.of1-driver__photo--empty {{ display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 1.2rem; }}
.of1-driver__info {{ min-width: 0; flex: 1; }}
.of1-driver__head {{ display: flex; align-items: baseline; gap: .4rem; }}
.of1-driver__acronym {{ font-weight: 900; font-size: 1.3rem; letter-spacing: .03em; }}
.of1-driver__number {{ color: var(--team); font-weight: 900; font-size: 1.05rem; }}
.of1-driver__name {{ font-size: .85rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.of1-driver__team {{ color: var(--of1-muted); font-size: .75rem; text-transform: uppercase; letter-spacing: .06em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.of1-driver__stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: .3rem; margin-top: .55rem; }}
.of1-driver__stats div {{ font-size: .65rem; color: var(--of1-muted); text-transform: uppercase; letter-spacing: .06em; }}
.of1-driver__stats b {{ display: block; font-family: "JetBrains Mono", monospace; font-size: .82rem; color: var(--of1-text); letter-spacing: 0; text-transform: none; }}
.of1-driver__stats b.of1-purple {{ color: #D17BF0; }}

.of1-segments {{ display: flex; flex-direction: column; gap: .45rem; }}
.of1-segrow {{ display: grid; grid-template-columns: 70px 1fr 1fr 1fr 96px; gap: .6rem; align-items: center; }}
.of1-segrow__driver {{ font-weight: 900; border-left: 4px solid var(--team); padding-left: .45rem; }}
.of1-segrow__sector {{ display: flex; gap: 3px; }}
.of1-segrow__sector i {{ flex: 1; height: 14px; border-radius: 2px; }}
.of1-segrow__time {{ font-family: "JetBrains Mono", monospace; font-size: .85rem; text-align: right; }}
.of1-segrow--head {{ color: var(--of1-muted); font-size: .7rem; text-transform: uppercase; letter-spacing: .1em; font-weight: 700; }}
.of1-legend {{ display: flex; flex-wrap: wrap; gap: 1rem; margin-top: .8rem; color: var(--of1-muted); font-size: .78rem; }}
.of1-legend i {{ display: inline-block; width: 12px; height: 12px; border-radius: 2px; margin-right: .35rem; vertical-align: -1px; }}

[data-testid="stExpander"] details {{ border-color: var(--of1-border); background: var(--of1-surface); }}
</style>
"""


def aplicar_tema() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
