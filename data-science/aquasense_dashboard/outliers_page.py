
# ============================================================
#  AquaSense — Outliers e Assimetria
#  outliers_page.py
# ============================================================

import numpy as np
from dash import html, dcc, Input, Output
from dash_iconify import DashIconify
import plotly.graph_objects as go

from variables_page import VARIABLES, _generate_raw, interpret_skew, interpret_kurt, interpret_cv


def ico(icon_name, size=24, color="#3fffe7"):
    return DashIconify(icon=icon_name, width=size, height=size, color=color)


CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#d8f5f1"),
    margin=dict(l=18, r=18, t=44, b=24),
    showlegend=False,
    xaxis=dict(
        gridcolor="rgba(63,255,231,0.08)",
        linecolor="rgba(63,255,231,0.15)",
        tickfont=dict(size=11, color="rgba(212,245,241,0.66)"),
        tickcolor="rgba(63,255,231,0.15)",
    ),
    yaxis=dict(
        gridcolor="rgba(63,255,231,0.08)",
        linecolor="rgba(63,255,231,0.15)",
        tickfont=dict(size=11, color="rgba(212,245,241,0.66)"),
        tickcolor="rgba(63,255,231,0.15)",
    ),
    hoverlabel=dict(
        bgcolor="rgba(0,77,72,0.94)",
        bordercolor="rgba(63,255,231,0.35)",
        font=dict(color="#f4fffe", size=12),
    ),
)


def _var_options():
    return [{"label": meta["label"], "value": key} for key, meta in VARIABLES.items()]


def _outlier_index(meta):
    iqr = max(meta["q3"] - meta["q1"], 1e-9)
    return abs(meta["skew"]) * 0.55 + max(meta["kurtosis"], 0) * 0.012 + (meta["std"] / (abs(meta["mean"]) + 1e-9)) * 0.9 + np.log1p(meta["vmax"] / iqr) * 0.35


def _metric_rows():
    rows = []
    for key, m in VARIABLES.items():
        cv = m["std"] / (abs(m["mean"]) + 1e-9)
        iqr = m["q3"] - m["q1"]
        rows.append({
            "key": key,
            "label": m["label"],
            "skew": m["skew"],
            "kurtosis": m["kurtosis"],
            "std": m["std"],
            "cv": cv,
            "iqr": iqr,
            "outlier_index": _outlier_index(m),
        })
    return rows


def _stat_card(value, title, text, icon_name, highlight=False):
    cls = "var-stat-card var-stat-card-highlight" if highlight else "var-stat-card"
    return html.Div(className=cls, children=[
        html.Div(className="var-stat-icon", children=[ico(icon_name, size=18)]),
        html.Div(className="var-stat-value", children=value),
        html.Div(className="var-stat-title", children=title),
        html.Div(className="var-stat-interp", children=text),
    ])


# ============================================================
#  PAGE SECTIONS
# ============================================================

def make_outliers_hero():
    return html.Section(className="var-hero", children=[
        html.Div(className="hero-bg", children=[html.Div(className="hero-grid"), html.Div(className="orb orb-1"), html.Div(className="orb orb-2")]),
        html.Div(className="var-hero-content", children=[
            html.Span("EDA AVANÇADA", className="section-label"),
            html.H1("Outliers e Assimetria dos Parâmetros Ambientais", className="var-hero-title"),
            html.P("Análise estatística de valores extremos, caudas longas, dispersão e comportamento assimétrico nas variáveis físico-químicas do AquaSense, alinhada aos notebooks de histogramas, boxplots e assimetrias da EDA.", className="var-hero-sub"),
            html.P("Em dados ambientais, outliers não devem ser tratados automaticamente como erro. Muitos deles podem representar eventos reais de contaminação, despejos pontuais, alterações hidrológicas ou condições críticas de um corpo hídrico.", className="var-hero-body"),
        ]),
    ])


