# ============================================================
#  AquaSense — Análise por Corpo Hídrico 
# ============================================================

from dash import html, dcc
from dash_iconify import DashIconify
import plotly.graph_objects as go

TEAL_PALETTE = ["#3fffe7", "#00e0ca", "#00c4ad", "#00a893", "#008c7a", "#006960"]

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#d8f5f1"),
    margin=dict(l=18, r=18, t=42, b=18),
    showlegend=False,
    xaxis=dict(
        gridcolor="rgba(63,255,231,0.08)",
        linecolor="rgba(63,255,231,0.15)",
        tickfont=dict(size=11, color="rgba(212,245,241,0.65)"),
        tickcolor="rgba(63,255,231,0.15)",
    ),
    yaxis=dict(
        gridcolor="rgba(63,255,231,0.08)",
        linecolor="rgba(63,255,231,0.15)",
        tickfont=dict(size=11, color="rgba(212,245,241,0.65)"),
        tickcolor="rgba(63,255,231,0.15)",
    ),
    hoverlabel=dict(
        bgcolor="rgba(0,77,72,0.94)",
        bordercolor="rgba(63,255,231,0.35)",
        font=dict(color="#f4fffe", size=12),
    ),
)


WATERBODY_ROWS = [
    {"type": "River", "count": 1852579, "percent": 65.49, "ccme": 90.03, "dbo": 3.02, "ammonia": 0.41, "od": 10.04, "nitrate": 4.55, "note": "Tipo dominante no dataset; maior suporte estatístico para comparação e modelagem."},
    {"type": "Effluent", "count": 601550, "percent": 21.27, "ccme": 66.56, "dbo": 8.40, "ammonia": 3.48, "od": 10.20, "nitrate": 6.93, "note": "Alta carga orgânica e nutrientes; forte sinal de impacto ambiental."},
    {"type": "Lake", "count": 153603, "percent": 5.43, "ccme": 97.11, "dbo": 2.25, "ammonia": 0.16, "od": 9.61, "nitrate": 1.49, "note": "Qualidade média elevada, com menor carga de nutrientes comparada aos efluentes."},
    {"type": "Estuarine", "count": 49375, "percent": 1.75, "ccme": 85.12, "dbo": 3.24, "ammonia": 0.41, "od": 9.83, "nitrate": 4.13, "note": "Ambiente de transição, naturalmente mais variável por influência continental e marinha."},
    {"type": "Bay", "count": 45997, "percent": 1.63, "ccme": 96.51, "dbo": 0.91, "ammonia": 0.10, "od": 8.31, "nitrate": 0.14, "note": "Baixa carga média de nutrientes, mas exige leitura contextual por hidrodinâmica costeira."},
    {"type": "Sea Water", "count": 32061, "percent": 1.13, "ccme": 84.37, "dbo": 6.02, "ammonia": 1.44, "od": 9.84, "nitrate": 4.69, "note": "Qualidade intermediária, com valores influenciados por mistura e dinâmica costeira."},
    {"type": "Canal", "count": 28574, "percent": 1.01, "ccme": 86.53, "dbo": 3.37, "ammonia": 0.26, "od": 9.87, "nitrate": 3.93, "note": "Pode concentrar cargas urbanas e apresentar variabilidade local relevante."},
    {"type": "Sewage", "count": 23777, "percent": 0.84, "ccme": 53.66, "dbo": 88.25, "ammonia": 13.31, "od": 10.20, "nitrate": 4.80, "note": "Pior qualidade média; representa sinal claro de carga orgânica extrema."},
    {"type": "Marine", "count": 23162, "percent": 0.82, "ccme": 97.09, "dbo": 1.66, "ammonia": 0.05, "od": 9.41, "nitrate": 0.63, "note": "Qualidade média elevada e baixa carga média de nutrientes."},
    {"type": "Drainage", "count": 10205, "percent": 0.36, "ccme": 73.94, "dbo": 17.60, "ammonia": 3.26, "od": 10.15, "nitrate": 4.57, "note": "Sinal de carga orgânica e amoniacal elevada; possível influência urbana/agropecuária."},
    {"type": "Transitional", "count": 4275, "percent": 0.15, "ccme": 93.76, "dbo": 1.68, "ammonia": 0.21, "od": 9.37, "nitrate": 1.47, "note": "Baixa amostragem; interpretações devem ser feitas com cautela."},
    {"type": "Coastal", "count": 2819, "percent": 0.10, "ccme": 93.70, "dbo": 1.57, "ammonia": 0.79, "od": 9.63, "nitrate": 1.30, "note": "Menor representatividade; bom desempenho médio, mas pouco suporte amostral."},
]

