# ============================================================
#  AquaSense — Dashboard |  app.py
# ============================================================

import dash
from dash import html, dcc, Input, Output
from dash_iconify import DashIconify
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from environmental_monitoring_page import make_environmental_monitoring_page

app = dash.Dash(
    __name__,
    title="AquaSense | Monitoramento Hídrico Colaborativo",
    update_title=None,
    suppress_callback_exceptions=True,
    use_pages=False,
)
server = app.server


# ── Helpers de ícone ─────────────────────────────────────────

def ico(icon_name, size=24, color="#3fffe7"):
    return DashIconify(icon=icon_name, width=size, height=size, color=color)


def icon_nav_logo():
    return html.Div(
        className="nav-logo-icon",
        children=[
            html.Img(
                src="/assets/aquasense-logo.png",
                style={"width": "80px", "height": "80px",
                       "display": "block", "objectFit": "contain"},
            )
        ],
    )

def icon_ml():        return ico("carbon:machine-learning")
def icon_leaf():      return ico("lucide:leaf")
def icon_chart():     return ico("lucide:bar-chart-2")
def icon_science():   return ico("lucide:flask-conical")
def icon_search():    return ico("lucide:search")
def icon_tag():       return ico("lucide:tag")
def icon_cpu():       return ico("lucide:cpu")
def icon_dashboard(): return ico("lucide:layout-dashboard")
def icon_globe():     return ico("lucide:globe")
def icon_database():  return ico("lucide:database")
def icon_calendar():  return ico("lucide:calendar")
def icon_map():       return ico("lucide:map-pin")
def icon_droplets():  return ico("lucide:droplets")
def icon_layers():    return ico("lucide:layers")
def icon_target():    return ico("lucide:target")
def icon_copy_check():return ico("lucide:copy-check")
def icon_alert():     return ico("lucide:alert-triangle")
def icon_activity():  return ico("lucide:activity")
def icon_flask():     return ico("lucide:flask-conical")
def icon_trending():  return ico("lucide:trending-up")
def icon_compass():   return ico("lucide:compass")
def icon_pandas():    return ico("simple-icons:pandas")
def icon_python():    return ico("simple-icons:python")
def icon_sklearn():   return ico("simple-icons:scikitlearn")
def icon_plotly():    return ico("simple-icons:plotly")
def icon_colab():     return ico("simple-icons:googlecolab")
def icon_rf():        return ico("lucide:trees")
def icon_lgbm():      return ico("lucide:zap")
def icon_svm():       return ico("lucide:git-merge")


def water_core_svg():
    import base64
    inner = (
        '<defs>'
        '<radialGradient id="cg" cx="50%" cy="40%" r="55%">'
        '<stop offset="0%" stop-color="%233fffe7" stop-opacity="0.9"/>'
        '<stop offset="100%" stop-color="%23004d48" stop-opacity="0.5"/>'
        '</radialGradient></defs>'
        '<path d="M12 2C12 2 5 9.5 5 14a7 7 0 0 0 14 0C19 9.5 12 2 12 2Z" '
        'stroke="url(%23cg)" stroke-width="1.4" fill="%233fffe7" fill-opacity="0.06"/>'
        '<path d="M9 15.5a3 3 0 0 0 4.5 1.5" stroke="%233fffe7" stroke-width="1.4" stroke-opacity="0.5"/>'
        '<circle cx="12" cy="13" r="2.5" fill="%233fffe7" fill-opacity="0.5" stroke="none"/>'
    )
    svg = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">' + inner + '</svg>'
    b64 = base64.b64encode(svg.encode()).decode()
    return html.Img(
        src=f"data:image/svg+xml;base64,{b64}",
        style={"width": "64px", "height": "64px"},
        className="water-core-img",
    )


# ============================================================
#  LANDING PAGE DATA
# ============================================================

FEATURES = [
    (icon_ml,      "Análise Exploratória",    "Pipeline completo de análise exploratória, engenharia de atributos e validação estatística para extrair padrões ambientais relevantes."),
    (icon_leaf,    "Machine Learning",        "Modelos supervisionados e clusterização para classificar a qualidade da água e descobrir padrões ambientais ocultos."),
    (icon_science, "Monitoramento Ambiental", "Acompanhamento contínuo de corpos hídricos com integração a dados da CONAMA, garantindo conformidade com as normas de preservação ambiental."),
]

