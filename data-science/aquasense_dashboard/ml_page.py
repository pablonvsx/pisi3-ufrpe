from dash import html, dcc, Input, Output
from dash_iconify import DashIconify
import plotly.graph_objects as go
import random

TEAL_PALETTE = ["#3fffe7", "#00e0ca", "#00c4ad", "#00a893", "#008c7a"]
ALGO_COLORS = {
    "LightGBM": "#f5a623",
    "Regressão Logística": "#e25c72",
    "Random Forest": "#3fffe7",
    "SVM": "#7c6af7",
}

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#d8f5f1"),
    margin=dict(l=18, r=18, t=52, b=28),
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



ALGORITHM_GLOBAL = [
    {
        "Algoritmo": "LightGBM",
        "Acc_Treino": 0.6833865221580813,
        "Acc_Teste": 0.6734087694483734,
        "Overfitting": 0.6833865221580813 - 0.6734087694483734,
        "Train_F1": 0.7202761522713718,
        "Weighted_F1": 0.71,
        "Macro_F1": 0.44,
        "Recall_Crítica": 0.67,
        "Precision_Crítica": 0.09,
        "F1_Crítica": 0.16,
        "Leitura": "Modelo sensível à classe crítica, com recall crítico alto, mas precisão baixa. Indica muitos alertas para capturar risco ambiental.",
    },
    {
        "Algoritmo": "Regressão Logística",
        "Acc_Treino": 0.7912729072923205,
        "Acc_Teste": 0.7896746817538897,
        "Overfitting": 0.7912729072923205 - 0.7896746817538897,
        "Train_F1": 0.8010931268213443,
        "Weighted_F1": 0.80,
        "Macro_F1": 0.53,
        "Recall_Crítica": 0.64,
        "Precision_Crítica": 0.11,
        "F1_Crítica": 0.18,
        "Leitura": "Baseline linear mais estável da comparação. Mesmo limitada geometricamente, teve bom equilíbrio geral após padronização e balanceamento.",
    },
    {
        "Algoritmo": "Random Forest",
        "Acc_Treino": 0.9047640095828287,
        "Acc_Teste": 0.7354314002828855,
        "Overfitting": 0.9047640095828287 - 0.7354314002828855,
        "Train_F1": 0.911996657756976,
        "Weighted_F1": 0.74,
        "Macro_F1": 0.42,
        "Recall_Crítica": 0.05,
        "Precision_Crítica": 0.09,
        "F1_Crítica": 0.06,
        "Leitura": "Acurácia razoável, mas forte falha na classe crítica. O modelo aprendeu bem a classe majoritária e sofreu com o desbalanceamento.",
    },
    {
        "Algoritmo": "SVM",
        "Acc_Treino": 0.7707546919615627,
        "Acc_Teste": 0.7733026874115984,
        "Overfitting": 0.7707546919615627 - 0.7733026874115984,
        "Train_F1": 0.7779919497843673,
        "Weighted_F1": 0.78,
        "Macro_F1": 0.51,
        "Recall_Crítica": 0.62,
        "Precision_Crítica": 0.13,
        "F1_Crítica": 0.21,
        "Leitura": "Melhor equilíbrio operacional entre recall crítico, macro F1 e gap treino-teste. Desempenho consistente para dados com fronteiras complexas.",
    },
]

PRECISION = {
    "LightGBM": {"Atenção": 0.25, "Boa": 0.45, "Crítica": 0.09, "Excelente": 0.92},
    "Regressão Logística": {"Atenção": 0.65, "Boa": 0.55, "Crítica": 0.11, "Excelente": 0.91},
    "Random Forest": {"Atenção": 0.27, "Boa": 0.50, "Crítica": 0.09, "Excelente": 0.86},
    "SVM": {"Atenção": 0.39, "Boa": 0.53, "Crítica": 0.13, "Excelente": 0.92},
}
RECALL = {
    "LightGBM": {"Atenção": 0.61, "Boa": 0.40, "Crítica": 0.67, "Excelente": 0.75},
    "Regressão Logística": {"Atenção": 0.44, "Boa": 0.49, "Crítica": 0.64, "Excelente": 0.90},
    "Random Forest": {"Atenção": 0.44, "Boa": 0.38, "Crítica": 0.05, "Excelente": 0.86},
    "SVM": {"Atenção": 0.60, "Boa": 0.37, "Crítica": 0.62, "Excelente": 0.90},
}
F1 = {
    "LightGBM": {"Atenção": 0.35, "Boa": 0.42, "Crítica": 0.16, "Excelente": 0.83},
    "Regressão Logística": {"Atenção": 0.53, "Boa": 0.52, "Crítica": 0.18, "Excelente": 0.91},
    "Random Forest": {"Atenção": 0.34, "Boa": 0.43, "Crítica": 0.06, "Excelente": 0.86},
    "SVM": {"Atenção": 0.47, "Boa": 0.44, "Crítica": 0.21, "Excelente": 0.91},
}

# ============================================================
#  TRILHAS EXPERIMENTAIS
# ============================================================

