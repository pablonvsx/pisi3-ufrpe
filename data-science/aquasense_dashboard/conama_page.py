# ============================================================
#  AquaSense — CONAMA e Construção do Target | conama_page.py
# ============================================================

from dash import html, dcc
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

SELECTED_PARAMETERS = [
    ("pH", "pH (ph units)", "6,0 a 9,0", "Equilíbrio químico", "Avalia acidez/alcalinidade e estabilidade química da água."),
    ("OD", "Dissolved Oxygen (mg/l)", "≥ 5 mg/L", "Suporte à vida aquática", "Baixos valores indicam estresse ambiental e risco para a biota."),
    ("DBO", "Biochemical Oxygen Demand (mg/l)", "≤ 5 mg/L", "Carga orgânica", "Valores altos indicam maior consumo de oxigênio por decomposição orgânica."),
    ("Nitrato", "Nitrate (mg/l)", "≤ 10 mg/L", "Nutrientes", "Excesso pode indicar lixiviação agrícola e favorecer eutrofização."),
    ("Amônia", "Ammonia (mg/l)", "Variável conforme pH", "Contaminação nitrogenada", "Pode indicar efluentes domésticos/agropecuários e toxicidade para organismos."),
]

EXCLUDED_PARAMETERS = [
    ("Nitrogênio Total", "Não entrou diretamente porque o dataset já contém nitrato e amônia, indicadores nitrogenados mais específicos."),
    ("Ortofosfato", "Foi mantido como variável analítica relevante, mas não como regra principal do target por diferença normativa entre formas de fósforo."),
    ("Temperatura", "Foi tratada como variável contextual, pois influencia processos físico-químicos, mas não foi critério direto do rótulo inicial."),
]

PIPELINE_STEPS = [
    ("1", "EDA", "Compreensão das variáveis, distribuições, assimetrias e padrões do dataset."),
    ("2", "Validação", "Verificação da correspondência entre variáveis do dataset e parâmetros ambientais clássicos."),
    ("3", "CONAMA", "Adoção da Classe 2 da Resolução CONAMA 357/2005 como referência normativa."),
    ("4", "Score", "Cada parâmetro em conformidade recebe 1 ponto; fora do limite recebe 0."),
    ("5", "Target", "O score ambiental é convertido na variável supervisionada conama_status."),
    ("6", "ML", "Os modelos aprendem padrões associados às classes ambientais construídas."),
]

FOUR_CLASS_DIST = {
    "Excelente": 68.9,
    "Boa": 20.0,
    "Atenção": 8.9,
    "Crítica": 2.2,
}

THREE_CLASS_DIST = {
    "Adequada": 68.9,
    "Atenção": 28.9,
    "Crítica": 2.2,
}


def ico(icon_name, size=22, color="#3fffe7"):
    return DashIconify(icon=icon_name, width=size, height=size, color=color)


def _section_header(label, title, subtitle):
    return html.Div(className="eda-section-header", children=[
        html.Span(label, className="section-label"),
        html.H2(title, className="section-title"),
        html.P(subtitle, className="section-sub"),
    ])


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


def _glass_card(children, extra_class=""):
    return html.Div(className=f"conama-glass-card {extra_class}".strip(), children=children)


# ============================================================
#  FIGURES
# ============================================================