OBJETIVOS = [
    ("01", "Monitoramento Hídrico Contínuo",   "Analisar parâmetros físico-químicos relacionados à qualidade da água, permitindo identificar padrões e variações ambientais relevantes."),
    ("02", "Classificação pela CONAMA",         "Rotular amostras de acordo com as classes de enquadramento definidas pela Resolução CONAMA 357/2005."),
    ("03", "Descoberta de Padrões Ambientais",  "Aplicar técnicas de EDA e machine learning para revelar correlações e tendências nos ecossistemas hídricos."),
    ("04", "Suporte à Tomada de Decisão",       "Explorar visualmente os dados ambientais através de dashboards interativos, facilitando a interpretação das análises realizadas ao longo do projeto."),
]

PIPELINE_STEPS = [
    ("1", icon_search,    "EDA",       "Análise exploratória e limpeza dos dados brutos"),
    ("2", icon_tag,       "Rótulo",    "Construção do target via CONAMA 357"),
    ("3", icon_cpu,       "ML",        "Treinamento e avaliação dos modelos preditivos"),
    ("4", icon_dashboard, "Dashboard", "Criação de visualizações interativas com Dash"),
    ("5", icon_globe,     "Ambiental", "Interpretação ecológica e geração de insights"),
]

TECHS = [
    (icon_python,  "Python"),
    (icon_pandas,  "Pandas"),
    (icon_sklearn, "Scikit-Learn"),
    (icon_plotly,  "Plotly Dash"),
    (icon_rf,      "Random Forest"),
    (icon_lgbm,    "LightGBM"),
    (icon_svm,     "SVM"),
    (icon_colab,   "Google Colab"),
]


# ============================================================
#  EDA DATA
# ============================================================

EDA_JOURNEY_STEPS = [
    ("1", "Entender o dataset",              "Contexto, origem e estrutura geral dos dados ambientais."),
    ("2", "Avaliar estrutura e qualidade",   "Colunas, tipos, nulos, duplicatas e consistência temporal."),
    ("3", "Explorar distribuições",          "Estatísticas descritivas e histogramas por variável."),
    ("4", "Identificar outliers",            "Detecção de valores extremos e assimetrias nas distribuições."),
    ("5", "Comparar países e corpos hídricos","Padrões regionais e variações por tipo de ecossistema."),
    ("6", "Analisar correlações",            "Relações entre parâmetros físico-químicos e qualidade."),
    ("7", "Relacionar com a CONAMA",         "Enquadramento nas classes ambientais da resolução 357/2005."),
    ("8", "Preparar base para ML",           "Engenharia de atributos e construção do dataset final."),
]

EDA_NAV_CARDS = [
    (icon_activity,  "Variáveis Ambientais",     "Distribuições, outliers e análise estatística.", "/eda/variables"),
    (icon_alert,     "Outliers e Assimetria",     "Detecção de valores extremos e assimetria estatística.", "/eda/outliers"),
    (icon_globe,     "Análise por País",          "Padrões regionais e diferenças geográficas.", "/eda/countries"),
    (icon_droplets,  "Análise por Corpo Hídrico", "Comparação entre ecossistemas aquáticos.", "/eda/water-bodies"),
    (icon_trending,  "Correlações",               "Relações entre parâmetros físico-químicos.", "/eda/correlations"),
    (icon_compass,   "CONAMA e Target",           "Enquadramento ambiental e construção do rótulo.", "/eda/conama-target"),
    (icon_cpu,       "Machine Learning",          "Modelagem supervisionada e clusterização não supervisionada.", "/machine-learning"),
]


# ============================================================
#  PLOTLY CHART THEME
# ============================================================

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#d8f5f1"),
    margin=dict(l=16, r=16, t=32, b=16),
    showlegend=False,
    xaxis=dict(
        gridcolor="rgba(63,255,231,0.08)",
        linecolor="rgba(63,255,231,0.15)",
        tickfont=dict(size=11, color="rgba(212,245,241,0.6)"),
        tickcolor="rgba(63,255,231,0.15)",
    ),
    yaxis=dict(
        gridcolor="rgba(63,255,231,0.08)",
        linecolor="rgba(63,255,231,0.15)",
        tickfont=dict(size=11, color="rgba(212,245,241,0.6)"),
        tickcolor="rgba(63,255,231,0.15)",
    ),
    hoverlabel=dict(
        bgcolor="rgba(0,77,72,0.92)",
        bordercolor="rgba(63,255,231,0.3)",
        font=dict(color="#f4fffe", size=12),
    ),
)

TEAL_PALETTE = ["#3fffe7", "#00e0ca", "#00c4ad", "#00a893", "#008c7a"]