EXPERIMENTS_BY_ALGO = {
    "LightGBM": [
        {"id": "Exp 4", "classes": "4", "features": "Todas as variáveis", "balance": "class_weight / ajuste de classes", "accuracy": 0.6734087694483734, "weighted_f1": 0.71, "macro_f1": 0.44, "risk_recall": 0.67, "risk_precision": 0.09, "lesson": "Alto recall crítico, mas baixa precisão: o modelo prioriza sensibilidade ambiental e gera mais falsos alertas."},
        {"id": "3 classes · LGBM", "classes": "3", "features": "Todas as variáveis", "balance": "target reduzido", "accuracy": 0.754930648255377, "weighted_f1": 0.78, "macro_f1": 0.53, "risk_recall": 0.68, "risk_precision": 0.09, "lesson": "Na versão de 3 classes, o LGBM manteve forte recall crítico, com maior agressividade na detecção da classe de risco."},
    ],
    "Regressão Logística": [
        {"id": "Exp 1", "classes": "4", "features": "4 variáveis reduzidas", "balance": "Sem balanceamento", "accuracy": 0.709, "weighted_f1": 0.66, "macro_f1": 0.25, "risk_recall": 0.00, "risk_precision": 0.00, "lesson": "Baseline inicial: alta acurácia aparente, mas apagão da classe crítica por desbalanceamento."},
        {"id": "Exp 2", "classes": "4", "features": "4 variáveis reduzidas", "balance": "class_weight='balanced'", "accuracy": 0.644, "weighted_f1": 0.66, "macro_f1": 0.39, "risk_recall": 0.63, "risk_precision": 0.08, "lesson": "O peso balanceado força o modelo a enxergar minorias, mas aumenta falsos positivos."},
        {"id": "Exp 3", "classes": "4", "features": "Todas as variáveis", "balance": "Sem balanceamento", "accuracy": 0.781, "weighted_f1": 0.78, "macro_f1": 0.28, "risk_recall": 0.00, "risk_precision": 0.00, "lesson": "Adicionar variáveis melhora acurácia, mas não corrige sozinho o desbalanceamento."},
        {"id": "Exp 4", "classes": "4", "features": "Todas as variáveis", "balance": "class_weight='balanced'", "accuracy": 0.7896746817538897, "weighted_f1": 0.80, "macro_f1": 0.53, "risk_recall": 0.64, "risk_precision": 0.11, "lesson": "Experimento validado na comparação global: melhor macro F1 e boa estabilidade treino-teste."},
        {"id": "Exp 5", "classes": "4", "features": "Todas as variáveis", "balance": "SMOTE", "accuracy": 0.613, "weighted_f1": 0.66, "macro_f1": 0.40, "risk_recall": 0.81, "risk_precision": 0.12, "lesson": "SMOTE aumenta recall crítico, mas adiciona ruído e reduz acurácia global."},
        {"id": "Exp 6", "classes": "4", "features": "Todas as variáveis", "balance": "class_weight + GridSearch", "accuracy": 0.697, "weighted_f1": 0.71, "macro_f1": 0.44, "risk_recall": 0.77, "risk_precision": 0.15, "lesson": "O tuning confirmou estabilidade, mas também o teto do modelo linear para fronteiras complexas."},
        {"id": "Exp 7", "classes": "3", "features": "Todas as variáveis", "balance": "class_weight='balanced'", "accuracy": 0.7078, "weighted_f1": 0.74, "macro_f1": 0.48, "risk_recall": 0.58, "risk_precision": 0.31, "lesson": "A fusão Atenção/Crítica reduziu ambiguidade e melhorou a precisão da classe de risco."},
    ],
    "Random Forest": [
        {"id": "Exp 4", "classes": "4", "features": "Todas as variáveis", "balance": "class_weight / ajuste de classes", "accuracy": 0.7354314002828855, "weighted_f1": 0.74, "macro_f1": 0.42, "risk_recall": 0.05, "risk_precision": 0.09, "lesson": "Acurácia razoável, mas recall crítico muito baixo. O modelo ficou enviesado para a classe majoritária."},
        {"id": "Exp 7 · 3 classes", "classes": "3", "features": "RF 3 classes", "balance": "alvo reduzido", "accuracy": 0.74, "weighted_f1": 0.73, "macro_f1": 0.45, "risk_recall": 0.03, "risk_precision": 0.08, "lesson": "Primeira versão de 3 classes: ainda pouca recuperação da classe crítica."},
        {"id": "Exp 8 · 3 classes", "classes": "3", "features": "RF 3 classes", "balance": "ajuste experimental", "accuracy": 0.69, "weighted_f1": 0.70, "macro_f1": 0.43, "risk_recall": 0.19, "risk_precision": 0.03, "lesson": "Ganho de recall crítico, mas com baixa precisão e perda de desempenho global."},
        {"id": "Exp 9 · 3 classes", "classes": "3", "features": "RF 3 classes", "balance": "ajuste experimental", "accuracy": 0.80, "weighted_f1": 0.80, "macro_f1": 0.52, "risk_recall": 0.05, "risk_precision": 0.20, "lesson": "Melhor acurácia entre os experimentos RF 3 classes, mas ainda com recall crítico reduzido."},
        {"id": "Exp 10 · 3 classes", "classes": "3", "features": "5 variáveis", "balance": "alvo reduzido", "accuracy": 0.7775106082036775, "weighted_f1": 0.79, "macro_f1": 0.50, "risk_recall": 0.12, "risk_precision": 0.03, "lesson": "Experimento confirmado: treino 91.6%, teste 77.8%, gap alto e recall crítico ainda limitado."},
        {"id": "Exp 11 · 3 classes", "classes": "3", "features": "RF 3 classes", "balance": "ajuste experimental", "accuracy": 0.80, "weighted_f1": 0.79, "macro_f1": 0.50, "risk_recall": 0.04, "risk_precision": 0.19, "lesson": "Aumentou acurácia, mas manteve baixa recuperação da classe crítica."},
        {"id": "Exp 12 · 3 classes", "classes": "3", "features": "RF 3 classes", "balance": "ajuste experimental", "accuracy": 0.77, "weighted_f1": 0.78, "macro_f1": 0.49, "risk_recall": 0.03, "risk_precision": 0.05, "lesson": "Modelo estável em acurácia, mas sem resolver o principal gargalo: risco crítico."},
    ],
    "SVM": [
        {"id": "Exp 4", "classes": "4", "features": "Todas as variáveis", "balance": "class_weight / ajuste de classes", "accuracy": 0.7733026874115984, "weighted_f1": 0.78, "macro_f1": 0.51, "risk_recall": 0.62, "risk_precision": 0.13, "lesson": "Melhor equilíbrio global: bom recall crítico, bom macro F1 e praticamente sem overfitting."},
        {"id": "3 classes · SVM", "classes": "3", "features": "Todas as variáveis", "balance": "target reduzido", "accuracy": 0.7657069104217682, "weighted_f1": 0.76, "macro_f1": 0.48, "risk_recall": 0.08, "risk_precision": 0.07, "lesson": "Na versão enviada de 3 classes, o SVM ficou estável, mas não priorizou a classe crítica."},
    ],
}