def build_target_distribution_chart():
    labels = list(THREE_CLASS_DIST.keys())
    values = list(THREE_CLASS_DIST.values())
    fig = go.Figure(go.Bar(
        x=labels,
        y=values,
        marker=dict(
            color=["#3fffe7", "#00c4ad", "#ffb86b"],
            line=dict(color="rgba(244,255,254,0.28)", width=1),
        ),
        text=[f"{v:.1f}%" for v in values],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>%{y:.1f}% das amostras<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(
            text="Distribuição do target conama_status — 3 classes",
            font=dict(family="Syne, sans-serif", size=13, color="#f4fffe"),
            x=0,
        ),
        height=320,
        bargap=0.38,
    )
    fig.update_yaxes(title="Percentual (%)", range=[0, max(values) + 12])
    fig.update_xaxes(title="Classe ambiental")
    return fig


def build_score_mapping_chart():
    scores = [0, 1, 2, 3, 4, 5]
    labels = ["Crítica", "Crítica", "Crítica", "Atenção", "Atenção", "Adequada"]
    colors = ["#ff7f7f", "#ff7f7f", "#ff7f7f", "#00c4ad", "#00c4ad", "#3fffe7"]
    fig = go.Figure(go.Bar(
        x=[str(s) for s in scores],
        y=[1 for _ in scores],
        marker=dict(color=colors, line=dict(color="rgba(244,255,254,0.18)", width=1)),
        text=labels,
        textposition="inside",
        insidetextfont=dict(color="#011a18", size=12),
        hovertemplate="<b>Score %{x}</b><br>Classificação: %{text}<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(
            text="Conversão do score ambiental em classe supervisionada",
            font=dict(family="Syne, sans-serif", size=13, color="#f4fffe"),
            x=0,
        ),
        height=260,
        bargap=0.16,
    )
    fig.update_yaxes(showticklabels=False, showgrid=False, title="")
    fig.update_xaxes(title="Pontuação de conformidade CONAMA")
    return fig


def build_four_vs_three_chart():
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(FOUR_CLASS_DIST.keys()),
        y=list(FOUR_CLASS_DIST.values()),
        name="4 classes",
        marker=dict(color="rgba(63,255,231,0.52)", line=dict(color="rgba(63,255,231,0.28)", width=1)),
        hovertemplate="<b>%{x}</b><br>4 classes: %{y:.1f}%<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=list(THREE_CLASS_DIST.keys()),
        y=list(THREE_CLASS_DIST.values()),
        name="3 classes",
        marker=dict(color="rgba(0,196,173,0.72)", line=dict(color="rgba(63,255,231,0.28)", width=1)),
        hovertemplate="<b>%{x}</b><br>3 classes: %{y:.1f}%<extra></extra>",
    ))
    layout = dict(CHART_LAYOUT)
    layout.pop("showlegend", None)
    fig.update_layout(**layout)
    fig.update_layout(
        title=dict(
            text="4 classes vs 3 classes — redução de granularidade",
            font=dict(family="Syne, sans-serif", size=13, color="#f4fffe"),
            x=0,
        ),
        height=340,
        barmode="group",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#d8f5f1")),
    )
    fig.update_yaxes(title="Percentual (%)")
    fig.update_xaxes(title="Classes")
    return fig


def build_parameter_radar():
    categories = [p[0] for p in SELECTED_PARAMETERS]
    relevance = [0.88, 0.95, 0.90, 0.82, 0.84]
    categories_closed = categories + [categories[0]]
    relevance_closed = relevance + [relevance[0]]
    fig = go.Figure(go.Scatterpolar(
        r=relevance_closed,
        theta=categories_closed,
        fill="toself",
        line=dict(color="#3fffe7", width=2),
        marker=dict(color="#3fffe7", size=5),
        fillcolor="rgba(63,255,231,0.16)",
        hovertemplate="<b>%{theta}</b><br>Relevância metodológica: %{r:.2f}<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color="#d8f5f1"),
        margin=dict(l=24, r=24, t=52, b=24),
        height=380,
        showlegend=False,
        title=dict(
            text="Cobertura ambiental dos parâmetros do target",
            font=dict(family="Syne, sans-serif", size=13, color="#f4fffe"),
            x=0,
        ),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(63,255,231,0.12)", tickfont=dict(color="rgba(212,245,241,0.45)", size=9)),
            angularaxis=dict(gridcolor="rgba(63,255,231,0.12)", tickfont=dict(color="rgba(212,245,241,0.78)", size=11)),
        ),
    )
    return fig


# ============================================================
#  PAGE SECTIONS
# ============================================================