def make_chart_records_by_country():
    countries = ["England", "USA", "Ireland", "China", "Canada"]
    values    = [2_129_198, 413_814, 235_019, 45_997, 3_949]
    fig = go.Figure(go.Bar(
        x=countries, y=values,
        marker=dict(color=TEAL_PALETTE, line=dict(color="rgba(63,255,231,0.3)", width=1)),
        hovertemplate="<b>%{x}</b><br>%{y:,.0f} registros<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT, title=dict(
        text="Registros por País",
        font=dict(family="Syne, sans-serif", size=13, color="#f4fffe"), x=0, pad=dict(l=0),
    ), height=260)
    return fig


def make_chart_water_bodies():
    categories = ["River", "Effluent", "Lake", "Estuarine", "Bay", "Sea Water", "Canal", "Sewage", "Marine", "Drainage"]
    values     = [1_852_579, 601_550, 153_603, 49_375, 45_997, 32_061, 28_574, 23_777, 23_162, 10_205]
    fig = go.Figure(go.Bar(
        x=values, y=categories, orientation="h",
        marker=dict(color=(TEAL_PALETTE[::-1] + ["#006960", "#00544d", "#004d48", "#003d39", "#002f2c"])[:len(categories)], line=dict(color="rgba(63,255,231,0.2)", width=1)),
        hovertemplate="<b>%{y}</b><br>%{x:,.0f} registros<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT, title=dict(
        text="Corpos Hídricos",
        font=dict(family="Syne, sans-serif", size=13, color="#f4fffe"), x=0, pad=dict(l=0),
    ), height=320)
    return fig


def make_chart_temporal():
    decades = ["1940s","1950s","1960s","1970s","1980s","1990s","2000s","2010s","2020s"]
    counts  = [12000, 28000, 65000, 145000, 280000, 490000, 670000, 890000, 247977]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=decades, y=counts,
        mode="lines+markers",
        line=dict(color="#3fffe7", width=2.5, shape="spline"),
        marker=dict(color="#3fffe7", size=7, line=dict(color="#011a18", width=2)),
        fill="tozeroy", fillcolor="rgba(63,255,231,0.07)",
        hovertemplate="<b>%{x}</b><br>%{y:,.0f} registros<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT, title=dict(
        text="Cobertura Temporal",
        font=dict(family="Syne, sans-serif", size=13, color="#f4fffe"), x=0, pad=dict(l=0),
    ), height=260)
    return fig


# ============================================================
#  HELPERS
# ============================================================

def nav_link(label, href, extra_cls=""):
    return html.Li(html.A(label, href=href, className=f"nav-link {extra_cls}".strip()))

def feature_card(icon_fn, title, text):
    target = None
    cta = None
    if title == "Análise Exploratória":
        target = "/eda"
        cta = "Explorar análise "
    elif title == "Machine Learning":
        target = "/machine-learning"
        cta = "Ver modelagem "
    elif title == "Monitoramento Ambiental":
        target = "/environmental-monitoring"
        cta = "Ver insights "

    card = html.Div(className="feature-card", style={"cursor": "pointer"} if target else {}, children=[
        html.Div(className="card-icon", children=[icon_fn()]),
        html.H3(title, className="card-title"),
        html.P(text, className="card-text"),
        html.Div(style={"marginTop": "20px", "display": "inline-flex", "alignItems": "center",
                        "gap": "8px", "fontSize": "13px", "fontWeight": "600",
                        "color": "var(--teal)", "letterSpacing": "0.3px"}, children=[
            cta,
            DashIconify(icon="lucide:arrow-right", width=14, height=14, color="#3fffe7"),
        ]) if target else None,
    ])
    if target:
        return html.A(href=target, style={"textDecoration": "none"}, children=[card])
    return card

def objetivo_item(num, title, desc):
    return html.Li(className="obj-item", children=[
        html.Span(num, className="obj-num"),
        html.Div(className="obj-content", children=[
            html.H4(title, className="obj-title"),
            html.P(desc,   className="obj-desc"),
        ]),
    ])

def pipeline_step(num, icon_fn, label, desc):
    return html.Div(className="pipeline-step", children=[
        html.Div(className="pipeline-step-inner", children=[
            html.Div(num, className="pipeline-num"),
            html.Div(className="pipeline-icon", children=[icon_fn()]),
            html.H4(label, className="pipeline-label"),
            html.P(desc,   className="pipeline-desc"),
        ]),
    ])

def tech_pill(icon_fn, name):
    return html.Div(className="tech-pill", children=[
        html.Div(className="tech-icon", children=[icon_fn()]),
        html.Span(name, className="tech-name"),
    ])


# ============================================================
#  NAVBARS
# ============================================================