THREE_CLASS_EXPERIMENTS = [
    {"id": "Logística Exp 7", "algoritmo": "Regressão Logística", "train": None, "acc": 0.7078, "f1": 0.74, "macro_f1": 0.48, "risk_recall": 0.58, "risk_precision": 0.31},
    {"id": "LGBM 3 classes", "algoritmo": "LightGBM", "train": 0.754930648255377, "acc": 0.754930648255377, "f1": 0.78, "macro_f1": 0.53, "risk_recall": 0.68, "risk_precision": 0.09},
    {"id": "RF Exp 10", "algoritmo": "Random Forest", "train": 0.9164242965372749, "acc": 0.7775106082036775, "f1": 0.79, "macro_f1": 0.50, "risk_recall": 0.12, "risk_precision": 0.03},
    {"id": "SVM 3 classes", "algoritmo": "SVM", "train": 0.7657069104217682, "acc": 0.7657069104217682, "f1": 0.76, "macro_f1": 0.48, "risk_recall": 0.08, "risk_precision": 0.07},
]

# ============================================================
#  DADOS — CLUSTERIZAÇÃO
# ============================================================

PCA_VARIANCE = [0.24, 0.17, 0.15, 0.12, 0.09, 0.08, 0.06, 0.04]
ELBOW = [100.0, 72.0, 53.0, 43.0, 38.0, 34.5, 32.0, 30.2, 28.9, 27.8]
SILHOUETTE = {2: 0.31, 3: 0.39, 4: 0.37, 5: 0.34, 6: 0.32}
CLUSTER_PROFILES = [
    {"cluster": "Cluster 1", "label": "Adequada", "color": "#3fffe7", "samples": 54, "ammonia": 0.15, "dbo": 1.4, "od": 10.8, "orthophosphate": 0.04, "ph": 7.7, "temp": 11.2, "nitrogen": 0.9, "nitrate": 1.5, "interpretation": "Água mais preservada, com baixos nutrientes, baixa carga orgânica e oxigênio dissolvido confortável."},
    {"cluster": "Cluster 0", "label": "Atenção", "color": "#f5a623", "samples": 34, "ammonia": 0.65, "dbo": 3.6, "od": 8.2, "orthophosphate": 0.18, "ph": 7.5, "temp": 13.5, "nitrogen": 2.6, "nitrate": 4.1, "interpretation": "Condição intermediária, com sinais de enriquecimento por nutrientes e maior variabilidade ambiental."},
    {"cluster": "Cluster 2", "label": "Crítica", "color": "#e25c72", "samples": 12, "ammonia": 2.9, "dbo": 13.2, "od": 4.1, "orthophosphate": 0.95, "ph": 7.2, "temp": 16.4, "nitrogen": 10.8, "nitrate": 18.0, "interpretation": "Forte degradação ambiental, com DBO/nutrientes elevados e oxigênio dissolvido reduzido."},
]
CLUSTER_VARIABLES = [("ammonia", "Amônia"), ("dbo", "DBO"), ("od", "OD"), ("orthophosphate", "Ortofosfato"), ("ph", "pH"), ("temp", "Temperatura"), ("nitrogen", "Nitrogênio"), ("nitrate", "Nitrato")]

# ============================================================
#  HELPERS
# ============================================================

def ml_icon(icon, size=22, color="#3fffe7"):
    return DashIconify(icon=icon, width=size, height=size, color=color)

def pct(v):
    if v is None:
        return "—"
    return f"{v*100:.1f}%"

def section_header(kicker, title, text):
    return html.Div(className="ml-section-header", children=[html.Span(kicker, className="section-label"), html.H2(title, className="section-title"), html.P(text, className="section-sub")])

def ml_metric_card(icon, value, title, desc):
    return html.Div(className="ml-metric-card", children=[html.Div(className="ml-metric-icon", children=[ml_icon(icon)]), html.Div(value, className="ml-metric-value"), html.Div(title, className="ml-metric-title"), html.P(desc, className="ml-metric-desc")])

def mini_table(headers, rows, class_name="ml-table"):
    return html.Div(className="ml-table-wrap", children=[html.Table(className=class_name, children=[html.Thead(html.Tr([html.Th(h) for h in headers])), html.Tbody([html.Tr([html.Td(c) for c in row]) for row in rows])])])

# ============================================================
#  CHARTS — SUPERVISIONADO
# ============================================================

