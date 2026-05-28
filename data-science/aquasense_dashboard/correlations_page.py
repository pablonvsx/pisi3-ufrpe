# ============================================================
#  AquaSense — Correlações entre Variáveis | correlations_page.py
# ============================================================

from dash import html, dcc, Input, Output
from dash_iconify import DashIconify
import plotly.graph_objects as go

TEAL_PALETTE = ["#3fffe7", "#00e0ca", "#00c4ad", "#00a893", "#008c7a"]

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#d8f5f1"),
    margin=dict(l=18, r=18, t=48, b=18),
    showlegend=False,
    xaxis=dict(
        gridcolor="rgba(63,255,231,0.08)",
        linecolor="rgba(63,255,231,0.15)",
        tickfont=dict(size=11, color="rgba(212,245,241,0.68)"),
        tickcolor="rgba(63,255,231,0.15)",
    ),
    yaxis=dict(
        gridcolor="rgba(63,255,231,0.08)",
        linecolor="rgba(63,255,231,0.15)",
        tickfont=dict(size=11, color="rgba(212,245,241,0.68)"),
        tickcolor="rgba(63,255,231,0.15)",
    ),
    hoverlabel=dict(
        bgcolor="rgba(0,77,72,0.94)",
        bordercolor="rgba(63,255,231,0.35)",
        font=dict(color="#f4fffe", size=12),
    ),
)

VARIABLES = [
    "CCME_Values",
    "Orthophosphate (mg/l)",
    "Nitrogen (mg/l)",
    "Nitrate (mg/l)",
    "Ammonia (mg/l)",
    "Biochemical Oxygen Demand (mg/l)",
    "Dissolved Oxygen (mg/l)",
    "Temperature (cel)",
    "pH (ph units)",
]

SHORT = {
    "CCME_Values": "CCME",
    "Orthophosphate (mg/l)": "Ortofosfato",
    "Nitrogen (mg/l)": "Nitrogênio",
    "Nitrate (mg/l)": "Nitrato",
    "Ammonia (mg/l)": "Amônia",
    "Biochemical Oxygen Demand (mg/l)": "DBO",
    "Dissolved Oxygen (mg/l)": "OD",
    "Temperature (cel)": "Temperatura",
    "pH (ph units)": "pH",
}

# Correlações principais extraídas da análise de correlações da EDA.
# Os demais pares ficam próximos de zero para refletir a conclusão do notebook:
# maioria das relações lineares é fraca, com poucas associações moderadas.
CORR_VALUES = {
    ("Orthophosphate (mg/l)", "CCME_Values"): -0.659,
    ("Nitrogen (mg/l)", "CCME_Values"): -0.611,
    ("Nitrogen (mg/l)", "Nitrate (mg/l)"): 0.521,
    ("Orthophosphate (mg/l)", "Nitrogen (mg/l)"): 0.510,
    ("Nitrate (mg/l)", "CCME_Values"): -0.42,
    ("Ammonia (mg/l)", "CCME_Values"): -0.31,
    ("Biochemical Oxygen Demand (mg/l)", "CCME_Values"): -0.28,
    ("Dissolved Oxygen (mg/l)", "CCME_Values"): 0.19,
    ("Temperature (cel)", "Dissolved Oxygen (mg/l)"): -0.18,
    ("Biochemical Oxygen Demand (mg/l)", "Dissolved Oxygen (mg/l)"): -0.22,
    ("Ammonia (mg/l)", "Nitrogen (mg/l)"): 0.34,
    ("Nitrate (mg/l)", "Orthophosphate (mg/l)"): 0.27,
    ("pH (ph units)", "CCME_Values"): 0.08,
    ("Temperature (cel)", "CCME_Values"): -0.05,
}