def make_conama_hero():
    return html.Section(className="var-hero conama-hero", children=[
        html.Div(className="hero-bg"),
        html.Div(className="hero-grid"),
        html.Div(className="orb orb-1"),
        html.Div(className="orb orb-2"),
        html.Div(className="var-hero-content", children=[
            html.Div(className="hero-badge", style={"marginBottom": "24px"}, children=[
                html.Span(className="hero-badge-dot"),
                "CONAMA 357/2005 • Target Supervisionado",
            ]),
            html.H1(className="var-hero-title", children=[
                "CONAMA e Construção do ",
                html.Span("Target", className="hero-title-teal"),
            ]),
            html.P("Como transformamos critérios ambientais em uma variável alvo interpretável para Machine Learning.", className="var-hero-sub"),
            html.P(
                "Esta seção conta a história metodológica do AquaSense: primeiro entendemos o dataset pela EDA, depois validamos quais parâmetros tinham sentido ambiental, usamos a CONAMA como referência normativa e, por fim, criamos o conama_status para treinar modelos supervisionados.",
                className="var-hero-body",
            ),
        ]),
    ])


def make_conama_metrics():
    return html.Section(className="eda-section", children=[
        html.Div(className="eda-metrics-grid", children=[
            _metric_card("lucide:scale", "CONAMA", "Base normativa", "Referência brasileira para enquadramento e qualidade das águas."),
            _metric_card("lucide:flask-conical", "5", "Parâmetros diretos", "pH, OD, DBO, Nitrato e Amônia usados na regra inicial.", True),
            _metric_card("lucide:binary", "0–5", "Score ambiental", "Pontuação construída pela quantidade de critérios atendidos."),
            _metric_card("lucide:target", "3 classes", "Target final", "Adequada, Atenção e Crítica para reduzir ambiguidade operacional."),
        ]),
    ])


def make_conama_story_section():
    return html.Section(className="eda-section eda-section-alt", children=[
        _section_header(
            "Narrativa Metodológica",
            "Por que construir um rótulo próprio?",
            "O dataset possuía indicadores ambientais, mas não trazia uma classificação diretamente alinhada ao contexto brasileiro do AquaSense.",
        ),
        html.Div(className="conama-story-grid", children=[
            _glass_card([
                html.Div(className="conama-card-icon", children=[ico("lucide:database")]),
                html.H3("O problema inicial"),
                html.P("Para aplicar Machine Learning supervisionado, era necessário criar uma variável alvo. O dataset continha parâmetros físico-químicos e o índice CCME, mas o objetivo do AquaSense era trabalhar com uma referência ambiental brasileira."),
            ]),
            _glass_card([
                html.Div(className="conama-card-icon", children=[ico("lucide:landmark")]),
                html.H3("A ponte normativa"),
                html.P("A CONAMA 357/2005 entrou como referência para conectar os dados analisados à realidade nacional, permitindo transformar limites ambientais em uma classificação interpretável."),
            ]),
            _glass_card([
                html.Div(className="conama-card-icon", children=[ico("lucide:cpu")]),
                html.H3("A etapa preditiva"),
                html.P("Depois da construção do rótulo, os modelos passaram a aprender padrões associados à qualidade da água, indo além de uma checagem isolada por regra fixa."),
            ]),
        ]),
    ])


def make_conama_pipeline_section():
    return html.Section(className="eda-section", children=[
        _section_header(
            "Fluxo de Construção",
            "Da EDA ao Machine Learning",
            "O target não surgiu de forma automática: ele foi resultado de uma sequência metodológica pensada para manter coerência ambiental e utilidade preditiva.",
        ),
        html.Div(className="conama-pipeline", children=[
            html.Div(className="conama-pipeline-step", children=[
                html.Div(className="conama-pipeline-num", children=num),
                html.H4(title),
                html.P(desc),
            ]) for num, title, desc in PIPELINE_STEPS
        ]),
    ])