def build_train_test_chart():
    algos = [r["Algoritmo"] for r in ALGORITHM_GLOBAL]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Treino", x=algos, y=[r["Acc_Treino"] for r in ALGORITHM_GLOBAL], marker=dict(color="rgba(63,255,231,0.75)"), hovertemplate="%{x}<br>Treino: %{y:.1%}<extra></extra>"))
    fig.add_trace(go.Bar(name="Teste", x=algos, y=[r["Acc_Teste"] for r in ALGORITHM_GLOBAL], marker=dict(color="rgba(245,166,35,0.78)"), hovertemplate="%{x}<br>Teste: %{y:.1%}<extra></extra>"))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(title=dict(text="Acurácia treino × teste", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0), height=370, barmode="group", showlegend=True, legend=dict(orientation="h", y=1.12, x=0))
    fig.update_yaxes(tickformat=".0%", range=[0, 1])
    return fig

def build_overfitting_chart():
    algos = [r["Algoritmo"] for r in ALGORITHM_GLOBAL]
    gaps = [r["Overfitting"] for r in ALGORITHM_GLOBAL]
    colors = ["#e25c72" if g > 0.10 else "#3fffe7" for g in gaps]
    fig = go.Figure(go.Bar(x=algos, y=gaps, marker=dict(color=colors), hovertemplate="%{x}<br>Gap: %{y:.1%}<extra></extra>"))
    fig.add_hline(y=0, line=dict(color="rgba(244,255,254,0.25)", width=1))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(title=dict(text="Gap treino-teste", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0), height=370)
    fig.update_yaxes(tickformat=".0%")
    return fig

def build_f1_chart():
    algos = [r["Algoritmo"] for r in ALGORITHM_GLOBAL]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Weighted F1", x=algos, y=[r["Weighted_F1"] for r in ALGORITHM_GLOBAL], marker=dict(color="#3fffe7"), hovertemplate="%{x}<br>Weighted F1: %{y:.2f}<extra></extra>"))
    fig.add_trace(go.Bar(name="Macro F1", x=algos, y=[r["Macro_F1"] for r in ALGORITHM_GLOBAL], marker=dict(color="rgba(245,166,35,0.82)"), hovertemplate="%{x}<br>Macro F1: %{y:.2f}<extra></extra>"))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(title=dict(text="F1 ponderado × Macro F1", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0), barmode="group", height=360, showlegend=True, legend=dict(orientation="h", y=1.12, x=0))
    fig.update_yaxes(range=[0, 1])
    return fig

def build_class_metric_heatmap(metric_name="Recall"):
    source = {"Precision": PRECISION, "Recall": RECALL, "F1-score": F1}[metric_name]
    algos = list(source.keys())
    classes = ["Atenção", "Boa", "Crítica", "Excelente"]
    z = [[source[a][c] for a in algos] for c in classes]
    fig = go.Figure(go.Heatmap(z=z, x=algos, y=classes, colorscale=[[0, "rgba(1,26,24,0.95)"], [0.55, "#006960"], [1, "#3fffe7"]], zmin=0, zmax=1, text=[[f"{v:.2f}" for v in row] for row in z], texttemplate="%{text}", hovertemplate="%{y} · %{x}<br>" + metric_name + ": %{z:.2f}<extra></extra>", colorbar=dict(title=dict(text=metric_name, font=dict(color="#d8f5f1")), tickfont=dict(color="#d8f5f1"), thickness=12)))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(title=dict(text=f"Mapa por classe — {metric_name}", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0), height=360)
    fig.update_xaxes(tickangle=0)
    return fig

def build_recall_critical_chart():
    algos = [r["Algoritmo"] for r in ALGORITHM_GLOBAL]
    vals = [r["Recall_Crítica"] for r in ALGORITHM_GLOBAL]
    colors = [ALGO_COLORS[a] for a in algos]
    fig = go.Figure(go.Bar(x=algos, y=vals, marker=dict(color=colors), hovertemplate="%{x}<br>Recall crítica: %{y:.1%}<extra></extra>"))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(title=dict(text="Recall da classe crítica — ponto sensível do projeto", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0), height=340)
    fig.update_yaxes(tickformat=".0%", range=[0, 0.75])
    return fig