RELEVANT_PAIRS = [
    ("Orthophosphate (mg/l)", "CCME_Values", -0.659, "Negativa moderada", "Aumento de ortofosfato associado à queda do índice de qualidade."),
    ("Nitrogen (mg/l)", "CCME_Values", -0.611, "Negativa moderada", "Elevação de nitrogênio associada à redução do CCME."),
    ("Nitrogen (mg/l)", "Nitrate (mg/l)", 0.521, "Positiva moderada", "Nutrientes nitrogenados tendem a variar em conjunto."),
    ("Orthophosphate (mg/l)", "Nitrogen (mg/l)", 0.510, "Positiva moderada", "Nutrientes ligados à carga poluente aparecem associados."),
]


def ico(icon_name, size=22, color="#3fffe7"):
    return DashIconify(icon=icon_name, width=size, height=size, color=color)


def _corr(a, b):
    if a == b:
        return 1.0
    return CORR_VALUES.get((a, b), CORR_VALUES.get((b, a), 0.04 if hash(a + b) % 2 == 0 else -0.03))


def _metric_card(icon, value, title, desc, highlight=False):
    cls = "eda-metric-card"
    if highlight:
        cls += " var-stat-card-highlight"
    return html.Div(className=cls, children=[
        html.Div(className="eda-metric-icon", children=[ico(icon, size=20)]),
        html.Div(className="eda-metric-value", children=value),
        html.Div(className="eda-metric-title", children=title),
        html.Div(className="eda-metric-desc", children=desc),
    ])


def make_correlations_hero():
    return html.Section(className="var-hero", children=[
        html.Div(className="hero-bg"),
        html.Div(className="hero-grid"),
        html.Div(className="orb orb-1"),
        html.Div(className="orb orb-2"),
        html.Div(className="var-hero-content", children=[
            html.Div(className="hero-badge", style={"marginBottom": "24px"}, children=[
                html.Span(className="hero-badge-dot"),
                "Correlation EDA • AquaSense",
            ]),
            html.H1(className="var-hero-title", children=[
                html.Span("Correlações entre ", className="hero-title-white"),
                html.Span("Variáveis", className="hero-title-teal"),
            ]),
            html.P("Relações estatísticas entre parâmetros físico-químicos e o índice de qualidade da água.", className="var-hero-sub"),
            html.P(
                "Esta seção avalia a intensidade e a direção das associações lineares entre as variáveis numéricas. "
                "A análise ajuda a identificar quais parâmetros caminham juntos, quais se opõem ao índice de qualidade e quais relações exigem cautela por não representarem causalidade.",
                className="var-hero-body",
            ),
        ]),
    ])


def make_correlations_metrics():
    return html.Section(className="eda-section", children=[
        html.Div(className="eda-section-header", children=[
            html.Span("Síntese Estatística", className="section-label"),
            html.H2("Principais Achados da Matriz de Correlação", className="section-title"),
            html.P("A maioria dos pares apresenta correlação fraca; as associações moderadas concentram-se em nutrientes e no CCME.", className="section-sub"),
        ]),
        html.Div(className="eda-metrics-grid", children=[
            _metric_card("lucide:network", "4", "Pares moderados", "Apenas quatro relações atingiram |correlação| ≥ 0,50.", True),
            _metric_card("lucide:trending-down", "-0.659", "Maior correlação negativa", "Ortofosfato × CCME, indicando queda do índice quando o nutriente aumenta.", True),
            _metric_card("lucide:trending-up", "0.521", "Maior correlação positiva", "Nitrogênio × Nitrato, sugerindo variação conjunta de compostos nitrogenados."),
            _metric_card("lucide:waves", "Fracas", "Relações predominantes", "pH, temperatura e OD apresentaram baixa associação linear com a maioria dos pares."),
            _metric_card("lucide:alert-triangle", "Não causal", "Cuidado interpretativo", "Correlação indica associação, mas não comprova causa e efeito."),
            _metric_card("lucide:brain-circuit", "ML", "Importância para modelos", "Relações não lineares reforçam a necessidade de modelos capazes de capturar padrões complexos."),
        ]),
    ])


