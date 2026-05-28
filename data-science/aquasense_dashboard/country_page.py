# ============================================================
#  AquaSense — Análise por País | country_page.py
# ============================================================

from dash import html, dcc
from dash_iconify import DashIconify
import plotly.graph_objects as go


TEAL_PALETTE = ["#3fffe7", "#00e0ca", "#00c4ad", "#00a893", "#008c7a"]

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

COUNTRY_ROWS = [
    {"country": "England", "count": 2129198, "percent": 75.29, "start": 2000, "end": 2023, "coverage": "Contínua", "sampling": "Alta", "note": "Predominância absoluta no dataset; maior influência sobre padrões globais."},
    {"country": "USA", "count": 413814, "percent": 14.63, "start": 1940, "end": 2023, "coverage": "Contínua", "sampling": "Alta", "note": "Longa cobertura temporal e boa representatividade para séries históricas."},
    {"country": "Ireland", "count": 235019, "percent": 8.31, "start": 1940, "end": 2023, "coverage": "Com lacunas", "sampling": "Irregular", "note": "Intervalo amplo, mas com lacunas temporais; exige cautela em tendências."},
    {"country": "China", "count": 45997, "percent": 1.63, "start": 2001, "end": 2017, "coverage": "Contínua", "sampling": "Moderada", "note": "Período mais recente e menor amplitude temporal em relação aos demais países."},
    {"country": "Canada", "count": 3949, "percent": 0.14, "start": 1968, "end": 2021, "coverage": "Contínua", "sampling": "Baixa", "note": "Menor representatividade; alguns anos possuem pouquíssimos registros."},
]

LOW_SAMPLE_NOTES = [
    ("Canada", "1968–1975 e 2014–2017", "anos com menos de 10 registros em partes do intervalo"),
    ("Ireland", "1940–2023", "maior presença de lacunas temporais dentro do período observado"),
    ("England", "2000–2023", "cobertura contínua e sem baixa amostragem relevante"),
    ("China", "2001–2017", "cobertura contínua no intervalo, porém período mais curto"),
    ("USA", "1940–2023", "cobertura contínua e amplitude histórica elevada"),
]


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


def make_country_hero():
    return html.Section(className="var-hero", children=[
        html.Div(className="hero-bg"),
        html.Div(className="hero-grid"),
        html.Div(className="orb orb-1"),
        html.Div(className="orb orb-2"),
        html.Div(className="var-hero-content", children=[
            html.Div(className="hero-badge", style={"marginBottom": "24px"}, children=[
                html.Span(className="hero-badge-dot"),
                "Geographic EDA • AquaSense",
            ]),
            html.H1(className="var-hero-title", children=[
                html.Span("Análise por ", className="hero-title-white"),
                html.Span("País", className="hero-title-teal"),
            ]),
            html.P("Distribuição geográfica, representatividade e cobertura temporal dos registros ambientais.", className="var-hero-sub"),
            html.P(
                "Esta seção avalia como os dados estão distribuídos entre China, Inglaterra, Irlanda, Canadá e Estados Unidos. "
                "O objetivo é identificar desbalanceamentos de representatividade, diferenças temporais e possíveis vieses que podem influenciar a EDA e os modelos de Machine Learning.",
                className="var-hero-body",
            ),
        ]),
    ])


def make_country_metrics():
    total = sum(r["count"] for r in COUNTRY_ROWS)
    max_country = max(COUNTRY_ROWS, key=lambda r: r["count"])
    min_country = min(COUNTRY_ROWS, key=lambda r: r["count"])
    return html.Section(className="eda-section", children=[
        html.Div(className="eda-section-header", children=[
            html.Span("Representatividade", className="section-label"),
            html.H2("Métricas Geográficas Principais", className="section-title"),
            html.P("Indicadores extraídos da análise por país para entender a distribuição espacial do dataset.", className="section-sub"),
        ]),
        html.Div(className="eda-metrics-grid", children=[
            _metric_card("lucide:database", _fmt_int(total), "Registros analisados", "Volume total considerado na distribuição por país."),
            _metric_card("lucide:globe-2", "5", "Países presentes", "China, England, Ireland, Canada e USA."),
            _metric_card("lucide:map-pin", max_country["country"], "Maior representatividade", f"{max_country['percent']:.2f}% dos registros estão concentrados nesse país.", True),
            _metric_card("lucide:alert-triangle", min_country["country"], "Menor representatividade", f"Apenas {min_country['percent']:.2f}% dos registros, exigindo cautela comparativa.", True),
            _metric_card("lucide:calendar-range", "1940–2023", "Maior amplitude temporal", "Ireland e USA possuem o intervalo histórico mais amplo."),
            _metric_card("lucide:activity", "Desbalanceado", "Distribuição amostral", "A predominância da Inglaterra pode influenciar análises globais."),
        ]),
    ])