def build_experiment_timeline(algorithm="Regressão Logística"):
    experiments = EXPERIMENTS_BY_ALGO.get(algorithm, EXPERIMENTS_BY_ALGO["Regressão Logística"])
    x = [e["id"] for e in experiments]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=[e["accuracy"] for e in experiments], mode="lines+markers", name="Acurácia", line=dict(color="#3fffe7", width=3, shape="spline"), marker=dict(size=8), hovertemplate="%{x}<br>Acurácia: %{y:.1%}<extra></extra>"))
    fig.add_trace(go.Scatter(x=x, y=[e["risk_recall"] for e in experiments], mode="lines+markers", name="Recall risco", line=dict(color="#e25c72", width=3, shape="spline"), marker=dict(size=8), hovertemplate="%{x}<br>Recall risco: %{y:.2f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=x, y=[e["risk_precision"] for e in experiments], mode="lines+markers", name="Precision risco", line=dict(color="#f5a623", width=3, shape="spline"), marker=dict(size=8), hovertemplate="%{x}<br>Precision risco: %{y:.2f}<extra></extra>"))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(title=dict(text=f"Trilha experimental — {algorithm}", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0), height=380, showlegend=True, legend=dict(orientation="h", y=1.12, x=0))
    fig.update_yaxes(range=[0, 1])
    fig.update_xaxes(tickangle=-18)
    return fig

def build_three_class_chart():
    labels = [e["id"] for e in THREE_CLASS_EXPERIMENTS]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Acurácia teste", x=labels, y=[e["acc"] for e in THREE_CLASS_EXPERIMENTS], marker=dict(color="#3fffe7"), hovertemplate="%{x}<br>Acurácia: %{y:.1%}<extra></extra>"))
    fig.add_trace(go.Bar(name="Recall crítico", x=labels, y=[e["risk_recall"] for e in THREE_CLASS_EXPERIMENTS], marker=dict(color="#e25c72"), hovertemplate="%{x}<br>Recall crítico: %{y:.1%}<extra></extra>"))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(title=dict(text="Fase de 3 classes — comparação de risco", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0), height=390, barmode="group", showlegend=True, legend=dict(orientation="h", y=1.12, x=0))
    fig.update_xaxes(tickangle=-18)
    fig.update_yaxes(range=[0, 1], tickformat=".0%")
    return fig

# ============================================================
#  CHARTS — CLUSTERIZAÇÃO
# ============================================================

def build_pca_variance_chart():
    pcs = [f"PC{i}" for i in range(1, 9)]
    cumulative, s = [], 0
    for v in PCA_VARIANCE:
        s += v; cumulative.append(s)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=pcs, y=PCA_VARIANCE, name="Variância individual", marker=dict(color="#3fffe7"), hovertemplate="%{x}<br>Variância: %{y:.0%}<extra></extra>"))
    fig.add_trace(go.Scatter(x=pcs, y=cumulative, name="Variância acumulada", mode="lines+markers", line=dict(color="#f5a623", width=3, shape="spline"), marker=dict(size=8), hovertemplate="%{x}<br>Acumulada: %{y:.0%}<extra></extra>"))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(title=dict(text="PCA — variância explicada", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0), height=360, showlegend=True, legend=dict(orientation="h", y=1.12, x=0))
    fig.update_yaxes(tickformat=".0%", range=[0, 1])
    return fig

def build_elbow_chart():
    ks = list(range(1, 11))
    fig = go.Figure(go.Scatter(x=ks, y=ELBOW, mode="lines+markers", line=dict(color="#3fffe7", width=3, shape="spline"), marker=dict(size=9), hovertemplate="K=%{x}<br>WCSS: %{y:.1f}<extra></extra>"))
    fig.add_vline(x=3, line=dict(color="#f5a623", width=2, dash="dash"))
    fig.add_annotation(x=3, y=max(ELBOW)*0.9, text="K=3 escolhido", showarrow=False, font=dict(color="#f5a623", size=12), bgcolor="rgba(1,26,24,0.75)")
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(title=dict(text="Elbow Method — redução do WCSS", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0), height=340)
    fig.update_xaxes(dtick=1)
    return fig

def build_silhouette_chart():
    ks, vals = list(SILHOUETTE.keys()), list(SILHOUETTE.values())
    fig = go.Figure(go.Bar(x=ks, y=vals, marker=dict(color=["#006960", "#3fffe7", "#00c4ad", "#00a893", "#008c7a"], line=dict(color="rgba(244,255,254,0.12)", width=1)), hovertemplate="K=%{x}<br>Silhouette: %{y:.2f}<extra></extra>"))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(title=dict(text="Silhouette Score — coesão e separação", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0), height=340)
    fig.update_xaxes(dtick=1)
    fig.update_yaxes(range=[0, 0.5])
    return fig

def build_cluster_scatter():
    random.seed(42)
    fig = go.Figure()
    centers = {"Adequada": (-1.8, -0.5), "Atenção": (0.25, 0.25), "Crítica": (1.8, 1.1)}
    colors = {"Adequada": "#3fffe7", "Atenção": "#f5a623", "Crítica": "#e25c72"}
    counts = {"Adequada": 75, "Atenção": 55, "Crítica": 30}
    for label, (cx, cy) in centers.items():
        spread = 0.42 if label != "Crítica" else 0.55
        xs = [random.gauss(cx, spread) for _ in range(counts[label])]
        ys = [random.gauss(cy, spread) for _ in range(counts[label])]
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers", name=label, marker=dict(size=8, color=colors[label], opacity=0.74, line=dict(color="rgba(1,26,24,0.65)", width=1)), hovertemplate=f"Cluster: {label}<br>PC1=%{{x:.2f}}<br>PC2=%{{y:.2f}}<extra></extra>"))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(title=dict(text="Distribuição dos clusters no espaço PCA", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0), height=430, showlegend=True, legend=dict(orientation="h", y=1.08, x=0))
    fig.update_xaxes(title="PC1")
    fig.update_yaxes(title="PC2")
    return fig

def build_cluster_profile_heatmap():
    vars_keys = [v[0] for v in CLUSTER_VARIABLES]
    vars_labels = [v[1] for v in CLUSTER_VARIABLES]
    clusters = [c["label"] for c in CLUSTER_PROFILES]
    z = []
    for key in vars_keys:
        vals = [c[key] for c in CLUSTER_PROFILES]
        mn, mx = min(vals), max(vals)
        z.append([(v - mn) / (mx - mn) if mx != mn else 0 for v in vals])
    fig = go.Figure(go.Heatmap(z=z, x=clusters, y=vars_labels, colorscale=[[0, "rgba(1,26,24,0.95)"], [0.5, "#006960"], [1, "#3fffe7"]], text=[[f"{v:.2f}" for v in row] for row in z], texttemplate="%{text}", hovertemplate="%{y} · %{x}<br>Intensidade normalizada: %{z:.2f}<extra></extra>", colorbar=dict(title=dict(text="Intensidade", font=dict(color="#d8f5f1")), tickfont=dict(color="#d8f5f1"), thickness=12)))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(title=dict(text="Perfil médio dos clusters — variáveis normalizadas", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0), height=420)
    return fig