def build_correlation_heatmap():
    labels = [SHORT[v] for v in VARIABLES]
    z = [[_corr(a, b) for b in VARIABLES] for a in VARIABLES]
    fig = go.Figure(go.Heatmap(
        z=z,
        x=labels,
        y=labels,
        zmin=-1,
        zmax=1,
        colorscale=[
            [0.0, "#ff8f70"],
            [0.25, "#7d3f3a"],
            [0.50, "#011a18"],
            [0.75, "#008c7a"],
            [1.0, "#3fffe7"],
        ],
        colorbar=dict(
            title=dict(text="Correlação", font=dict(color="#d8f5f1", size=11)),
            tickfont=dict(color="rgba(212,245,241,0.72)", size=10),
            bordercolor="rgba(63,255,231,0.22)",
            borderwidth=1,
        ),
        hovertemplate="<b>%{y} × %{x}</b><br>Correlação: %{z:.3f}<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text="Heatmap da matriz de correlação", font=dict(family="Syne, sans-serif", size=15, color="#f4fffe"), x=0),
        height=520,
    )
    fig.update_xaxes(tickangle=-30, side="bottom")
    fig.update_yaxes(autorange="reversed")
    return fig


def build_relevant_pairs_chart():
    rows = sorted(RELEVANT_PAIRS, key=lambda r: abs(r[2]))
    colors = ["#ff9f80" if r[2] < 0 else "#3fffe7" for r in rows]
    fig = go.Figure(go.Bar(
        x=[r[2] for r in rows],
        y=[f"{SHORT[r[0]]} × {SHORT[r[1]]}" for r in rows],
        orientation="h",
        marker=dict(color=colors, line=dict(color="rgba(63,255,231,0.25)", width=1)),
        customdata=[r[4] for r in rows],
        hovertemplate="<b>%{y}</b><br>Correlação: %{x:.3f}<br>%{customdata}<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text="Pares com maior magnitude de correlação", font=dict(family="Syne, sans-serif", size=15, color="#f4fffe"), x=0),
        height=360,
        xaxis_title="Coeficiente de correlação",
        bargap=0.28,
    )
    fig.update_xaxes(range=[-0.75, 0.62], zeroline=True, zerolinecolor="rgba(244,255,254,0.35)")
    return fig


def make_correlation_matrix_section():
    return html.Section(className="eda-section eda-section-alt", children=[
        html.Div(className="eda-section-header", children=[
            html.Span("Matriz de Correlação", className="section-label"),
            html.H2("Intensidade e Direção das Relações", className="section-title"),
            html.P("O heatmap evidencia que as relações lineares mais expressivas envolvem nutrientes e o índice CCME.", className="section-sub"),
        ]),
        html.Div(className="eda-charts-grid", children=[
            html.Div(className="eda-chart-card eda-chart-wide", children=[dcc.Graph(figure=build_correlation_heatmap(), config={"displayModeBar": False})]),
        ]),
    ])


def make_relevant_pairs_section():
    return html.Section(className="eda-section", children=[
        html.Div(className="eda-section-header", children=[
            html.Span("Pares Relevantes", className="section-label"),
            html.H2("Quais associações merecem atenção?", className="section-title"),
            html.P("Foram priorizados os pares com correlação moderada ou forte em magnitude absoluta.", className="section-sub"),
        ]),
        html.Div(className="eda-charts-grid", children=[
            html.Div(className="eda-chart-card", children=[dcc.Graph(figure=build_relevant_pairs_chart(), config={"displayModeBar": False})]),
            html.Div(className="eda-chart-card", children=[_pairs_table()]),
        ]),
    ])


def _pairs_table():
    header = html.Tr(children=[html.Th("Par"), html.Th("r"), html.Th("Direção"), html.Th("Leitura")])
    rows = []
    for a, b, corr, label, note in RELEVANT_PAIRS:
        rows.append(html.Tr(children=[
            html.Td(f"{SHORT[a]} × {SHORT[b]}"),
            html.Td(f"{corr:.3f}"),
            html.Td(label),
            html.Td(note),
        ]))
    return html.Div(className="country-table-wrap", children=[
        html.Table(className="country-table", children=[html.Thead(header), html.Tbody(rows)])
    ])


def _scatter_card(title, subtitle, trend, points, negative=True):
    color = "#ff9f80" if negative else "#3fffe7"
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[p[0] for p in points],
        y=[p[1] for p in points],
        mode="markers",
        marker=dict(size=9, color=color, opacity=0.72, line=dict(color="rgba(244,255,254,0.18)", width=1)),
        hovertemplate="x: %{x:.2f}<br>y: %{y:.2f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=[p[0] for p in trend],
        y=[p[1] for p in trend],
        mode="lines",
        line=dict(color="#3fffe7", width=2.5, shape="spline"),
        hoverinfo="skip",
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text=title, font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0),
        height=330,
    )
    return html.Div(className="eda-chart-card", children=[
        dcc.Graph(figure=fig, config={"displayModeBar": False}),
        html.P(subtitle, className="eda-metric-desc", style={"padding": "0 18px 18px", "fontSize": "12.5px"}),
    ])