def make_navbar(page="landing"):
    if page == "variables":
        nav_items = [
            nav_link("Visão Geral", "/eda"),
            nav_link("← Início",   "/",  "nav-cta"),
        ]
    elif page == "eda":
        nav_items = [
            nav_link("Visão Geral",   "/eda"),
            nav_link("← Início",      "/",  "nav-cta"),
        ]
    else:
        nav_items = [
            nav_link("Recursos",    "#features"),
            nav_link("Objetivos",   "#objetivos"),
            nav_link("Pipeline",    "#pipeline"),
            nav_link("Tecnologias", "#tecnologias"),
            nav_link("Dashboard",   "#hero", "nav-cta"),
        ]
    return html.Nav(id="navbar", children=[
        html.A(className="nav-logo", href="/", children=[
            icon_nav_logo(),
            html.Span("AquaSense", className="nav-logo-text"),
        ]),
        html.Ul(className="nav-links", children=nav_items),
    ])


# ============================================================
#  LANDING PAGE
# ============================================================

def make_hero():
    return html.Section(id="hero", children=[
        html.Div(className="hero-bg"),
        html.Div(className="hero-grid"),
        html.Div(className="orb orb-1"),
        html.Div(className="orb orb-2"),
        html.Div(className="orb orb-3"),
        html.Div(className="hero-content", children=[
            html.Div(className="hero-badge", children=[
                html.Span(className="hero-badge-dot"),
                "Ciência de Dados Aplicada à Qualidade da Água",
            ]),
            html.H1(className="hero-title", children=[
                html.Span("Monitoramento ", className="hero-title-white"),
                html.Br(),
                html.Span("Hídrico",       className="hero-title-teal"),
                html.Br(),
                html.Span("Colaborativo",  className="hero-title-white"),
            ]),
            html.P("AquaSense combina ciência de dados, machine learning e dashboards interativos para monitorar, classificar e interpretar a qualidade dos recursos hídricos com base nas normas CONAMA.", className="hero-sub"),
            html.Div(className="hero-btn-wrap", children=[
                html.A("Explorar Dashboard", href="#features", className="btn-primary"),
                html.A("Ver Pipeline",       href="#pipeline",  className="btn-secondary"),
            ]),
            html.Div(className="hero-stats", children=[
                html.Div(className="hero-stat-item", children=[html.Div("3+", className="hero-stat-value"), html.Div("Algoritmos ML", className="hero-stat-label")]),
                html.Div(className="hero-stat-item", children=[html.Div("CONAMA", className="hero-stat-value"), html.Div("Conformidade", className="hero-stat-label")]),
                html.Div(className="hero-stat-item", children=[html.Div("100%", className="hero-stat-value"), html.Div("Open Source", className="hero-stat-label")]),
                html.Div(className="hero-stat-item", children=[html.Div("Real-time", className="hero-stat-value"), html.Div("Monitoramento", className="hero-stat-label")]),
            ]),
        ]),
    ])


def make_features():
    return html.Section(id="features", children=[
        html.Div(className="section-header section-header-center", children=[
            html.Span("Funcionalidades", className="section-label"),
            html.H2("Estrutura Analítica do AquaSense", className="section-title"),
            html.P("Quatro pilares que formam o ecossistema AquaSense, unindo dados, modelos e visualizações.", className="section-sub"),
        ]),
        html.Div(className="cards-grid", children=[feature_card(fn, t, tx) for fn, t, tx in FEATURES]),
    ])


def make_objetivos():
    return html.Section(id="objetivos", children=[
        html.Div(className="objetivos-layout", children=[
            html.Div([
                html.Div(className="section-header", children=[
                    html.Span("Objetivos", className="section-label"),
                    html.H2("Objetivos da Análise Desenvolvida", className="section-title"),
                    html.P("Estrutura analítica desenvolvida para interpretar dados ambientais, identificar padrões e auxiliar na classificação da qualidade da água.", className="section-sub"),
                ]),
                html.Ul(className="objetivos-list", children=[objetivo_item(n, t, d) for n, t, d in OBJETIVOS]),
            ]),
            html.Div(className="objetivos-visual", children=[
                html.Div(className="water-ring"),
                html.Div(className="water-ring"),
                html.Div(className="water-ring"),
                html.Div(className="water-core", children=[water_core_svg()]),
            ]),
        ]),
    ])


def make_pipeline():
    return html.Section(id="pipeline", children=[
        html.Div(className="section-header section-header-center", children=[
            html.Span("Fluxo do Projeto", className="section-label"),
            html.H2("Pipeline de Análise", className="section-title"),
            html.P("Fluxo metodológico utilizado na análise dos dados ambientais", className="section-sub"),
        ]),
        html.Div(className="pipeline-track", children=[pipeline_step(n, fn, l, d) for n, fn, l, d in PIPELINE_STEPS]),
    ])