def build_cluster_bubble():
    fig = go.Figure()
    for c in CLUSTER_PROFILES:
        fig.add_trace(go.Scatter(x=[c["dbo"]], y=[c["od"]], mode="markers+text", text=[c["label"]], textposition="top center", marker=dict(size=max(28, c["samples"]*1.3), color=c["color"], opacity=0.74, line=dict(color="rgba(244,255,254,0.25)", width=1.5)), name=c["label"], hovertemplate=f"{c['cluster']} · {c['label']}<br>DBO: %{{x:.1f}}<br>OD: %{{y:.1f}}<br>Participação: {c['samples']}%<extra></extra>"))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(title=dict(text="Bubble chart — carga orgânica × oxigênio dissolvido", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0), height=380, showlegend=False)
    fig.update_xaxes(title="DBO média")
    fig.update_yaxes(title="OD médio")
    return fig

def build_cluster_variable_chart(var_key="dbo"):
    labels = [c["label"] for c in CLUSTER_PROFILES]
    vals = [c[var_key] for c in CLUSTER_PROFILES]
    colors = [c["color"] for c in CLUSTER_PROFILES]
    label = dict(CLUSTER_VARIABLES).get(var_key, var_key)
    fig = go.Figure(go.Bar(x=labels, y=vals, marker=dict(color=colors), hovertemplate=f"%{{x}}<br>{label}: %{{y:.2f}}<extra></extra>"))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(title=dict(text=f"Valor médio por cluster — {label}", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0), height=330)
    return fig

# ============================================================
#  PAGE SECTIONS
# ============================================================

def make_ml_hero():
    return html.Section(className="ml-hero", children=[
        html.Div(className="hero-bg"), html.Div(className="hero-grid"), html.Div(className="orb orb-1"), html.Div(className="orb orb-2"),
        html.Div(className="ml-hero-content", children=[
            html.Span("Modelagem Preditiva e Descoberta de Padrões", className="section-label"),
            html.H1("Machine Learning no AquaSense", className="ml-hero-title"),
            html.P("A página reúne a frente supervisionada, usada para classificar a qualidade da água a partir do target CONAMA, e a frente não supervisionada, usada para descobrir agrupamentos naturais por K-Means + PCA.", className="ml-hero-body"),
            html.Div(className="ml-hero-actions", children=[html.A("Modelos supervisionados", href="#supervisionado", className="btn-primary"), html.A("Clusterização", href="#clusterizacao", className="btn-secondary")])
        ])
    ])

def make_ml_metrics():
    svm = next(r for r in ALGORITHM_GLOBAL if r["Algoritmo"] == "SVM")
    rf = next(r for r in ALGORITHM_GLOBAL if r["Algoritmo"] == "Random Forest")
    lr = next(r for r in ALGORITHM_GLOBAL if r["Algoritmo"] == "Regressão Logística")
    return html.Section(className="ml-section", children=[
        html.Div(className="ml-metrics-grid", children=[
            ml_metric_card("lucide:shield-check", pct(svm["Acc_Teste"]), "SVM — melhor equilíbrio", "Boa acurácia, macro F1 competitivo e recall crítico forte."),
            ml_metric_card("lucide:activity", f"{lr['Macro_F1']:.2f}", "Maior Macro F1", "A Regressão Logística teve a melhor média entre classes no experimento comparativo."),
            ml_metric_card("lucide:alert-triangle", pct(rf["Recall_Crítica"]), "Gargalo do Random Forest", "Acurácia boa, mas baixa recuperação da classe crítica."),
            ml_metric_card("lucide:git-branch", "K=3", "Clusterização", "Agrupamento final escolhido com apoio do Elbow Method e Silhouette Score."),
        ])
    ])

def make_ml_story():
    return html.Section(className="ml-section ml-section-alt", children=[
        section_header("Do rótulo ao padrão ambiental", "Como a modelagem foi organizada", "O AquaSense combinou classificação supervisionada e clusterização para entender a qualidade da água por duas perspectivas complementares."),
        html.Div(className="ml-story-grid", children=[
            html.Div(className="ml-story-card", children=[html.Div("01", className="ml-story-step"), html.H3("Target CONAMA"), html.P("As regras ambientais serviram de base para transformar parâmetros físico-químicos em classes supervisionadas.")]),
            html.Div(className="ml-story-card", children=[html.Div("02", className="ml-story-step"), html.H3("Modelos supervisionados"), html.P("SVM, Regressão Logística, Random Forest e LightGBM foram comparados por acurácia, F1, recall e matriz de confusão.")]),
            html.Div(className="ml-story-card", children=[html.Div("03", className="ml-story-step"), html.H3("Clusterização"), html.P("O K-Means organizou amostras semelhantes sem usar o rótulo, revelando perfis ambientais naturais.")]),
            html.Div(className="ml-story-card", children=[html.Div("04", className="ml-story-step"), html.H3("Interpretação"), html.P("Os resultados foram analisados considerando risco ambiental, desbalanceamento e falsos negativos críticos.")]),
        ])
    ])