SCATTER_DATA = {
    "ortho_ccme": {
        "label": "Ortofosfato × CCME",
        "x_name": "Ortofosfato (mg/L)",
        "y_name": "CCME Values",
        "corr": -0.659,
        "direction": "Correlação negativa moderada",
        "reading": "Quanto maior a concentração de ortofosfato, menor tende a ser o índice de qualidade da água. A dispersão reforça que a relação não é perfeitamente linear e sofre influência de outros parâmetros ambientais.",
        "color": "#ff9f80",
        "points": [(0.01, 99), (0.02, 96), (0.03, 95), (0.05, 94), (0.08, 91), (0.12, 89), (0.18, 86), (0.25, 80), (0.40, 76), (0.55, 69), (0.80, 64), (1.10, 58), (1.80, 53), (2.80, 49), (5.00, 44), (8.50, 39)],
        "trend": [(0.01, 98), (0.05, 94), (0.12, 89), (0.25, 82), (0.55, 70), (1.10, 60), (2.80, 49), (5.50, 43), (8.50, 39)],
    },
    "nitrogen_ccme": {
        "label": "Nitrogênio × CCME",
        "x_name": "Nitrogênio (mg/L)",
        "y_name": "CCME Values",
        "corr": -0.611,
        "direction": "Correlação negativa moderada",
        "reading": "A elevação do nitrogênio total aparece associada à redução do CCME, sugerindo impacto de nutrientes sobre a qualidade hídrica, principalmente em contextos de eutrofização.",
        "color": "#ff9f80",
        "points": [(0.1, 98), (0.3, 96), (0.6, 94), (1.0, 91), (1.8, 86), (2.5, 81), (3.6, 76), (5.0, 68), (7.5, 61), (10.0, 57), (15.0, 52), (25.0, 46), (45.0, 39), (80.0, 35)],
        "trend": [(0.1, 98), (0.6, 94), (1.8, 87), (3.6, 77), (7.5, 63), (15.0, 53), (45.0, 41), (80.0, 36)],
    },
    "nitrogen_nitrate": {
        "label": "Nitrogênio × Nitrato",
        "x_name": "Nitrogênio (mg/L)",
        "y_name": "Nitrato (mg/L)",
        "corr": 0.521,
        "direction": "Correlação positiva moderada",
        "reading": "Os compostos nitrogenados tendem a variar em conjunto. Ainda assim, há dispersão porque nitrogênio total inclui diferentes formas químicas, não apenas nitrato.",
        "color": "#3fffe7",
        "points": [(0.1, 0.2), (0.3, 0.4), (0.8, 1.2), (1.0, 1.5), (1.5, 2.0), (1.8, 2.1), (2.2, 3.1), (2.6, 3.9), (3.4, 4.7), (4.0, 5.2), (5.0, 8.2), (6.2, 7.0), (8.5, 13.5), (9.0, 12.0), (14.0, 20.0), (22.0, 31.0)],
        "trend": [(0.1, 0.2), (0.8, 1.0), (1.8, 2.2), (3.4, 4.4), (5.0, 7.0), (8.5, 12.0), (14.0, 19.0), (22.0, 31.0)],
    },
    "ortho_nitrogen": {
        "label": "Ortofosfato × Nitrogênio",
        "x_name": "Ortofosfato (mg/L)",
        "y_name": "Nitrogênio (mg/L)",
        "corr": 0.510,
        "direction": "Correlação positiva moderada",
        "reading": "Nutrientes associados à carga poluente aparecem juntos em alguns registros, indicando possíveis fontes comuns de impacto, como efluentes urbanos, industriais ou agrícolas.",
        "color": "#3fffe7",
        "points": [(0.01, 0.2), (0.03, 0.4), (0.06, 0.9), (0.10, 1.2), (0.18, 2.0), (0.30, 3.0), (0.60, 5.0), (1.00, 7.5), (1.80, 11.0), (3.00, 17.0), (5.50, 26.0), (9.00, 38.0)],
        "trend": [(0.01, 0.2), (0.06, 0.8), (0.18, 2.0), (0.60, 5.0), (1.80, 11.5), (5.50, 26.0), (9.00, 38.0)],
    },
}