def make_tecnologias():
    return html.Section(id="tecnologias", children=[
        html.Div(className="section-header section-header-center", children=[
            html.Span("Stack", className="section-label"),
            html.H2("Tecnologias utilizadas", className="section-title"),
            html.P("Tecnologias utilizadas no desenvolvimento da análise", className="section-sub"),
        ]),
        html.Div(className="tech-grid", children=[tech_pill(fn, name) for fn, name in TECHS]),
    ])


def make_footer():
    return html.Footer(id="footer", children=[
        html.Div(className="footer-inner", children=[
            html.Div(className="footer-top", children=[
                html.Div(className="footer-brand", children=[
                    html.Div(className="footer-logo", children=[
                        icon_nav_logo(),
                        html.Span("AquaSense", className="footer-logo-text"),
                    ]),
                    html.P("Sistema de monitoramento hídrico colaborativo, plataforma desenvolvida para análise, classificação e interpretação de dados relacionados à qualidade da água.", className="footer-tagline"),
                ]),
                html.Div([
                    html.H5("Projeto", className="footer-col-title"),
                    html.Ul(className="footer-links", children=[
                        html.Li(html.A("Visão Geral", href="#hero")),
                        html.Li(html.A("Objetivos",   href="#objetivos")),
                        html.Li(html.A("Pipeline",    href="#pipeline")),
                        html.Li(html.A("Tecnologias", href="#tecnologias")),
                    ]),
                ]),
                html.Div([
                    html.H5("Referências", className="footer-col-title"),
                    html.Ul(className="footer-links", children=[
                        html.Li(html.A("CONAMA 357/2005", href="https://conama.mma.gov.br/?option=com_sisconama&task=arquivo.download&id=450", target="_blank")),
                        html.Li(html.A("ANA — Dados Abertos", href="https://dadosabertos.ana.gov.br/", target="_blank")),
                        html.Li(html.A("Water Quality Dataset", href="https://doi.org/10.6084/m9.figshare.27800394.v2", target="_blank")),
                    ]),
                ]),
            ]),
            html.Div(className="footer-bottom", children=[
                html.P(["© 2026 ", html.Span("AquaSense"), " · Monitoramento Hídrico Colaborativo"], className="footer-copy"),
                html.Div(className="footer-badges", children=[
                    html.Span("Open Source", className="footer-badge"),
                    html.Span("Python", className="footer-badge"),
                    html.Span("Plotly Dash", className="footer-badge"),
                ]),
            ]),
        ]),
    ])


def make_landing_page():
    return html.Div(id="root", children=[
        make_navbar(),
        make_hero(),
        make_features(),
        make_objetivos(),
        make_pipeline(),
        make_tecnologias(),
        make_footer(),
    ])


# ============================================================
#  EDA VISÃO GERAL
# ============================================================

def eda_metric_card(icon_fn, value, title, desc):
    return html.Div(className="eda-metric-card", children=[
        html.Div(className="eda-metric-icon", children=[icon_fn()]),
        html.Div(className="eda-metric-value", children=value),
        html.Div(className="eda-metric-title", children=title),
        html.Div(className="eda-metric-desc",  children=desc),
    ])

def eda_journey_step(num, title, desc):
    return html.Div(className="eda-journey-step", children=[
        html.Div(className="eda-journey-inner", children=[
            html.Div(className="eda-journey-num", children=num),
            html.H4(title, className="eda-journey-label"),
            html.P(desc,   className="eda-journey-desc"),
        ]),
    ])

def eda_nav_card(icon_fn, title, desc, href=None):
    is_active = href is not None
    badge_text = "Acessar →" if is_active else "Em breve"
    badge_cls = "eda-nav-card-badge eda-nav-card-badge-active" if is_active else "eda-nav-card-badge"
    card = html.Div(className=f"eda-nav-card {'eda-nav-card-active' if is_active else ''}", children=[
        html.Div(className="eda-nav-card-icon", children=[icon_fn()]),
        html.Div(className=badge_cls, children=badge_text),
        html.H4(title, className="eda-nav-card-title"),
        html.P(desc,   className="eda-nav-card-desc"),
        html.Div(className="eda-nav-card-arrow", children=[
            DashIconify(icon="lucide:arrow-right", width=16, height=16,
                        color="rgba(63,255,231,0.8)" if is_active else "rgba(63,255,231,0.4)"),
        ]),
    ])
    if is_active:
        return html.A(href=href, style={"textDecoration": "none"}, children=[card])
    return card


