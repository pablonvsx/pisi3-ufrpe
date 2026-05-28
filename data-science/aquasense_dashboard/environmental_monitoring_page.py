from dash import html
from dash_iconify import DashIconify


def ico(name, size=24, color="#3fffe7"):
    return DashIconify(icon=name, width=size, height=size, color=color)


CARD = {
    "background": "rgba(0, 77, 72, 0.38)",
    "border": "1px solid rgba(63,255,231,0.18)",
    "borderRadius": "28px",
    "padding": "32px",
    "backdropFilter": "blur(14px)",
    "boxShadow": "0 18px 50px rgba(0,0,0,0.28)",
}

TEXT = {
    "color": "rgba(212,245,241,0.70)",
    "lineHeight": "1.8",
    "fontSize": "15px",
}


def section_title(label, title, desc=None):
    return html.Div(
        style={"maxWidth": "1050px", "margin": "0 auto 42px"},
        children=[
            html.Span(label, className="section-label"),
            html.H2(title, className="section-title"),
            html.P(desc, className="section-sub") if desc else None,
        ],
    )


def insight_card(icon, title, text):
    return html.Div(
        style=CARD,
        children=[
            html.Div(
                style={
                    "width": "48px",
                    "height": "48px",
                    "borderRadius": "14px",
                    "background": "rgba(63,255,231,0.09)",
                    "border": "1px solid rgba(63,255,231,0.20)",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "marginBottom": "22px",
                },
                children=[ico(icon)],
            ),
            html.H3(
                title,
                style={
                    "fontFamily": "Syne, sans-serif",
                    "fontSize": "19px",
                    "color": "#f4fffe",
                    "marginBottom": "12px",
                },
            ),
            html.P(text, style=TEXT),
        ],
    )


def pipeline_step(num, title, desc):
    return html.Div(
        style={
            **CARD,
            "padding": "26px",
            "position": "relative",
            "overflow": "hidden",
        },
        children=[
            html.Div(
                num,
                style={
                    "fontFamily": "Syne, sans-serif",
                    "fontSize": "28px",
                    "fontWeight": "800",
                    "color": "#3fffe7",
                    "marginBottom": "14px",
                },
            ),
            html.H4(
                title,
                style={
                    "fontFamily": "Syne, sans-serif",
                    "fontSize": "16px",
                    "color": "#f4fffe",
                    "marginBottom": "10px",
                },
            ),
            html.P(desc, style={**TEXT, "fontSize": "13px"}),
        ],
    )