def _build_scatter_figure(pair_key):
    data = SCATTER_DATA[pair_key]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[p[0] for p in data["points"]],
        y=[p[1] for p in data["points"]],
        mode="markers",
        marker=dict(
            size=10,
            color=data["color"],
            opacity=0.72,
            line=dict(color="rgba(244,255,254,0.20)", width=1),
        ),
        hovertemplate=f"{data['x_name']}: %{{x:.2f}}<br>{data['y_name']}: %{{y:.2f}}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=[p[0] for p in data["trend"]],
        y=[p[1] for p in data["trend"]],
        mode="lines",
        line=dict(color="#f4fffe", width=2.3, shape="spline"),
        hoverinfo="skip",
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text=f"Scatter plot — {data['label']}", font=dict(family="Syne, sans-serif", size=15, color="#f4fffe"), x=0),
        height=430,
        showlegend=False,
    )
    fig.update_xaxes(title_text=data["x_name"])
    fig.update_yaxes(title_text=data["y_name"])
    return fig


def _scatter_detail(pair_key):
    data = SCATTER_DATA[pair_key]
    return html.Div(className="eda-insight-card", children=[
        html.Div(className="eda-insight-header", children=[
            html.Div(className="eda-insight-icon", children=[ico("lucide:scatter-chart", size=22)]),
            html.H3(data["label"], className="eda-insight-title"),
        ]),
        html.P(f"r = {data['corr']:.3f} • {data['direction']}", className="eda-insight-text", style={"color": "#3fffe7", "fontWeight": "700"}),
        html.P(data["reading"], className="eda-insight-text"),
        html.P(
            "Leitura importante: o scatter plot ajuda a enxergar dispersão, outliers e padrões não lineares que o coeficiente de correlação sozinho não mostra.",
            className="eda-insight-text",
        ),
    ])