PARAM_LABELS = {
    "dbo": "DBO média (mg/L)",
    "ammonia": "Amônia média (mg/L)",
    "od": "Oxigênio dissolvido médio (mg/L)",
    "nitrate": "Nitrato médio (mg/L)",
    "ccme": "CCME médio",
}


def ico(icon_name, size=22, color="#3fffe7"):
    return DashIconify(icon=icon_name, width=size, height=size, color=color)


def _fmt_int(v):
    return f"{v:,}".replace(",", ".")


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


def make_waterbody_hero():
    return html.Section(className="var-hero", children=[
        html.Div(className="hero-bg"),
        html.Div(className="hero-grid"),
        html.Div(className="orb orb-1"),
        html.Div(className="orb orb-2"),
        html.Div(className="var-hero-content", children=[
            html.Div(className="hero-badge", style={"marginBottom": "24px"}, children=[
                html.Span(className="hero-badge-dot"),
                "Waterbody EDA • AquaSense",
            ]),
            html.H1(className="var-hero-title", children=[
                html.Span("Análise por ", className="hero-title-white"),
                html.Span("Corpo Hídrico", className="hero-title-teal"),
            ]),
            html.P("Comparação estatística e ambiental entre diferentes tipos de ecossistemas aquáticos.", className="var-hero-sub"),
            html.P(
                "Esta seção avalia como rios, efluentes, lagos, áreas costeiras, canais e outros tipos de corpos hídricos se distribuem no dataset. "
                "A análise ajuda a entender representatividade, variação de parâmetros físico-químicos, possíveis vieses e padrões ambientais relevantes para a modelagem.",
                className="var-hero-body",
            ),
        ]),
    ])


def make_waterbody_metrics():
    total = sum(r["count"] for r in WATERBODY_ROWS)
    most = max(WATERBODY_ROWS, key=lambda r: r["count"])
    best = max(WATERBODY_ROWS, key=lambda r: r["ccme"])
    worst = min(WATERBODY_ROWS, key=lambda r: r["ccme"])
    max_dbo = max(WATERBODY_ROWS, key=lambda r: r["dbo"])
    max_n = max(WATERBODY_ROWS, key=lambda r: r["nitrate"])
    return html.Section(className="eda-section", children=[
        html.Div(className="eda-section-header", children=[
            html.Span("Ecossistemas", className="section-label"),
            html.H2("Métricas por Tipo de Corpo Hídrico", className="section-title"),
            html.P("Indicadores principais para compreender distribuição, qualidade média e padrões críticos entre os tipos de corpos hídricos.", className="section-sub"),
        ]),
        html.Div(className="eda-metrics-grid", children=[
            _metric_card("lucide:database", _fmt_int(total), "Registros analisados", "Volume total distribuído entre 12 tipos de corpos hídricos."),
            _metric_card("lucide:waves", most["type"], "Tipo mais frequente", f"{most['percent']:.2f}% dos registros estão concentrados em rios.", True),
            _metric_card("lucide:sparkles", best["type"], "Melhor qualidade média", f"CCME médio de {best['ccme']:.2f}, indicando melhor condição geral."),
            _metric_card("lucide:biohazard", worst["type"], "Maior criticidade", f"CCME médio de {worst['ccme']:.2f}, com forte carga orgânica.", True),
            _metric_card("lucide:flask-conical", max_dbo["type"], "Maior DBO média", f"DBO média de {max_dbo['dbo']:.2f} mg/L, sinal de matéria orgânica elevada.", True),
            _metric_card("lucide:leaf", max_n["type"], "Maior nitrato médio", f"Nitrato médio de {max_n['nitrate']:.2f} mg/L, associado a nutrientes."),
        ]),
    ])