def make_eda_hero():
    return html.Section(className="eda-hero", children=[
        html.Div(className="hero-bg"),
        html.Div(className="hero-grid"),
        html.Div(className="orb orb-1"),
        html.Div(className="orb orb-2"),
        html.Div(className="eda-hero-content", children=[
            html.Div(className="hero-badge", style={"marginBottom": "24px"}, children=[
                html.Span(className="hero-badge-dot"),
                "EDA • AquaSense Intelligence",
            ]),
            html.H1(className="eda-hero-title", children=[
                html.Span("Visão Geral da ", className="hero-title-white"),
                html.Span("Análise",         className="hero-title-teal"),
                html.Span(" Exploratória",   className="hero-title-white"),
            ]),
            html.P("Uma leitura inicial dos dados que sustentam a inteligência ambiental do AquaSense.", className="eda-hero-sub"),
            html.P("O AquaSense utiliza dados físico-químicos de qualidade da água para compreender padrões ambientais, apoiar a construção de classificações e preparar a base para modelos de aprendizado de máquina. Esta área apresenta a exploração inicial do dataset e orienta a jornada analítica do projeto.", className="eda-hero-body"),
        ]),
    ])


def make_eda_metrics():
    return html.Section(className="eda-section", children=[
        html.Div(className="eda-section-header", children=[
            html.Span("Dataset", className="section-label"),
            html.H2("Métricas Principais", className="section-title"),
            html.P("Indicadores quantitativos que definem a escala e estrutura do dataset.", className="section-sub"),
        ]),
        html.Div(className="eda-metrics-grid", children=[
            eda_metric_card(fn, v, t, d)
            for fn, v, t, d in [
                (icon_database,    "2.827.977",   "Registros ambientais",     "Volume total de observações disponíveis para exploração."),
                (icon_layers,      "14",           "Colunas no dataset",       "Variáveis físico-químicas e contextuais disponíveis."),
                (icon_calendar,    "1940 – 2023",  "Cobertura temporal",       "Mais de 8 décadas de dados ambientais contínuos."),
                (icon_map,         "5",            "Países presentes",         "Inglaterra, Irlanda, Canadá, China e Estados Unidos."),
                (icon_droplets,    "Múltiplas",    "Tipos de corpos hídricos", "Rios, lagos, reservatórios e outras categorias ambientais."),
                (icon_target,      "CCME_Values",  "Variável de qualidade",    "Indicador de qualidade hídrica base para análise."),
                (icon_copy_check,  "0",            "Dados nulos",              "Base de dados completa, sem ausências nas variáveis."),
                (icon_alert,       "9.971",        "Duplicatas identificadas", "Registros duplicados mapeados para tratamento."),
            ]
        ]),
    ])


def make_eda_what_is():
    return html.Section(className="eda-section eda-section-alt", children=[
        html.Div(className="eda-what-layout", children=[
            html.Div(className="eda-what-text", children=[
                html.Span("Contexto", className="section-label"),
                html.H2("O que esses dados representam?", className="section-title"),
                html.P("O dataset reúne medições físico-químicas coletadas em corpos hídricos de cinco países, associadas à avaliação da qualidade da água. Os registros abrangem parâmetros essenciais como pH, temperatura e oxigênio dissolvido, além de nutrientes e compostos relacionados à poluição orgânica e inorgânica.", className="eda-what-p"),
                html.P("Essa diversidade de variáveis permite investigar tanto a saúde biológica dos ecossistemas quanto os impactos de atividades humanas sobre os recursos hídricos. O indicador CCME_Values oferece uma métrica de síntese que conecta os parâmetros individuais a uma avaliação integrada de qualidade.", className="eda-what-p"),
            ]),
            html.Div(className="eda-what-card", children=[
                html.Div(className="eda-var-group", children=[
                    html.Div(className="eda-var-group-label", children="Identificação e contexto"),
                    html.Div(className="eda-var-pills", children=[html.Span("Country", className="eda-var-pill"), html.Span("Waterbody_Type", className="eda-var-pill"), html.Span("Date", className="eda-var-pill")]),
                ]),
                html.Div(className="eda-var-group", children=[
                    html.Div(className="eda-var-group-label", children="Parâmetros físico-químicos"),
                    html.Div(className="eda-var-pills", children=[html.Span(p, className="eda-var-pill") for p in ["pH", "Temperature", "Dissolved O₂", "BOD", "Ammonia", "Nitrogen", "Nitrate", "Orthophosphate"]]),
                ]),
                html.Div(className="eda-var-group", children=[
                    html.Div(className="eda-var-group-label", children="Indicador de qualidade"),
                    html.Div(className="eda-var-pills", children=[html.Span("CCME_Values", className="eda-var-pill eda-var-pill-highlight")]),
                ]),
            ]),
        ]),
    ])