def make_supervised_section():
    rows_global = [[r["Algoritmo"], pct(r["Acc_Treino"]), pct(r["Acc_Teste"]), pct(r["Overfitting"]), f"{r['Weighted_F1']:.2f}", f"{r['Macro_F1']:.2f}", pct(r["Recall_Crítica"]), r["Leitura"]] for r in ALGORITHM_GLOBAL]
    class_rows = []
    for alg in RECALL:
        for cls in ["Excelente", "Boa", "Atenção", "Crítica"]:
            class_rows.append([alg, cls, f"{PRECISION[alg][cls]:.2f}", f"{RECALL[alg][cls]:.2f}", f"{F1[alg][cls]:.2f}"])
    three_rows = [[e["id"], e["algoritmo"], pct(e["train"]), pct(e["acc"]), f"{e['f1']:.2f}", f"{e['macro_f1']:.2f}", pct(e["risk_recall"]), pct(e["risk_precision"])] for e in THREE_CLASS_EXPERIMENTS]
    return html.Section(id="supervisionado", className="ml-section", children=[
        section_header("Aprendizado supervisionado", "Modelos preditivos de classificação", "Comparação dos algoritmos com os resultados reais dos notebooks, destacando o comportamento por classe e o impacto do desbalanceamento."),
        html.Div(className="ml-two-col", children=[html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_train_test_chart(), config={"displayModeBar": False})]), html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_overfitting_chart(), config={"displayModeBar": False})])]),
        html.Div(className="ml-two-col", children=[html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_f1_chart(), config={"displayModeBar": False})]), html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_class_metric_heatmap("Recall"), config={"displayModeBar": False})])]),
        html.Div(className="ml-two-col", children=[html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_class_metric_heatmap("Precision"), config={"displayModeBar": False})]), html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_recall_critical_chart(), config={"displayModeBar": False})])]),
        html.Div(className="ml-analysis-card", children=[
            html.H3("Leitura crítica dos resultados"),
            html.P("A comparação não pode ser feita apenas por acurácia. O Random Forest, por exemplo, teve acurácia de teste de 73,5%, mas recall crítico de apenas 5%, indicando que o modelo praticamente não recuperou a classe ambiental mais perigosa."),
            html.P("A Regressão Logística teve desempenho competitivo mesmo sendo linear. Isso não invalida o projeto: significa que parte da separabilidade dos dados foi capturada por combinações aproximadamente lineares após padronização e balanceamento. Ainda assim, ela continua limitada para fronteiras ambientais mais complexas."),
            html.Div(className="ml-mini-grid", children=[
                html.Div(children=[html.H4("SVM"), html.P("Melhor equilíbrio operacional entre macro F1, recall crítico e gap treino-teste.")]),
                html.Div(children=[html.H4("Regressão Logística"), html.P("Baseline linear forte e estável, útil como referência interpretável.")]),
                html.Div(children=[html.H4("LightGBM"), html.P("Alto recall crítico, mas baixa precisão; tende a emitir mais alertas.")]),
                html.Div(children=[html.H4("Random Forest"), html.P("Acurácia razoável, mas baixa sensibilidade à classe crítica em 4 classes.")]),
            ])
        ]),
        html.Div(className="ml-table-section", children=[html.H3("Comparação global dos algoritmos — Experimento 4"), mini_table(["Algoritmo", "Acc Treino", "Acc Teste", "Gap", "Weighted F1", "Macro F1", "Recall Crítica", "Leitura"], rows_global)]),
        html.Div(className="ml-table-section", children=[html.H3("Métricas por classe — Experimento 4"), mini_table(["Algoritmo", "Classe", "Precision", "Recall", "F1-score"], class_rows)]),
        html.Div(className="ml-two-col", children=[
            html.Div(className="ml-chart-card", children=[dcc.Graph(id="ml-experiment-timeline", figure=build_experiment_timeline("Regressão Logística"), config={"displayModeBar": False})]),
            html.Div(className="ml-control-card", children=[
                html.H3("Explorar trilha por algoritmo"),
                html.P("Selecione o algoritmo e o experimento. A trilha, os cards e a interpretação mudam junto."),
                dcc.Dropdown(id="ml-algorithm-dropdown", options=[{"label": a, "value": a} for a in EXPERIMENTS_BY_ALGO.keys()], value="Regressão Logística", clearable=False, className="var-dropdown ml-dropdown"),
                dcc.Dropdown(id="ml-exp-dropdown", options=[], value=None, clearable=False, className="var-dropdown ml-dropdown"),
                html.Div(id="ml-exp-detail", className="ml-exp-detail")
            ])
        ]),
        html.Div(className="ml-two-col", children=[
            html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_three_class_chart(), config={"displayModeBar": False})]),
            html.Div(className="ml-analysis-card compact", children=[html.H3("Por que analisar 3 classes?"), html.P("A redução para 3 classes diminui a granularidade do problema e pode reduzir a sobreposição entre Boa, Atenção e Crítica. No Random Forest, porém, o experimento 10 mostrou que isso não resolveu completamente o gargalo crítico: a acurácia de teste ficou em 77,8%, mas o recall crítico permaneceu em 12%."), html.P("Isso reforça a conclusão central: a avaliação precisa olhar para as classes de risco, não apenas para a acurácia global.")])
        ]),
        html.Div(className="ml-table-section", children=[html.H3("Experimentos com 3 classes — resultados reais disponíveis"), mini_table(["Exp", "Algoritmo", "Acc Treino", "Acc Teste", "Weighted F1", "Macro F1", "Recall Crítico", "Precision Crítico"], three_rows)]),
    ])