def build_waterbody_count_chart():
    rows = sorted(WATERBODY_ROWS, key=lambda r: r["count"])
    fig = go.Figure(go.Bar(
        x=[r["count"] for r in rows],
        y=[r["type"] for r in rows],
        orientation="h",
        customdata=[r["percent"] for r in rows],
        marker=dict(color=["#006960", "#008c7a", "#00a893", "#00c4ad", "#00e0ca", "#3fffe7"] * 2,
                    line=dict(color="rgba(63,255,231,0.32)", width=1)),
        hovertemplate="<b>%{y}</b><br>%{x:,.0f} registros<br>%{customdata:.2f}% do dataset<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text="Distribuição de registros por corpo hídrico", font=dict(family="Syne, sans-serif", size=15, color="#f4fffe"), x=0),
        height=430,
        xaxis_title="Número de registros",
        bargap=0.28,
    )
    return fig


def build_waterbody_share_chart():
    top = WATERBODY_ROWS[:5]
    others = sum(r["count"] for r in WATERBODY_ROWS[5:])
    labels = [r["type"] for r in top] + ["Outros"]
    values = [r["count"] for r in top] + [others]
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.62,
        marker=dict(colors=TEAL_PALETTE, line=dict(color="rgba(1,26,24,0.95)", width=2)),
        textinfo="label+percent",
        textfont=dict(color="#f4fffe", size=11),
        hovertemplate="<b>%{label}</b><br>%{value:,.0f} registros<br>%{percent}<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color="#d8f5f1"),
        margin=dict(l=12, r=12, t=42, b=12),
        title=dict(text="Participação percentual", font=dict(family="Syne, sans-serif", size=15, color="#f4fffe"), x=0),
        height=430,
        showlegend=False,
        annotations=[dict(text="Tipos", x=0.5, y=0.5, showarrow=False, font=dict(size=16, color="#3fffe7", family="Syne"))],
    )
    return fig


def make_waterbody_distribution_section():
    return html.Section(className="eda-section eda-section-alt", children=[
        html.Div(className="eda-section-header", children=[
            html.Span("Distribuição", className="section-label"),
            html.H2("Representatividade por Tipo de Corpo Hídrico", className="section-title"),
            html.P("A base é fortemente concentrada em rios, efluentes e lagos. Tipos menos frequentes exigem leitura estatística mais cuidadosa.", className="section-sub"),
        ]),
        html.Div(className="eda-charts-grid", children=[
            html.Div(className="eda-chart-card", children=[dcc.Graph(figure=build_waterbody_count_chart(), config={"displayModeBar": False})]),
            html.Div(className="eda-chart-card", children=[dcc.Graph(figure=build_waterbody_share_chart(), config={"displayModeBar": False})]),
        ]),
    ])