def make_conama_parameters_section():
    return html.Section(className="eda-section eda-section-alt", children=[
        _section_header(
            "Parâmetros Selecionados",
            "As variáveis que formam o rótulo",
            "A seleção priorizou parâmetros com correspondência ambiental clara, unidade compatível e relevância para avaliação de qualidade da água.",
        ),
        html.Div(className="conama-param-layout", children=[
            html.Div(className="conama-param-grid", children=[
                _glass_card([
                    html.Div(className="conama-param-top", children=[
                        html.H3(name),
                        html.Span(limit),
                    ]),
                    html.Div(className="conama-param-code", children=column),
                    html.H4(dimension),
                    html.P(desc),
                ], "conama-param-card")
                for name, column, limit, dimension, desc in SELECTED_PARAMETERS
            ]),
            _glass_card([
                dcc.Graph(figure=build_parameter_radar(), config={"displayModeBar": False}),
            ], "conama-chart-card"),
        ]),
    ])


def make_conama_threshold_table_section():
    rows = []
    for name, column, limit, dimension, desc in SELECTED_PARAMETERS:
        rows.append(html.Tr(children=[
            html.Td(name),
            html.Td(column),
            html.Td(limit),
            html.Td(dimension),
            html.Td(desc),
        ]))
    return html.Section(className="eda-section", children=[
        _section_header(
            "Critérios Computacionais",
            "Como a regra normativa virou score ambiental",
            "Cada parâmetro foi avaliado como conforme ou não conforme. O somatório desses critérios formou um score de 0 a 5.",
        ),
        html.Div(className="conama-two-col", children=[
            _glass_card([
                html.Div(className="conama-table-wrap", children=[
                    html.Table(className="conama-table", children=[
                        html.Thead(html.Tr([html.Th("Parâmetro"), html.Th("Coluna"), html.Th("Limite"), html.Th("Dimensão"), html.Th("Interpretação") ])),
                        html.Tbody(rows),
                    ])
                ])
            ], "conama-table-card"),
            _glass_card([
                dcc.Graph(figure=build_score_mapping_chart(), config={"displayModeBar": False}),
                html.P("A classificação final não foi binária. O score permitiu representar diferentes níveis de conformidade ambiental, preservando mais informação para a modelagem supervisionada.", className="conama-note"),
            ], "conama-chart-card"),
        ]),
    ])


def make_conama_ifelse_ml_section():
    return html.Section(className="eda-section eda-section-alt", children=[
        _section_header(
            "Regra fixa vs Aprendizado",
            "Por que não apenas if/else?",
            "A CONAMA define referências, mas o Machine Learning aprende padrões conjuntos entre variáveis ambientais e ajuda a generalizar para novas amostras.",
        ),
        html.Div(className="conama-compare-grid", children=[
            _glass_card([
                html.Div(className="conama-card-icon danger", children=[ico("lucide:braces", color="#ffb86b")]),
                html.H3("Automação por regra fixa"),
                html.Ul([
                    html.Li("Verifica limites de forma direta."),
                    html.Li("Funciona bem para decisões simples e isoladas."),
                    html.Li("Fica rígida quando muitas variáveis interagem."),
                    html.Li("Não aprende padrões estatísticos do histórico."),
                ]),
                html.Code("if DBO > limite: status = 'Crítica'"),
            ], "conama-compare-card"),
            _glass_card([
                html.Div(className="conama-card-icon", children=[ico("carbon:machine-learning")]),
                html.H3("Machine Learning supervisionado"),
                html.Ul([
                    html.Li("Aprende combinações entre parâmetros."),
                    html.Li("Lida melhor com padrões não lineares."),
                    html.Li("Ajuda a classificar novas amostras."),
                    html.Li("Apoia decisão sem substituir o especialista."),
                ]),
                html.Code("modelo.fit(X, conama_status)"),
            ], "conama-compare-card highlight"),
        ]),
        html.Div(className="conama-thesis", children=[
            html.Span("Ideia central"),
            html.P("O ML não substitui a CONAMA. Ele usa a classificação inspirada nela como base para aprender padrões ambientais mais amplos e complexos."),
        ]),
    ])