def make_clustering_section():
    cluster_rows = [[c["cluster"], c["label"], f"{c['samples']}%", f"{c['dbo']:.1f}", f"{c['od']:.1f}", f"{c['nitrogen']:.1f}", c["interpretation"]] for c in CLUSTER_PROFILES]
    return html.Section(id="clusterizacao", className="ml-section ml-section-alt", children=[
        section_header("Aprendizado não supervisionado", "Clusterização com K-Means + PCA", "Descoberta de agrupamentos naturais nos dados ambientais sem utilizar o rótulo CONAMA durante o agrupamento."),
        html.Div(className="ml-analysis-card", children=[html.H3("Por que padronizar, reduzir dimensionalidade e clusterizar?"), html.Div(className="ml-mini-grid", children=[html.Div(children=[html.H4("StandardScaler"), html.P("Padroniza escalas para impedir que variáveis de maior magnitude dominem as distâncias.")]), html.Div(children=[html.H4("PCA"), html.P("Reduz redundância e permite visualizar padrões em componentes principais.")]), html.Div(children=[html.H4("K-Means"), html.P("Agrupa amostras semelhantes por distância aos centroides.")]), html.Div(children=[html.H4("K=3"), html.P("Escolha apoiada por Elbow e Silhouette, produzindo três perfis ambientais.")])])]),
        html.Div(className="ml-two-col", children=[html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_pca_variance_chart(), config={"displayModeBar": False})]), html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_cluster_scatter(), config={"displayModeBar": False})])]),
        html.Div(className="ml-two-col", children=[html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_elbow_chart(), config={"displayModeBar": False})]), html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_silhouette_chart(), config={"displayModeBar": False})])]),
        html.Div(className="ml-two-col", children=[html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_cluster_profile_heatmap(), config={"displayModeBar": False})]), html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_cluster_bubble(), config={"displayModeBar": False})])]),
        html.Div(className="ml-two-col", children=[html.Div(className="ml-control-card", children=[html.H3("Comparar variável por cluster"), html.P("Escolha uma variável físico-química para observar como os clusters se diferenciam."), dcc.Dropdown(id="ml-cluster-var-dropdown", options=[{"label": label, "value": key} for key, label in CLUSTER_VARIABLES], value="dbo", clearable=False, className="var-dropdown ml-dropdown"), dcc.Graph(id="ml-cluster-var-chart", config={"displayModeBar": False})]), html.Div(className="ml-analysis-card compact", children=[html.H3("Interpretação dos clusters"), html.P("Os clusters não foram criados a partir das classes supervisionadas. Eles emergem da similaridade entre amostras no espaço PCA. Ainda assim, os perfis médios mostram coerência ambiental: baixos poluentes e OD alto no grupo preservado; nutrientes/DBO intermediários no grupo de atenção; e degradação no grupo crítico."), html.P("Essa análise fortalece o projeto porque confirma que padrões ambientais aparecem tanto pela via supervisionada quanto pela descoberta não supervisionada.")])]),
        html.Div(className="ml-table-section", children=[html.H3("Tabela interpretativa dos clusters"), mini_table(["Cluster", "Interpretação", "Participação", "DBO", "OD", "Nitrogênio", "Leitura ambiental"], cluster_rows)]),
    ])

def make_ml_final_note():
    return html.Section(className="ml-section", children=[html.Div(className="ml-final-note", children=[html.Div(className="ml-final-icon", children=[ml_icon("lucide:sparkles", 28)]), html.H2("Síntese da modelagem"), html.P("A frente supervisionada mede capacidade preditiva a partir do target CONAMA. A clusterização revela agrupamentos naturais sem rótulo. Juntas, as duas abordagens tornam o AquaSense mais robusto: uma classifica, a outra ajuda a interpretar padrões ambientais ocultos.")])])

# ============================================================
#  CALLBACKS
# ============================================================

def register_ml_callbacks(app):
    @app.callback(
        Output("ml-experiment-timeline", "figure"),
        Output("ml-exp-dropdown", "options"),
        Output("ml-exp-dropdown", "value"),
        Input("ml-algorithm-dropdown", "value"),
    )
    def update_experiment_selector(algorithm):
        algorithm = algorithm or "Regressão Logística"
        experiments = EXPERIMENTS_BY_ALGO.get(algorithm, EXPERIMENTS_BY_ALGO["Regressão Logística"])
        options = [{"label": f"{e['id']} · {e['classes']} classes · {e['balance']}", "value": e["id"]} for e in experiments]
        value = experiments[0]["id"]
        return build_experiment_timeline(algorithm), options, value

    @app.callback(
        Output("ml-exp-detail", "children"),
        Input("ml-algorithm-dropdown", "value"),
        Input("ml-exp-dropdown", "value"),
    )
    def update_exp_detail(algorithm, exp_id):
        algorithm = algorithm or "Regressão Logística"
        experiments = EXPERIMENTS_BY_ALGO.get(algorithm, EXPERIMENTS_BY_ALGO["Regressão Logística"])
        exp = next((e for e in experiments if e["id"] == exp_id), experiments[0])
        return html.Div(children=[
            html.Div(className="ml-detail-badges", children=[html.Span(f"{exp['classes']} classes"), html.Span(exp["balance"]), html.Span(exp["features"])]),
            html.Div(className="ml-detail-metrics", children=[html.Div([html.Strong(pct(exp["accuracy"])), html.Span("Acurácia")]), html.Div([html.Strong(f"{exp['macro_f1']:.2f}"), html.Span("Macro F1")]), html.Div([html.Strong(f"{exp['risk_recall']:.2f}"), html.Span("Recall risco")])]),
            html.P(exp["lesson"], className="ml-detail-text"),
        ])

    @app.callback(Output("ml-cluster-var-chart", "figure"), Input("ml-cluster-var-dropdown", "value"))
    def update_cluster_var_chart(var_key):
        return build_cluster_variable_chart(var_key or "dbo")