def make_eda_journey():
    return html.Section(className="eda-section", children=[
        html.Div(className="eda-section-header", children=[
            html.Span("Jornada Analítica", className="section-label"),
            html.H2("Estrutura da Exploração", className="section-title"),
            html.P("Etapas sequenciais que guiam a análise dos dados do AquaSense.", className="section-sub"),
        ]),
        html.Div(className="eda-journey-track", children=[eda_journey_step(n, t, d) for n, t, d in EDA_JOURNEY_STEPS]),
    ])


def make_eda_charts():
    return html.Section(className="eda-section eda-section-alt", children=[
        html.Div(className="eda-section-header", children=[
            html.Span("Prévia Visual", className="section-label"),
            html.H2("Primeiras Impressões do Dataset", className="section-title"),
            html.P("Visualizações iniciais para orientar a leitura dos dados.", className="section-sub"),
        ]),
        html.Div(className="eda-charts-grid", children=[
            html.Div(className="eda-chart-card", children=[dcc.Graph(figure=make_chart_records_by_country(), config={"displayModeBar": False}, style={"width": "100%"})]),
            html.Div(className="eda-chart-card", children=[dcc.Graph(figure=make_chart_water_bodies(), config={"displayModeBar": False}, style={"width": "100%"})]),
            html.Div(className="eda-chart-card eda-chart-wide", children=[dcc.Graph(figure=make_chart_temporal(), config={"displayModeBar": False}, style={"width": "100%"})]),
        ]),
    ])


def make_eda_insight():
    return html.Section(className="eda-section", children=[
        html.Div(className="eda-insight-card", children=[
            html.Div(className="eda-insight-header", children=[
                html.Div(className="eda-insight-icon", children=[DashIconify(icon="lucide:lightbulb", width=22, height=22, color="#3fffe7")]),
                html.H3("Primeira leitura dos dados", className="eda-insight-title"),
            ]),
            html.P("O dataset apresenta alto volume de registros, ampla cobertura temporal e variáveis físico-químicas relevantes para análise da qualidade da água. A presença do indicador CCME_Values permite investigar padrões de qualidade e criar uma ponte entre análise exploratória, critérios ambientais e modelos preditivos. A próxima etapa da exploração aprofunda a estrutura interna dos dados, avaliando colunas, tipos, duplicatas, consistência temporal e variáveis disponíveis.", className="eda-insight-body"),
            html.Div(className="eda-insight-tags", children=[
                html.Span("2.8M+ registros",   className="eda-insight-tag"),
                html.Span("8 décadas",          className="eda-insight-tag"),
                html.Span("5 países",           className="eda-insight-tag"),
                html.Span("CCME_Values",        className="eda-insight-tag eda-insight-tag-teal"),
                html.Span("Zero nulos",         className="eda-insight-tag"),
            ]),
        ]),
    ])


def make_eda_nav():
    return html.Section(className="eda-section eda-section-nav", children=[
        html.Div(className="eda-section-header", children=[
            html.Span("Próximas Etapas", className="section-label"),
            html.H2("Continuar a Exploração", className="section-title"),
            html.P("Acesse as próximas seções da análise exploratória do AquaSense.", className="section-sub"),
        ]),
        html.Div(className="eda-nav-grid", children=[
            eda_nav_card(fn, t, d, href)
            for fn, t, d, href in EDA_NAV_CARDS
        ]),
    ])


def make_eda_page():
    return html.Div(id="root", className="eda-root", children=[
        make_navbar(page="eda"),
        make_eda_hero(),
        make_eda_metrics(),
        make_eda_what_is(),
        make_eda_journey(),
        make_eda_charts(),
        make_eda_insight(),
        make_eda_nav(),
        make_footer(),
    ])




from variables_page import (
    make_variables_page, register_callbacks,
    VARIABLES, build_histogram, build_boxplot_violin, build_comparison_chart,
    stat_card, interpret_skew, interpret_kurt, interpret_cv
)
from outliers_page import (
    make_outliers_hero, make_outlier_metrics, make_outlier_heatmap_section,
    make_outlier_ranking_section, make_outlier_interactive_section,
    make_outlier_context_sections, register_outlier_callbacks
)

from country_page import (
    make_country_hero, make_country_metrics, make_country_distribution_section,
    make_country_temporal_section, make_country_quality_notes, make_country_insight
)