def build_quality_bar_chart():
    rows = sorted(WATERBODY_ROWS, key=lambda r: r["ccme"])
    colors = ["#ff9f80" if r["ccme"] < 70 else "#ffd580" if r["ccme"] < 85 else "#3fffe7" for r in rows]
    fig = go.Figure(go.Bar(
        x=[r["ccme"] for r in rows],
        y=[r["type"] for r in rows],
        orientation="h",
        marker=dict(color=colors, line=dict(color="rgba(63,255,231,0.25)", width=1)),
        customdata=[(r["dbo"], r["ammonia"], r["nitrate"]) for r in rows],
        hovertemplate="<b>%{y}</b><br>CCME médio: %{x:.2f}<br>DBO média: %{customdata[0]:.2f}<br>Amônia média: %{customdata[1]:.2f}<br>Nitrato médio: %{customdata[2]:.2f}<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text="Qualidade média por corpo hídrico (CCME)", font=dict(family="Syne, sans-serif", size=15, color="#f4fffe"), x=0),
        height=420,
        xaxis_title="CCME médio",
        bargap=0.26,
    )
    fig.update_xaxes(range=[45, 101])
    return fig


def build_parameter_heatmap():
    types = [r["type"] for r in WATERBODY_ROWS]
    metrics = ["dbo", "ammonia", "od", "nitrate", "ccme"]
    z = []
    for m in metrics:
        vals = [r[m] for r in WATERBODY_ROWS]
        mn, mx = min(vals), max(vals)
        z.append([(v - mn) / (mx - mn) if mx != mn else 0 for v in vals])
    fig = go.Figure(go.Heatmap(
        z=z,
        x=types,
        y=[PARAM_LABELS[m] for m in metrics],
        colorscale=[[0, "#011a18"], [0.35, "#006960"], [0.7, "#00c4ad"], [1, "#3fffe7"]],
        colorbar=dict(
            title=dict(text="Intensidade", font=dict(color="#d8f5f1", size=11)),
            tickfont=dict(color="rgba(212,245,241,0.7)", size=10),
            bordercolor="rgba(63,255,231,0.22)",
            borderwidth=1,
        ),
        hovertemplate="<b>%{x}</b><br>%{y}<br>Intensidade normalizada: %{z:.2f}<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text="Mapa comparativo de parâmetros médios", font=dict(family="Syne, sans-serif", size=15, color="#f4fffe"), x=0),
        height=390,
    )
    fig.update_xaxes(tickangle=-30)
    return fig


def make_waterbody_quality_section():
    return html.Section(className="eda-section", children=[
        html.Div(className="eda-section-header", children=[
            html.Span("Parâmetros", className="section-label"),
            html.H2("Qualidade e Intensidade Ambiental", className="section-title"),
            html.P("Comparação entre qualidade média e intensidade dos principais parâmetros físico-químicos por tipo de corpo hídrico.", className="section-sub"),
        ]),
        html.Div(className="eda-charts-grid", children=[
            html.Div(className="eda-chart-card", children=[dcc.Graph(figure=build_quality_bar_chart(), config={"displayModeBar": False})]),
            html.Div(className="eda-chart-card", children=[dcc.Graph(figure=build_parameter_heatmap(), config={"displayModeBar": False})]),
        ]),
    ])


def build_pollution_chart():
    selected = ["Sewage", "Drainage", "Effluent", "Sea Water", "River", "Lake", "Bay", "Marine"]
    rows = [r for r in WATERBODY_ROWS if r["type"] in selected]
    x = [r["type"] for r in rows]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=[r["dbo"] for r in rows],
        mode="lines+markers",
        name="DBO",
        line=dict(color="#3fffe7", width=2.5, shape="spline"),
        marker=dict(size=8, color="#3fffe7", line=dict(color="#011a18", width=2)),
        hovertemplate="<b>%{x}</b><br>DBO média: %{y:.2f} mg/L<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=x,
        y=[r["ammonia"] for r in rows],
        mode="lines+markers",
        name="Amônia",
        line=dict(color="#ffd580", width=2.2, shape="spline"),
        marker=dict(size=8, color="#ffd580", line=dict(color="#011a18", width=2)),
        hovertemplate="<b>%{x}</b><br>Amônia média: %{y:.2f} mg/L<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text="Sinais médios de carga orgânica e amoniacal", font=dict(family="Syne, sans-serif", size=15, color="#f4fffe"), x=0),
        height=390,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#d8f5f1")),
    )
    fig.update_xaxes(tickangle=-25)
    return fig


def _waterbody_table():
    header = html.Tr(children=[
        html.Th("Corpo hídrico"), html.Th("Registros"), html.Th("%"), html.Th("CCME médio"), html.Th("DBO média"), html.Th("Amônia média"), html.Th("Leitura analítica"),
    ])
    rows = []
    for r in WATERBODY_ROWS:
        rows.append(html.Tr(children=[
            html.Td(r["type"]),
            html.Td(_fmt_int(r["count"])),
            html.Td(f"{r['percent']:.2f}%"),
            html.Td(f"{r['ccme']:.2f}"),
            html.Td(f"{r['dbo']:.2f}"),
            html.Td(f"{r['ammonia']:.2f}"),
            html.Td(r["note"]),
        ]))
    return html.Div(className="country-table-wrap", children=[
        html.Table(className="country-table", children=[html.Thead(header), html.Tbody(rows)])
    ])


def make_waterbody_pollution_section():
    return html.Section(className="eda-section eda-section-alt", children=[
        html.Div(className="eda-section-header", children=[
            html.Span("Carga Poluente", className="section-label"),
            html.H2("DBO, Amônia e Leitura Ambiental", className="section-title"),
            html.P("Sewage, Drainage e Effluent aparecem como grupos de maior atenção por concentrarem sinais médios de carga orgânica e amoniacal mais elevados.", className="section-sub"),
        ]),
        html.Div(className="eda-charts-grid", children=[
            html.Div(className="eda-chart-card eda-chart-wide", children=[dcc.Graph(figure=build_pollution_chart(), config={"displayModeBar": False})]),
        ]),
        html.Div(style={"maxWidth": "1200px", "margin": "22px auto 0"}, children=[_waterbody_table()]),
    ])


def make_waterbody_context_sections():
    return html.Section(className="eda-section", children=[
        html.Div(className="eda-section-header", children=[
            html.Span("Interpretação", className="section-label"),
            html.H2("Como o tipo de corpo hídrico influencia a análise?", className="section-title"),
            html.P("Os parâmetros ambientais não devem ser interpretados fora do contexto hidrológico e ecológico de cada tipo de corpo hídrico.", className="section-sub"),
        ]),
        html.Div(className="eda-metrics-grid", children=[
            _metric_card("lucide:waves", "Rios", "Maior representatividade", "Como River domina a base, os padrões globais tendem a refletir fortemente o comportamento de rios.", True),
            _metric_card("lucide:factory", "Efluentes", "Maior pressão ambiental", "Effluent e Sewage concentram valores mais altos de DBO e amônia, indicando impacto orgânico.", True),
            _metric_card("lucide:landmark", "Lagos", "Qualidade média elevada", "Lake apresenta CCME médio alto, mas deve ser analisado considerando baixa renovação hídrica."),
            _metric_card("lucide:shuffle", "Ambientes mistos", "Mais heterogeneidade", "Estuarine, Sea Water e Transitional podem apresentar maior variação pela mistura continental e marinha."),
        ]),
        html.Div(className="eda-insight-card", style={"marginTop": "34px"}, children=[
            html.Div(className="eda-insight-header", children=[
                html.Div(className="eda-insight-icon", children=[ico("lucide:lightbulb", size=22)]),
                html.H3("Leitura principal da análise por corpo hídrico", className="eda-insight-title"),
            ]),
            html.P(
                "A análise por corpo hídrico mostra que o dataset é fortemente desbalanceado em direção a rios, enquanto tipos como Coastal, Transitional e Drainage têm menor representatividade. "
                "Além disso, categorias diretamente associadas a lançamento de efluentes — especialmente Sewage e Effluent — apresentam pior qualidade média e maiores sinais de carga orgânica. "
                "Essa diferença entre ecossistemas ajuda a explicar por que a modelagem ambiental é complexa: o mesmo parâmetro pode ter interpretações distintas dependendo do tipo de corpo hídrico.",
                className="eda-insight-body",
            ),
            html.Div(className="eda-insight-tags", children=[
                html.Span("River ≈ 65,5%", className="eda-insight-tag eda-insight-tag-teal"),
                html.Span("Effluent ≈ 21,3%", className="eda-insight-tag"),
                html.Span("Sewage: menor CCME", className="eda-insight-tag"),
                html.Span("Lake/Marine: alta qualidade média", className="eda-insight-tag"),
                html.Span("Impacto direto no ML", className="eda-insight-tag"),
            ]),
        ]),
    ])