def make_conama_distribution_section():
    return html.Section(className="eda-section", children=[
        _section_header(
            "Distribuição do Target",
            "O rótulo também revelou desbalanceamento",
            "Assim como em muitos problemas ambientais, condições críticas aparecem em menor frequência. Por isso, métricas como recall ganharam importância nos experimentos.",
        ),
        html.Div(className="conama-two-col", children=[
            _glass_card([
                dcc.Graph(figure=build_target_distribution_chart(), config={"displayModeBar": False}),
            ], "conama-chart-card"),
            _glass_card([
                dcc.Graph(figure=build_four_vs_three_chart(), config={"displayModeBar": False}),
            ], "conama-chart-card"),
        ]),
        html.Div(className="conama-insight-row", children=[
            _glass_card([
                html.H3("Por que 3 classes?"),
                html.P("A versão com menos categorias reduziu ambiguidades entre faixas intermediárias, deixando o problema mais estável para os modelos e facilitando a separabilidade estatística."),
            ]),
            _glass_card([
                html.H3("Por que olhar além da acurácia?"),
                html.P("Como a classe crítica é menos frequente, um modelo poderia obter boa acurácia global e ainda falhar justamente nos casos ambientais mais sensíveis."),
            ]),
        ]),
    ])


def make_conama_excluded_section():
    return html.Section(className="eda-section eda-section-alt", children=[
        _section_header(
            "Decisões Metodológicas",
            "Variáveis importantes que não entraram diretamente no target",
            "Nem toda variável ambiental relevante precisa virar regra do rótulo. Algumas foram mantidas para análise, correlação, clusterização e modelagem preditiva.",
        ),
        html.Div(className="conama-story-grid", children=[
            _glass_card([
                html.Div(className="conama-card-icon", children=[ico("lucide:minus-circle")]),
                html.H3(name),
                html.P(reason),
            ]) for name, reason in EXCLUDED_PARAMETERS
        ]),
    ])


def make_conama_ml_impact_section():
    return html.Section(className="eda-section", children=[
        _section_header(
            "Papel no AquaSense",
            "Como o target sustenta o pipeline de ML",
            "A construção do conama_status conecta regulamentação ambiental, interpretação científica e modelagem preditiva.",
        ),
        html.Div(className="conama-impact-grid", children=[
            _glass_card([
                html.Div(className="conama-card-icon", children=[ico("lucide:tag")]),
                html.H3("Variável alvo"),
                html.P("O conama_status passa a ser aquilo que os modelos supervisionados tentam prever a partir das variáveis ambientais."),
            ]),
            _glass_card([
                html.Div(className="conama-card-icon", children=[ico("lucide:bar-chart-3")]),
                html.H3("Comparação experimental"),
                html.P("Com o target definido, foi possível comparar algoritmos, métricas, balanceamento e impacto das variáveis nos resultados."),
            ]),
            _glass_card([
                html.Div(className="conama-card-icon", children=[ico("lucide:layout-dashboard")]),
                html.H3("Dashboard"),
                html.P("A classificação torna os resultados mais comunicáveis e permite transformar a análise em apoio visual à decisão ambiental."),
            ]),
            _glass_card([
                html.Div(className="conama-card-icon", children=[ico("lucide:shield-alert")]),
                html.H3("Apoio, não substituição"),
                html.P("O AquaSense não substitui avaliação técnica; ele organiza evidências e sinaliza padrões de risco para apoiar interpretação humana."),
            ]),
        ]),
    ])


def make_conama_final_note():
    return html.Section(className="eda-section eda-section-nav", children=[
        html.Div(className="conama-final-panel", children=[
            html.Span("Síntese"),
            html.H2("O target é o elo entre norma ambiental e inteligência computacional."),
            html.P("A EDA revelou o comportamento dos dados; a CONAMA forneceu referência ambiental; o score traduziu essa referência em lógica computacional; e o Machine Learning passou a aprender padrões associados à qualidade da água. Essa é a base metodológica que sustenta a etapa preditiva do AquaSense."),
        ]),
    ])