def make_outlier_metrics():
    rows = _metric_rows()
    max_skew = max(rows, key=lambda r: abs(r["skew"]))
    min_skew = min(rows, key=lambda r: abs(r["skew"]))
    max_kurt = max(rows, key=lambda r: r["kurtosis"])
    max_cv = max(rows, key=lambda r: r["cv"])
    max_out = max(rows, key=lambda r: r["outlier_index"])
    extreme_count = sum(1 for r in rows if abs(r["skew"]) > 3 or r["kurtosis"] > 10)

    return html.Section(className="outlier-section", children=[
        html.Div(className="var-stats-inner", children=[
            _stat_card(max_skew["label"], "Maior assimetria", f"Skewness = {max_skew['skew']:.2f}. Indica cauda longa e poucos valores muito altos/baixos.", "lucide:trending-up", True),
            _stat_card(min_skew["label"], "Mais simétrica", f"Skewness = {min_skew['skew']:.2f}. Distribuição mais equilibrada em torno do centro.", "lucide:activity"),
            _stat_card(max_kurt["label"], "Maior curtose", f"Curtose = {max_kurt['kurtosis']:.1f}. Forte concentração com eventos extremos raros.", "lucide:move-vertical", True),
            _stat_card(max_cv["label"], "Maior dispersão relativa", interpret_cv(VARIABLES[max_cv['key']]['mean'], VARIABLES[max_cv['key']]['std']), "lucide:expand"),
            _stat_card(max_out["label"], "Maior índice de outliers", "Combina assimetria, curtose, variabilidade e distância dos extremos.", "lucide:alert-triangle", True),
            _stat_card(f"{extreme_count}/{len(rows)}", "Variáveis críticas", "Variáveis com assimetria ou curtose elevadas, exigindo interpretação ambiental cuidadosa.", "lucide:flask-conical"),
        ])
    ])


def build_outlier_heatmap():
    rows = _metric_rows()
    labels = [r["label"] for r in rows]
    metrics = ["Assimetria", "Curtose", "Coef. variação", "Índice outlier"]
    raw = np.array([
        [abs(r["skew"]) for r in rows],
        [max(r["kurtosis"], 0) for r in rows],
        [r["cv"] for r in rows],
        [r["outlier_index"] for r in rows],
    ], dtype=float)
    z = raw / (raw.max(axis=1, keepdims=True) + 1e-9)

    fig = go.Figure(go.Heatmap(
        z=z,
        x=labels,
        y=metrics,
        colorscale=[[0, "rgba(0,77,72,0.18)"], [0.35, "#006960"], [0.7, "#00c4ad"], [1, "#3fffe7"]],
        hovertemplate="<b>%{x}</b><br>%{y}<br>Intensidade normalizada: %{z:.2f}<extra></extra>",
        colorbar=dict(title=dict(text="Intensidade", font=dict(color="#d8f5f1")), tickfont=dict(color="#d8f5f1")),
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text="Mapa de intensidade estatística", font=dict(family="Syne, sans-serif", size=15, color="#f4fffe"), x=0),
        height=360,
    )
    fig.update_xaxes(tickangle=-32, tickfont=dict(size=11, color="rgba(212,245,241,0.65)"))
    return fig


def make_outlier_heatmap_section():
    return html.Section(className="outlier-section outlier-section-wide", children=[
        html.Div(className="var-chart-card", children=[
            html.Div(className="var-chart-header", children=[
                html.Div(className="var-chart-icon", children=[ico("lucide:grid-3x3")]),
                html.Div(children=[
                    html.H4("Heatmap de Assimetria, Curtose e Outliers", className="var-chart-title"),
                    html.P("Comparação normalizada entre variáveis para destacar distribuições mais críticas.", className="var-chart-sub"),
                ]),
            ]),
            dcc.Graph(figure=build_outlier_heatmap(), config={"displayModeBar": False}),
        ])
    ])


def build_skew_ranking():
    rows = sorted(_metric_rows(), key=lambda r: abs(r["skew"]), reverse=True)
    labels = [r["label"] for r in rows][::-1]
    values = [abs(r["skew"]) for r in rows][::-1]
    signs = ["positiva" if r["skew"] > 0 else "negativa" for r in rows][::-1]

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation="h",
        marker=dict(color=values, colorscale=[[0, "#006960"], [0.55, "#00c4ad"], [1, "#3fffe7"]], line=dict(color="rgba(63,255,231,0.26)", width=1)),
        hovertemplate="<b>%{y}</b><br>|Skewness|: %{x:.2f}<extra></extra>",
        customdata=signs,
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Ranking das variáveis mais assimétricas", font=dict(family="Syne, sans-serif", size=15, color="#f4fffe"), x=0),
        height=420,
        xaxis_title="Intensidade da assimetria absoluta",
    )
    return fig