def make_environmental_monitoring_page():
    return html.Div(
        id="root",
        className="var-root monitoring-root",
        children=[
            html.Section(
                className="eda-hero",
                children=[
                    html.Div(className="hero-bg"),
                    html.Div(className="hero-grid"),
                    html.Div(className="orb orb-1"),
                    html.Div(className="orb orb-2"),
                    html.Div(
                        className="eda-hero-content",
                        children=[
                            html.Div(
                                className="hero-badge",
                                children=[
                                    html.Span(className="hero-badge-dot"),
                                    "Síntese Final • AquaSense",
                                ],
                            ),
                            html.H1(
                                className="eda-hero-title",
                                children=[
                                    html.Span("Monitoramento ", className="hero-title-white"),
                                    html.Span("Ambiental", className="hero-title-teal"),
                                    html.Br(),
                                    html.Span("Inteligente", className="hero-title-white"),
                                ],
                            ),
                            html.P(
                                "Uma visão integrada dos principais resultados obtidos na EDA, na construção do target, na modelagem supervisionada e na clusterização.",
                                className="eda-hero-sub",
                            ),
                            html.P(
                                "Esta seção fecha o dashboard mostrando como os resultados analíticos do AquaSense podem apoiar a leitura ambiental, a priorização de riscos e a tomada de decisão baseada em dados.",
                                className="eda-hero-body",
                            ),
                        ],
                    ),
                ],
            ),

            html.Section(
                className="eda-section",
                children=[
                    section_title(
                        "Leitura Integrada",
                        "O que o AquaSense revelou?",
                        "A análise mostrou que a qualidade da água não pode ser entendida por um único parâmetro isolado, mas sim pela combinação entre variáveis físico-químicas, contexto ambiental e padrões estatísticos.",
                    ),
                    html.Div(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(3, 1fr)",
                            "gap": "24px",
                            "maxWidth": "1200px",
                            "margin": "0 auto",
                        },
                        children=[
                            insight_card(
                                "lucide:activity",
                                "Variabilidade Ambiental",
                                "Os dados apresentaram forte dispersão, assimetrias e valores extremos, indicando que eventos críticos podem aparecer de forma concentrada e pontual.",
                            ),
                            insight_card(
                                "lucide:alert-triangle",
                                "Outliers com Significado",
                                "Nem todo valor extremo deve ser tratado como erro. Em dados ambientais, outliers podem representar eventos reais de poluição, descarga orgânica ou alteração química.",
                            ),
                            insight_card(
                                "lucide:layers",
                                "Padrões por Contexto",
                                "Países e tipos de corpos hídricos apresentaram comportamentos distintos, reforçando a importância de análises segmentadas.",
                            ),
                        ],
                    ),
                ],
            ),

            html.Section(
                className="eda-section eda-section-alt",
                children=[
                    section_title(
                        "Machine Learning",
                        "Principais conclusões dos modelos",
                        "Os modelos supervisionados não foram avaliados apenas por acurácia. A análise considerou recall crítico, macro F1, precisão e comportamento por classe.",
                    ),
                    html.Div(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(2, 1fr)",
                            "gap": "24px",
                            "maxWidth": "1200px",
                            "margin": "0 auto",
                        },
                        children=[
                            insight_card(
                                "lucide:git-merge",
                                "SVM como modelo equilibrado",
                                "O SVM apresentou bom equilíbrio geral entre desempenho global e identificação da classe crítica, sendo uma opção robusta dentro da comparação realizada.",
                            ),
                            insight_card(
                                "lucide:trees",
                                "Random Forest e classe crítica",
                                "Apesar de boa acurácia, o Random Forest teve baixo recall na classe crítica, evidenciando o risco de avaliar o modelo apenas por acertos globais.",
                            ),
                            insight_card(
                                "lucide:target",
                                "Recall crítico como prioridade",
                                "No contexto ambiental, falsos negativos críticos são especialmente perigosos, pois significam deixar passar uma condição de risco como se fosse segura.",
                            ),
                            insight_card(
                                "lucide:bar-chart-3",
                                "Trade-off entre métricas",
                                "Modelos com maior recall podem gerar mais falsos alarmes, enquanto modelos mais precisos podem deixar passar casos críticos. O valor está no equilíbrio.",
                            ),
                        ],
                    ),
                ],
            ),

            html.Section(
                className="eda-section",
                children=[
                    section_title(
                        "Fluxo Analítico",
                        "Da medição ao apoio à decisão",
                        "O AquaSense organiza a análise em uma sequência lógica, conectando dados brutos, critérios ambientais, modelos e interpretação final.",
                    ),
                    html.Div(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(4, 1fr)",
                            "gap": "18px",
                            "maxWidth": "1200px",
                            "margin": "0 auto",
                        },
                        children=[
                            pipeline_step("01", "EDA", "Compreensão das distribuições, outliers, correlações e padrões iniciais."),
                            pipeline_step("02", "CONAMA", "Uso de referência normativa para apoiar a construção do rótulo ambiental."),
                            pipeline_step("03", "ML", "Treinamento de modelos supervisionados e análise de métricas por classe."),
                            pipeline_step("04", "Monitoramento", "Transformação dos resultados em leitura estratégica para decisão ambiental."),
                        ],
                    ),
                ],
            ),

            html.Section(
                className="eda-section eda-section-alt",
                children=[
                    section_title(
                        "Aplicação Prática",
                        "Como esses resultados podem ser usados?",
                        "O AquaSense atua como uma ferramenta de apoio: ele não substitui especialistas, mas ajuda a organizar evidências, priorizar alertas e facilitar a interpretação dos dados.",
                    ),
                    html.Div(
                        style={
                            **CARD,
                            "maxWidth": "1100px",
                            "margin": "0 auto",
                        },
                        children=[
                            html.H3(
                                "Síntese operacional",
                                style={
                                    "fontFamily": "Syne, sans-serif",
                                    "fontSize": "24px",
                                    "color": "#f4fffe",
                                    "marginBottom": "18px",
                                },
                            ),
                            html.P(
                                "Na prática, o sistema pode apoiar equipes técnicas na identificação de corpos hídricos com padrões de risco, na comparação entre regiões, na priorização de análises laboratoriais e na comunicação visual dos resultados para gestores e comunidades.",
                                style={**TEXT, "fontSize": "16px"},
                            ),
                            html.Div(
                                style={
                                    "display": "grid",
                                    "gridTemplateColumns": "repeat(3, 1fr)",
                                    "gap": "16px",
                                    "marginTop": "28px",
                                },
                                children=[
                                    html.Div("Priorização de risco", className="eda-insight-tag eda-insight-tag-teal"),
                                    html.Div("Apoio técnico", className="eda-insight-tag"),
                                    html.Div("Gestão ambiental", className="eda-insight-tag"),
                                    html.Div("Comunicação visual", className="eda-insight-tag"),
                                    html.Div("Monitoramento contínuo", className="eda-insight-tag"),
                                    html.Div("Decisão baseada em dados", className="eda-insight-tag eda-insight-tag-teal"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),

            html.Section(
                className="eda-section",
                children=[
                    html.Div(
                        style={
                            **CARD,
                            "maxWidth": "1180px",
                            "margin": "0 auto",
                            "textAlign": "center",
                            "padding": "48px",
                        },
                        children=[
                            html.Span("Conclusão", className="section-label"),
                            html.H2(
                                "Dados ambientais só geram valor quando viram interpretação.",
                                style={
                                    "fontFamily": "Syne, sans-serif",
                                    "fontSize": "38px",
                                    "color": "#f4fffe",
                                    "margin": "18px auto",
                                    "maxWidth": "900px",
                                },
                            ),
                            html.P(
                                "O AquaSense integra análise exploratória, critérios ambientais, aprendizado de máquina e visualização interativa para transformar medições de qualidade da água em conhecimento acessível e útil para o monitoramento ambiental.",
                                style={
                                    **TEXT,
                                    "fontSize": "17px",
                                    "maxWidth": "900px",
                                    "margin": "0 auto",
                                },
                            ),
                        ],
                    )
                ],
            ),
        ],
    )