from waterbody_page import (
    make_waterbody_hero, make_waterbody_metrics, make_waterbody_distribution_section,
    make_waterbody_quality_section, make_waterbody_pollution_section, make_waterbody_context_sections
)

from correlations_page import (
    make_correlations_hero, make_correlations_metrics, make_correlation_matrix_section,
    make_relevant_pairs_section, make_scatter_interpretation_section, make_correlation_context_sections, register_correlation_callbacks
)

from conama_page import (
    make_conama_hero, make_conama_metrics, make_conama_story_section,
    make_conama_pipeline_section, make_conama_parameters_section,
    make_conama_threshold_table_section, make_conama_ifelse_ml_section,
    make_conama_distribution_section, make_conama_excluded_section,
    make_conama_ml_impact_section, make_conama_final_note
)

from ml_page import (
    make_ml_hero, make_ml_metrics, make_ml_story,
    make_supervised_section, make_clustering_section,
    make_ml_final_note, register_ml_callbacks
)

register_callbacks(app)
register_outlier_callbacks(app)
register_correlation_callbacks(app)
register_ml_callbacks(app)


def make_variables_page_full():
    from variables_page import make_variables_hero, make_filter_bar, make_stats_row, make_viz_area, make_interpretation_block
    return html.Div(id="root", className="var-root", children=[
        make_navbar(page="variables"),
        make_variables_hero(),
        make_filter_bar(),
        make_stats_row(),
        make_viz_area(),
        make_interpretation_block(),
        make_footer(),
    ])


def make_outliers_page_full():
    return html.Div(id="root", className="var-root outlier-root", children=[
        make_navbar(page="outliers"),
        make_outliers_hero(),
        make_outlier_metrics(),
        make_outlier_heatmap_section(),
        make_outlier_ranking_section(),
        make_outlier_interactive_section(),
        make_outlier_context_sections(),
        make_footer(),
    ])


def make_country_page_full():
    return html.Div(id="root", className="var-root country-root", children=[
        make_navbar(page="country"),
        make_country_hero(),
        make_country_metrics(),
        make_country_distribution_section(),
        make_country_temporal_section(),
        make_country_quality_notes(),
        make_country_insight(),
        make_footer(),
    ])


def make_waterbody_page_full():
    return html.Div(id="root", className="var-root waterbody-root", children=[
        make_navbar(page="waterbody"),
        make_waterbody_hero(),
        make_waterbody_metrics(),
        make_waterbody_distribution_section(),
        make_waterbody_quality_section(),
        make_waterbody_pollution_section(),
        make_waterbody_context_sections(),
        make_footer(),
    ])



def make_conama_page_full():
    return html.Div(id="root", className="var-root conama-root", children=[
        make_navbar(page="conama"),
        make_conama_hero(),
        make_conama_metrics(),
        make_conama_story_section(),
        make_conama_pipeline_section(),
        make_conama_parameters_section(),
        make_conama_threshold_table_section(),
        make_conama_ifelse_ml_section(),
        make_conama_distribution_section(),
        make_conama_excluded_section(),
        make_conama_ml_impact_section(),
        make_conama_final_note(),
        make_footer(),
    ])

def make_correlations_page_full():
    return html.Div(id="root", className="var-root correlations-root", children=[
        make_navbar(page="correlations"),
        make_correlations_hero(),
        make_correlations_metrics(),
        make_correlation_matrix_section(),
        make_relevant_pairs_section(),
        make_scatter_interpretation_section(),
        make_correlation_context_sections(),
        make_footer(),
    ])


def make_ml_page_full():
    return html.Div(id="root", className="var-root ml-root", children=[
        make_navbar(page="ml"),
        make_ml_hero(),
        make_ml_metrics(),
        make_ml_story(),
        make_supervised_section(),
        make_clustering_section(),
        make_ml_final_note(),
        make_footer(),
    ])


# ============================================================
#  ROUTING
# ============================================================

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content"),
])


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def render_page(pathname):
    if pathname == "/eda/variables":
        return make_variables_page_full()
    if pathname == "/eda/outliers":
        return make_outliers_page_full()
    if pathname == "/eda/countries":
        return make_country_page_full()
    if pathname == "/eda/water-bodies":
        return make_waterbody_page_full()
    if pathname == "/eda/correlations":
        return make_correlations_page_full()
    if pathname == "/eda/conama-target":
        return make_conama_page_full()
    if pathname == "/machine-learning":
        return make_ml_page_full()
    if pathname == "/eda":
        return make_eda_page()
    elif pathname == "/environmental-monitoring":
        return make_environmental_monitoring_page()
    
    return make_landing_page()


if __name__ == "__main__":
    app.run(debug=True, port=8050)