def make_outlier_ranking_section():
    return html.Section(className="outlier-section", children=[
        html.Div(className="outlier-grid-2", children=[
            html.Div(className="var-chart-card", children=[
                html.Div(className="var-chart-header", children=[
                    html.Div(className="var-chart-icon", children=[ico("lucide:bar-chart-horizontal")]),
                    html.Div(children=[
                        html.H4("Ranking de Assimetria", className="var-chart-title"),
                        html.P("Variáveis com caudas longas merecem atenção analítica e ambiental.", className="var-chart-sub"),
                    ]),
                ]),
                dcc.Graph(figure=build_skew_ranking(), config={"displayModeBar": False}),
            ]),
            html.Div(className="outlier-narrative-card", children=[
                html.H3("Como interpretar a assimetria?", className="outlier-narrative-title"),
                html.P("Assimetria positiva significa que a maioria dos registros está concentrada em valores baixos, mas existem poucos valores muito altos puxando a distribuição para a direita. Isso é comum em variáveis de poluição, como Ammonia, DBO, Orthophosphate e Nitrate, que aparecem entre as maiores assimetrias da amostra analisada.", className="outlier-narrative-text"),
                html.P("No contexto ambiental, esses picos não devem ser removidos automaticamente. Eles podem indicar despejos pontuais, eventos de chuva, efluentes agrícolas ou situações reais de degradação hídrica.", className="outlier-narrative-text"),
                html.Div(className="outlier-chip-row", children=[
                    html.Span("caudas longas", className="eda-insight-tag"),
                    html.Span("eventos extremos", className="eda-insight-tag"),
                    html.Span("poluição pontual", className="eda-insight-tag"),
                    html.Span("interpretação ambiental", className="eda-insight-tag"),
                ]),
            ]),
        ])
    ])


def build_variable_distribution(var_key, scale="linear"):
    m = VARIABLES[var_key]
    np.random.seed(24)
    raw = _generate_raw(m, size=900)
    y_title = f"{m['label']} [{m['unit']}]"
    if scale == "log" and raw.min() >= 0:
        raw = np.log1p(raw)
        y_title = f"log(1 + {m['label']})"

    counts, bins = np.histogram(raw, bins=34)
    centers = (bins[:-1] + bins[1:]) / 2
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=raw,
        nbinsx=34,
        marker=dict(color="rgba(63,255,231,0.42)", line=dict(color="rgba(63,255,231,0.24)", width=1)),
        hovertemplate="Faixa: %{x:.3f}<br>Frequência: %{y}<extra></extra>",
        name="Histograma",
    ))
    fig.add_trace(go.Scatter(
        x=centers,
        y=counts,
        mode="lines",
        line=dict(color="#f4fffe", width=2.2, shape="spline"),
        fill="tozeroy",
        fillcolor="rgba(244,255,254,0.04)",
        hoverinfo="skip",
        name="Tendência",
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=f"Distribuição — {m['label']}", font=dict(family="Syne, sans-serif", size=15, color="#f4fffe"), x=0),
        height=330,
        xaxis_title=y_title,
        yaxis_title="Frequência",
        bargap=0.03,
    )
    return fig