def build_country_count_chart():
    countries = [r["country"] for r in COUNTRY_ROWS]
    counts = [r["count"] for r in COUNTRY_ROWS]
    pct = [r["percent"] for r in COUNTRY_ROWS]
    fig = go.Figure(go.Bar(
        x=countries,
        y=counts,
        customdata=pct,
        marker=dict(color=TEAL_PALETTE, line=dict(color="rgba(63,255,231,0.32)", width=1)),
        hovertemplate="<b>%{x}</b><br>%{y:,.0f} registros<br>%{customdata:.2f}% do dataset<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text="Contagem de amostras por país", font=dict(family="Syne, sans-serif", size=15, color="#f4fffe"), x=0),
        height=360,
        yaxis_title="Número de registros",
    )
    return fig


def build_country_share_chart():
    countries = [r["country"] for r in COUNTRY_ROWS]
    pct = [r["percent"] for r in COUNTRY_ROWS]
    fig = go.Figure(go.Pie(
        labels=countries,
        values=pct,
        hole=0.62,
        marker=dict(colors=TEAL_PALETTE, line=dict(color="rgba(1,26,24,0.95)", width=2)),
        textinfo="label+percent",
        textfont=dict(color="#f4fffe", size=11),
        hovertemplate="<b>%{label}</b><br>%{value:.2f}% dos registros<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color="#d8f5f1"),
        margin=dict(l=12, r=12, t=42, b=12),
        title=dict(text="Participação percentual", font=dict(family="Syne, sans-serif", size=15, color="#f4fffe"), x=0),
        height=360,
        showlegend=False,
        annotations=[dict(text="Países", x=0.5, y=0.5, showarrow=False, font=dict(size=16, color="#3fffe7", family="Syne"))],
    )
    return fig


def make_country_distribution_section():
    return html.Section(className="eda-section eda-section-alt", children=[
        html.Div(className="eda-section-header", children=[
            html.Span("Distribuição", className="section-label"),
            html.H2("Desbalanceamento entre Países", className="section-title"),
            html.P("A distribuição geográfica não é equilibrada: a Inglaterra domina o dataset, seguida por USA e Ireland.", className="section-sub"),
        ]),
        html.Div(className="eda-charts-grid", children=[
            html.Div(className="eda-chart-card", children=[dcc.Graph(figure=build_country_count_chart(), config={"displayModeBar": False})]),
            html.Div(className="eda-chart-card", children=[dcc.Graph(figure=build_country_share_chart(), config={"displayModeBar": False})]),
        ]),
    ])


def build_temporal_range_chart():
    countries = [r["country"] for r in COUNTRY_ROWS]
    starts = [r["start"] for r in COUNTRY_ROWS]
    ends = [r["end"] for r in COUNTRY_ROWS]
    durations = [e - s for s, e in zip(starts, ends)]
    fig = go.Figure(go.Bar(
        x=durations,
        y=countries,
        base=starts,
        orientation="h",
        marker=dict(color=TEAL_PALETTE, line=dict(color="rgba(63,255,231,0.32)", width=1)),
        customdata=list(zip(starts, ends)),
        hovertemplate="<b>%{y}</b><br>Intervalo: %{customdata[0]}–%{customdata[1]}<br>Duração aproximada: %{x} anos<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text="Intervalo temporal por país", font=dict(family="Syne, sans-serif", size=15, color="#f4fffe"), x=0),
        height=370,
        xaxis_title="Ano",
        bargap=0.34,
    )
    fig.update_xaxes(range=[1938, 2025])
    return fig


def _country_table():
    header = html.Tr(children=[
        html.Th("País"), html.Th("Registros"), html.Th("%"), html.Th("Período"), html.Th("Cobertura"), html.Th("Leitura analítica"),
    ])
    rows = []
    for r in COUNTRY_ROWS:
        rows.append(html.Tr(children=[
            html.Td(r["country"]),
            html.Td(_fmt_int(r["count"])),
            html.Td(f"{r['percent']:.2f}%"),
            html.Td(f"{r['start']}–{r['end']}"),
            html.Td(r["coverage"]),
            html.Td(r["note"]),
        ]))
    return html.Div(className="country-table-wrap", children=[
        html.Table(className="country-table", children=[html.Thead(header), html.Tbody(rows)])
    ])


def make_country_temporal_section():
    return html.Section(className="eda-section", children=[
        html.Div(className="eda-section-header", children=[
            html.Span("Cobertura Temporal", className="section-label"),
            html.H2("Amplitude e Consistência dos Registros", className="section-title"),
            html.P("A amplitude temporal não garante continuidade ou volume suficiente: alguns países têm períodos longos, mas com lacunas ou baixa amostragem.", className="section-sub"),
        ]),
        html.Div(className="eda-charts-grid", children=[
            html.Div(className="eda-chart-card eda-chart-wide", children=[dcc.Graph(figure=build_temporal_range_chart(), config={"displayModeBar": False})]),
        ]),
        html.Div(style={"maxWidth": "1200px", "margin": "22px auto 0"}, children=[_country_table()]),
    ])


def make_country_quality_notes():
    return html.Section(className="eda-section eda-section-alt", children=[
        html.Div(className="eda-section-header", children=[
            html.Span("Lacunas e Cautelas", className="section-label"),
            html.H2("O que observar antes de comparar países?", className="section-title"),
            html.P("A comparação por país precisa considerar volume amostral, regularidade temporal e concentração de registros.", className="section-sub"),
        ]),
        html.Div(className="eda-metrics-grid", children=[
            _metric_card("lucide:shield-alert", "Viés geográfico", "Predomínio da Inglaterra", "Como England concentra cerca de 75% dos registros, análises globais podem refletir principalmente esse país.", True),
            _metric_card("lucide:calendar-x", "Lacunas temporais", "Cuidado com séries históricas", "Ireland possui amplitude longa, mas apresenta lacunas; Canadá tem anos com baixa amostragem."),
            _metric_card("lucide:scale", "Comparação justa", "Normalizar interpretação", "Países com poucos registros não devem ser interpretados com o mesmo peso estatístico dos países dominantes."),
            _metric_card("lucide:brain-circuit", "Impacto no ML", "Possível viés de aprendizagem", "Modelos podem aprender melhor os padrões dos países mais representados, exigindo avaliação cuidadosa."),
        ]),
    ])


def make_country_insight():
    return html.Section(className="eda-section", children=[
        html.Div(className="eda-insight-card", children=[
            html.Div(className="eda-insight-header", children=[
                html.Div(className="eda-insight-icon", children=[ico("lucide:lightbulb", size=22)]),
                html.H3("Leitura principal da análise por país", className="eda-insight-title"),
            ]),
            html.P(
                "A análise por país mostra que o dataset possui forte desbalanceamento geográfico. England concentra a maior parte das amostras, enquanto China e Canada possuem participação reduzida. "
                "Isso não invalida a base, mas exige cautela: padrões globais, distribuições e modelos podem refletir principalmente os países mais representados. Por isso, a EDA por país é essencial para contextualizar resultados e evitar interpretações equivocadas.",
                className="eda-insight-body",
            ),
            html.Div(className="eda-insight-tags", children=[
                html.Span("England ≈ 75%", className="eda-insight-tag eda-insight-tag-teal"),
                html.Span("USA ≈ 14,6%", className="eda-insight-tag"),
                html.Span("Ireland ≈ 8,3%", className="eda-insight-tag"),
                html.Span("China ≈ 1,6%", className="eda-insight-tag"),
                html.Span("Canada ≈ 0,14%", className="eda-insight-tag"),
            ]),
        ]),
    ])