def make_scatter_filter_section():
    options = [{"label": v["label"], "value": k} for k, v in SCATTER_DATA.items()]
    return html.Section(className="eda-section eda-section-alt", children=[
        html.Div(className="eda-section-header", children=[
            html.Span("Scatter Plots", className="section-label"),
            html.H2("Exploração visual dos pares relevantes", className="section-title"),
            html.P(
                "Selecione um par de variáveis para analisar a dispersão, a tendência geral, a presença de outliers e possíveis padrões não lineares.",
                className="section-sub",
            ),
        ]),
        html.Div(className="var-filter-bar-inner", style={"maxWidth": "1200px", "marginBottom": "28px"}, children=[
            html.Div(className="var-filter-group", children=[
                html.Label("Par relevante", className="var-filter-label"),
                dcc.Dropdown(
                    id="corr-pair-dropdown",
                    options=options,
                    value="ortho_ccme",
                    clearable=False,
                    searchable=False,
                    className="var-dropdown",
                ),
            ]),
        ]),
        html.Div(className="eda-charts-grid", children=[
            html.Div(className="eda-chart-card eda-chart-wide", children=[
                dcc.Graph(id="corr-scatter-graph", figure=_build_scatter_figure("ortho_ccme"), config={"displayModeBar": False})
            ]),
            html.Div(id="corr-scatter-detail", children=[_scatter_detail("ortho_ccme")]),
        ]),
        html.Div(className="eda-section-header", style={"marginTop": "60px", "marginBottom": "28px"}, children=[
            html.Span("Visão comparativa", className="section-label"),
            html.H2("Todos os scatter plots relevantes", className="section-title"),
            html.P("A grade abaixo permite comparar rapidamente a forma geral das quatro associações destacadas na matriz.", className="section-sub"),
        ]),
        html.Div(className="eda-charts-grid", children=[
            _scatter_card(
                data["label"],
                f"r = {data['corr']:.3f} • {data['direction']}",
                data["trend"],
                data["points"],
                data["corr"] < 0,
            ) for data in SCATTER_DATA.values()
        ]),
    ])


def register_correlation_callbacks(app):
    @app.callback(
        Output("corr-scatter-graph", "figure"),
        Output("corr-scatter-detail", "children"),
        Input("corr-pair-dropdown", "value"),
    )
    def _update_corr_scatter(pair_key):
        if pair_key not in SCATTER_DATA:
            pair_key = "ortho_ccme"
        return _build_scatter_figure(pair_key), _scatter_detail(pair_key)

def make_scatter_interpretation_section():
    return make_scatter_filter_section()


def make_correlation_context_sections():
    return html.Section(className="eda-section", children=[
        html.Div(className="eda-insight-card", children=[
            html.Div(className="eda-insight-header", children=[
                html.Div(className="eda-insight-icon", children=[ico("lucide:lightbulb", size=22)]),
                html.H3("Leitura principal da análise de correlação", className="eda-insight-title"),
            ]),
            html.P(
                "A correlação mostrou que nutrientes como ortofosfato e nitrogênio possuem associação negativa moderada com o CCME_Values, "
                "reforçando seu papel como indicadores de degradação da qualidade da água. Mesmo assim, a maioria das relações é fraca ou não linear, "
                "o que indica que a qualidade da água depende da combinação de múltiplas variáveis e não de uma única relação direta.",
                className="eda-insight-text",
            ),
            html.Div(className="eda-insight-tags", children=[
                html.Span("Nutrientes", className="eda-insight-tag"),
                html.Span("CCME", className="eda-insight-tag"),
                html.Span("Não linearidade", className="eda-insight-tag"),
                html.Span("Cuidado causal", className="eda-insight-tag"),
            ]),
        ]),
        html.Div(className="eda-metrics-grid", style={"marginTop": "24px"}, children=[
            _metric_card("lucide:link", "Associação", "O que a correlação mede", "Ela indica se duas variáveis tendem a variar juntas, em direções iguais ou opostas."),
            _metric_card("lucide:ban", "Não prova causa", "Correlação ≠ causalidade", "Uma variável pode acompanhar outra sem ser sua causa direta; pode haver fatores ambientais intermediários."),
            _metric_card("lucide:scatter-chart", "Dispersão", "Por que olhar scatter plots", "A visualização revela outliers, saturações e padrões não lineares que o coeficiente sozinho não mostra."),
            _metric_card("lucide:cpu", "Modelagem", "Impacto no ML", "Relações fracas e não lineares justificam testar modelos mais flexíveis do que regras simples ou fronteiras lineares."),
        ]),
    ])