def build_variable_boxplot(var_key, scale="linear"):
    m = VARIABLES[var_key]
    np.random.seed(31)
    raw = _generate_raw(m, size=700)
    y_title = f"{m['label']} [{m['unit']}]"
    if scale == "log" and raw.min() >= 0:
        raw = np.log1p(raw)
        y_title = f"log(1 + {m['label']})"
    fig = go.Figure(go.Box(
        y=raw,
        name=m["label"],
        boxpoints="outliers",
        marker=dict(color=m.get("color", "#3fffe7"), size=4, opacity=0.38),
        line=dict(color="#3fffe7", width=1.8),
        fillcolor="rgba(63,255,231,0.08)",
        hovertemplate="%{y:.4f}<extra></extra>",
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Boxplot dos valores extremos", font=dict(family="Syne, sans-serif", size=15, color="#f4fffe"), x=0),
        height=330,
        yaxis_title=y_title,
    )
    return fig


def build_variable_insight(var_key):
    m = VARIABLES[var_key]
    iqr = m["q3"] - m["q1"]
    upper = m["q3"] + 1.5 * iqr
    lower = m["q1"] - 1.5 * iqr
    return html.Div(className="outlier-narrative-card", children=[
        html.H3(f"Leitura ambiental — {m['label']}", className="outlier-narrative-title"),
        html.P(m["interpretation"], className="outlier-narrative-text"),
        html.Div(className="outlier-chip-row", children=[
            html.Span(f"Skew: {m['skew']:.2f}", className="eda-insight-tag"),
            html.Span(f"Curtose: {m['kurtosis']:.1f}", className="eda-insight-tag"),
            html.Span(f"IQR: {iqr:.3g} {m['unit']}", className="eda-insight-tag"),
            html.Span(f"Limite outlier sup.: {upper:.3g}", className="eda-insight-tag"),
        ]),
        html.P("Regra estatística utilizada como referência visual: valores abaixo de Q1 − 1,5×IQR ou acima de Q3 + 1,5×IQR tendem a aparecer como outliers no boxplot. A decisão de remover ou manter depende do contexto ambiental.", className="outlier-note"),
    ])


def make_outlier_interactive_section():
    first = list(VARIABLES.keys())[0]
    return html.Section(className="outlier-section outlier-section-wide", children=[
        html.Div(className="eda-section-header", style={"marginBottom": "28px"}, children=[
            html.Span("EXPLORAÇÃO INTERATIVA", className="section-label"),
            html.H2("Distribuições, Boxplots e Leitura dos Extremos", className="section-title"),
            html.P("Selecione uma variável para observar a forma da distribuição, o comportamento dos outliers e o significado ambiental dos valores extremos.", className="section-sub"),
        ]),
        html.Div(className="outlier-filter-card", children=[
            html.Div(className="var-filter-group", children=[
                html.Label("Variável Ambiental", className="var-filter-label"),
                dcc.Dropdown(id="outlier-var-select", options=_var_options(), value=first, clearable=False, className="var-dropdown"),
            ]),
            html.Div(className="var-filter-group var-filter-group-scale", children=[
                html.Label("Escala", className="var-filter-label"),
                html.Div(className="var-scale-toggle-wrap", children=[
                    dcc.RadioItems(
                        id="outlier-scale-select",
                        options=[{"label": "Linear", "value": "linear"}, {"label": "Log", "value": "log"}],
                        value="linear", className="var-scale-toggle",
                        inputClassName="var-scale-radio", labelClassName="var-scale-label",
                    ),
                ]),
            ]),
        ]),
        html.Div(className="outlier-grid-2", children=[
            html.Div(className="var-chart-card", children=[dcc.Graph(id="outlier-dist-chart", config={"displayModeBar": False})]),
            html.Div(className="var-chart-card", children=[dcc.Graph(id="outlier-box-chart", config={"displayModeBar": False})]),
        ]),
        html.Div(style={"height": "24px"}),
        html.Div(id="outlier-insight-card"),
    ])


def make_outlier_context_sections():
    return html.Section(className="outlier-section", children=[
        html.Div(className="outlier-grid-3", children=[
            html.Div(className="outlier-narrative-card", children=[
                html.H3("Impacto no Machine Learning", className="outlier-narrative-title"),
                html.P("Distribuições muito assimétricas podem influenciar modelos lineares, distâncias no KMeans e componentes do PCA. Por isso, a padronização e a análise de escala são etapas importantes antes da modelagem.", className="outlier-narrative-text"),
            ]),
            html.Div(className="outlier-narrative-card", children=[
                html.H3("Outlier não é automaticamente erro", className="outlier-narrative-title"),
                html.P("Em qualidade da água, valores extremos podem ser justamente os registros mais importantes, pois indicam eventos raros de contaminação, hipóxia, eutrofização ou lançamento de efluentes.", className="outlier-narrative-text"),
            ]),
            html.Div(className="outlier-narrative-card", children=[
                html.H3("Uso no dashboard", className="outlier-narrative-title"),
                html.P("A página ajuda a explicar por que a EDA veio antes do ML: entender dispersão, caudas e assimetrias evita interpretações superficiais e melhora a defesa técnica dos resultados.", className="outlier-narrative-text"),
            ]),
        ])
    ])


# ============================================================
#  CALLBACKS
# ============================================================

def register_outlier_callbacks(app):
    @app.callback(
        Output("outlier-dist-chart", "figure"),
        Output("outlier-box-chart", "figure"),
        Output("outlier-insight-card", "children"),
        Input("outlier-var-select", "value"),
        Input("outlier-scale-select", "value"),
    )
    def update_outlier_variable(var_key, scale):
        if not var_key or var_key not in VARIABLES:
            var_key = list(VARIABLES.keys())[0]
        return (
            build_variable_distribution(var_key, scale=scale),
            build_variable_boxplot(var_key, scale=scale),
            build_variable_insight(var_key),
        )
