from dash import html, dcc, Input, Output, State, callback_context
import plotly.graph_objects as go
import random
import os, sys
import joblib
import pandas as pd
import numpy as np

# ============================================================
#  MODEL LOADING
# ============================================================

_BASE = os.path.dirname(os.path.abspath(__file__))

def _load_model():
    paths = [
        os.path.join(_BASE, "models", "aquasense_modelo_final.joblib"),
        os.path.join(_BASE, "aquasense_modelo_final.joblib"),
    ]
    for p in paths:
        if os.path.exists(p):
            return joblib.load(p)
    return None

def _load_features():
    paths = [
        os.path.join(_BASE, "models", "features_modelo.joblib"),
        os.path.join(_BASE, "features_modelo.joblib"),
    ]
    for p in paths:
        if os.path.exists(p):
            return joblib.load(p)
    return ['Temperature (cel)', 'Orthophosphate (mg/l)', 'Country', 'Waterbody Type', 'Nitrogen (mg/l)']

_MODEL = _load_model()
_FEATURES = _load_features()
_CLASSES = list(_MODEL.classes_) if _MODEL is not None else ['Adequada', 'Atenção', 'Não adequada']

# ============================================================
#  DESIGN TOKENS
# ============================================================

TEAL_PALETTE = ["#3fffe7", "#00e0ca", "#00c4ad", "#00a893", "#008c7a"]
CLASS_COLORS = {
    "Adequada":    "#3fffe7",
    "Atenção":     "#f5a623",
    "Não adequada": "#e25c72",
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

# ============================================================
#  DATA — CLUSTERIZAÇÃO (preserved exactly)
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
#  DATA — FINAL MODEL RESULTS
# ============================================================

FINAL_MODEL = {
    "algorithm": "LightGBM",
    "features": ["Temperature (cel)", "Orthophosphate (mg/l)", "Nitrogen (mg/l)", "Country", "Waterbody Type"],
    "classes": ["Adequada", "Atenção", "Não Adequada"],
    "train_acc": 0.920, "test_acc": 0.904,
    "train_precision": 0.926, "test_precision": 0.91,
    "train_recall": 0.920, "test_recall": 0.90,
    "train_f1": 0.921, "test_f1": 0.91,
    "macro_f1": 0.89,
}

# Per-class train/test metrics for the new "Desempenho por Classe — Treino x Teste" chart
CLASS_TRAIN_TEST_METRICS = {
    "Precisão Adequada":      {"train": 0.94, "test": 0.93},
    "Precisão Atenção":       {"train": 0.96, "test": 0.94},
    "Precisão Não Adequada":  {"train": 0.78, "test": 0.75},
    "Recall Adequada":        {"train": 0.98, "test": 0.97},
    "Recall Atenção":         {"train": 0.87, "test": 0.86},
    "Recall Não Adequada":    {"train": 0.93, "test": 0.89},
    "F1 Adequada":            {"train": 0.96, "test": 0.95},
    "F1 Atenção":             {"train": 0.92, "test": 0.90},
    "F1 Não Adequada":        {"train": 0.85, "test": 0.82},
}

CLASS_METRICS = {
    "Adequada":     {"precision": 0.93, "recall": 0.97, "f1": 0.95},
    "Atenção":      {"precision": 0.94, "recall": 0.86, "f1": 0.90},
    "Não Adequada": {"precision": 0.75, "recall": 0.89, "f1": 0.82},
}

CONFUSION = {
    "matrix": [[4010, 107, 0], [295, 5149, 546], [0, 199, 1674]],
    "labels": ["Adequada", "Atenção", "Não Adequada"],
}

SHAP_GLOBAL = [
    ("Orthophosphate", 0.312),
    ("Nitrogen", 0.267),
    ("Effluent", 0.108),
    ("Temperature", 0.092),
    ("River", 0.071),
    ("Sewage", 0.054),
    ("Estuarine", 0.038),
    ("USA", 0.029),
    ("Ireland", 0.016),
    ("Canal", 0.013),
]

SHAP_BY_CLASS = {
    "Adequada":     [("Orthophosphate", 0.28), ("Nitrogen", 0.23), ("Temperature", 0.19), ("Effluent", 0.12), ("River", 0.08), ("Sewage", 0.05), ("Estuarine", 0.03), ("USA", 0.01), ("Ireland", 0.01)],
    "Atenção":      [("Nitrogen", 0.31), ("Orthophosphate", 0.26), ("Temperature", 0.14), ("Effluent", 0.11), ("River", 0.07), ("Sewage", 0.05), ("Estuarine", 0.04), ("USA", 0.01), ("Ireland", 0.01)],
    "Não Adequada": [("Effluent", 0.34), ("Orthophosphate", 0.29), ("Nitrogen", 0.17), ("Sewage", 0.09), ("Temperature", 0.05), ("River", 0.03), ("Estuarine", 0.02), ("USA", 0.01)],
}

EXPERIMENTAL_TIMELINE = [
    {
        "step": "01", "title": "4 Classes",
        "subtitle": "CONAMA Original",
        "algorithm": "SVM",
        "accuracy": 0.773, "macro_f1": 0.51, "recall_risk": 0.62,
        "insight": "Boa capacidade de identificar cenários críticos, porém forte sobreposição entre classes intermediárias.",
        "color": "#7c6af7",
    },
    {
        "step": "02", "title": "3 Classes + Recorte Temporal",
        "subtitle": "Redução da granularidade",
        "algorithm": "LightGBM",
        "accuracy": 0.724, "macro_f1": 0.59, "recall_risk": None,
        "insight": "Redução parcial da ambiguidade entre classes, mas acurácia global ainda limitada.",
        "color": "#f5a623",
    },
    {
        "step": "03", "title": "Classificação Binária",
        "subtitle": "Adequada vs Não Adequada",
        "algorithm": "LightGBM",
        "accuracy": 0.807, "macro_f1": 0.78, "recall_risk": None,
        "insight": "Separação mais clara entre condições adequadas e não adequadas. Ganho significativo.",
        "color": "#00c4ad",
    },
    {
        "step": "04", "title": "Reconstrução do Rótulo",
        "subtitle": "Configuração final — 3 classes refinadas",
        "algorithm": "LightGBM",
        "accuracy": 0.904, "macro_f1": 0.89, "recall_risk": 0.89,
        "insight": "Melhor configuração obtida. A reformulação do problema, não a troca de algoritmo, foi o diferencial.",
        "color": "#3fffe7",
    },
]

COUNTRIES = ["Canada", "China", "England", "Ireland", "USA"]
WATERBODY_TYPES = ["River", "Effluent", "Lake", "Estuarine", "Bay", "Sea Water", "Canal", "Sewage", "Marine", "Drainage", "Transitional"]

# ============================================================
#  HELPERS
# ============================================================

def ml_icon(icon, size=22, color="#3fffe7"):
    from dash_iconify import DashIconify
    return DashIconify(icon=icon, width=size, height=size, color=color)

def pct(v):
    if v is None: return "—"
    return f"{v*100:.1f}%"

def section_header(kicker, title, text):
    return html.Div(className="ml-section-header", children=[
        html.Span(kicker, className="section-label"),
        html.H2(title, className="section-title"),
        html.P(text, className="section-sub"),
    ])

def ml_metric_card(icon, value, title, desc):
    return html.Div(className="ml-metric-card", children=[
        html.Div(className="ml-metric-icon", children=[ml_icon(icon)]),
        html.Div(value, className="ml-metric-value"),
        html.Div(title, className="ml-metric-title"),
        html.P(desc, className="ml-metric-desc"),
    ])

def mini_table(headers, rows, class_name="ml-table"):
    return html.Div(className="ml-table-wrap", children=[
        html.Table(className=class_name, children=[
            html.Thead(html.Tr([html.Th(h) for h in headers])),
            html.Tbody([html.Tr([html.Td(c) for c in row]) for row in rows]),
        ])
    ])

# ============================================================
#  CHARTS — MODELO FINAL
# ============================================================

def build_train_test_grouped():
    """
    Desempenho por Classe — Treino x Teste.
    Replaces the previous overall (Acurácia/Precisão/Recall/F1) bar chart
    with a per-class breakdown across Precision/Recall/F1, matching the
    notebook's reference chart.
    """
    metrics = list(CLASS_TRAIN_TEST_METRICS.keys())
    train_vals = [CLASS_TRAIN_TEST_METRICS[m]["train"] for m in metrics]
    test_vals  = [CLASS_TRAIN_TEST_METRICS[m]["test"] for m in metrics]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Treino", x=metrics, y=train_vals,
        marker=dict(color="rgba(63,255,231,0.75)"),
        text=[f"{v*100:.0f}%" for v in train_vals],
        textposition="outside",
        textfont=dict(color="#d8f5f1", size=10),
        hovertemplate="%{x}<br>Treino: %{y:.1%}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Teste", x=metrics, y=test_vals,
        marker=dict(color="rgba(245,166,35,0.82)"),
        text=[f"{v*100:.0f}%" for v in test_vals],
        textposition="outside",
        textfont=dict(color="#d8f5f1", size=10),
        hovertemplate="%{x}<br>Teste: %{y:.1%}<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text="Desempenho por Classe — Treino x Teste", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0),
        height=420, barmode="group", showlegend=True,
        legend=dict(orientation="h", y=1.10, x=0),
        margin=dict(l=18, r=18, t=58, b=90),
    )
    fig.update_yaxes(tickformat=".0%", range=[0, 1.08])
    fig.update_xaxes(tickangle=-30, tickfont=dict(size=10, color="rgba(212,245,241,0.68)"))
    return fig

def build_class_radar():
    classes = list(CLASS_METRICS.keys())
    metrics_keys = ["precision", "recall", "f1"]
    metrics_labels = ["Precision", "Recall", "F1"]
    colors = [CLASS_COLORS.get(c, "#3fffe7") for c in classes]
    fig = go.Figure()
    fill_map = {
        "Adequada":    "rgba(63,255,231,0.12)",
        "Atenção":     "rgba(245,166,35,0.12)",
        "Não Adequada":"rgba(226,92,114,0.12)",
    }
    for cls, color in zip(classes, colors):
        vals = [CLASS_METRICS[cls][m] for m in metrics_keys]
        vals_closed = vals + [vals[0]]
        labels_closed = metrics_labels + [metrics_labels[0]]
        fig.add_trace(go.Scatterpolar(r=vals_closed, theta=labels_closed, fill="toself",
                                      name=cls, line=dict(color=color, width=2),
                                      fillcolor=fill_map.get(cls, "rgba(63,255,231,0.12)"),
                                      hovertemplate=f"{cls}<br>%{{theta}}: %{{r:.2f}}<extra></extra>"))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text="Desempenho por classe", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0),
        height=390, showlegend=True,
        legend=dict(orientation="h", y=1.10, x=0),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(63,255,231,0.12)", tickfont=dict(color="#d8f5f1", size=10)),
            angularaxis=dict(gridcolor="rgba(63,255,231,0.12)", tickfont=dict(color="#d8f5f1", size=12)),
        ),
    )
    return fig

def build_confusion_heatmap():
    z = CONFUSION["matrix"]
    labels = CONFUSION["labels"]
    text = [[str(v) for v in row] for row in z]
    fig = go.Figure(go.Heatmap(
        z=z, x=labels, y=labels,
        colorscale=[[0, "rgba(1,26,24,0.95)"], [0.5, "#006960"], [1, "#3fffe7"]],
        text=text, texttemplate="<b>%{text}</b>",
        hovertemplate="Real: %{y}<br>Previsto: %{x}<br>Contagem: %{z}<extra></extra>",
        colorbar=dict(title=dict(text="Contagem", font=dict(color="#d8f5f1")), tickfont=dict(color="#d8f5f1"), thickness=12),
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text="Matriz de Confusão — conjunto de teste", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0),
        height=400,
        xaxis=dict(title="Classe Prevista", tickfont=dict(size=11, color="#d8f5f1")),
        yaxis=dict(title="Classe Real", tickfont=dict(size=11, color="#d8f5f1"), autorange="reversed"),
    )
    return fig

def build_scenario_comparison():
    scenarios = [e["title"] for e in EXPERIMENTAL_TIMELINE]
    accs = [e["accuracy"] for e in EXPERIMENTAL_TIMELINE]
    colors_bar = [e["color"] for e in EXPERIMENTAL_TIMELINE]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=scenarios, y=accs,
        marker=dict(color=colors_bar, line=dict(color="rgba(244,255,254,0.15)", width=1)),
        hovertemplate="%{x}<br>Acurácia: %{y:.1%}<extra></extra>",
        text=[f"{v:.1%}" for v in accs], textposition="outside",
        textfont=dict(color="#d8f5f1", size=13),
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text="Evolução da acurácia por cenário experimental", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0),
        height=360,
        margin=dict(l=18, r=18, t=52, b=48),
    )
    fig.update_yaxes(tickformat=".0%", range=[0, 1.05])
    return fig

def build_shap_global():
    names, vals = zip(*SHAP_GLOBAL)
    names_r = list(reversed(names))
    vals_r  = list(reversed(vals))
    bar_colors = ["#3fffe7" if n in ("Orthophosphate", "Nitrogen", "Temperature") else "rgba(63,255,231,0.40)" for n in names_r]
    fig = go.Figure(go.Bar(
        x=vals_r, y=names_r, orientation="h",
        marker=dict(color=bar_colors, line=dict(color="rgba(244,255,254,0.1)", width=1)),
        hovertemplate="%{y}<br>Importância SHAP: %{x:.3f}<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text="Importância Global SHAP", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0),
        height=400, margin=dict(l=110, r=18, t=52, b=28),
    )
    return fig

def build_shap_pareto():
    names, vals = zip(*SHAP_GLOBAL)
    total = sum(vals)
    norm = [v / total for v in vals]
    cumulative, s = [], 0
    for v in norm:
        s += v; cumulative.append(s)
    highlight = [n in ("Orthophosphate", "Nitrogen", "Temperature") for n in names]
    bar_colors = ["#3fffe7" if h else "rgba(63,255,231,0.38)" for h in highlight]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(names), y=norm,
        marker=dict(color=bar_colors),
        name="Importância individual",
        hovertemplate="%{x}<br>Contribuição: %{y:.1%}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=list(names), y=cumulative,
        mode="lines+markers", name="Acumulado",
        line=dict(color="#f5a623", width=2.5, shape="spline"),
        marker=dict(size=7),
        hovertemplate="%{x}<br>Acumulado: %{y:.1%}<extra></extra>",
        yaxis="y2",
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text="Pareto SHAP — contribuição acumulada", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0),
        height=370, showlegend=True,
        legend=dict(orientation="h", y=1.12, x=0),
        yaxis=dict(tickformat=".0%", title="Contribuição individual", gridcolor="rgba(63,255,231,0.08)"),
        yaxis2=dict(tickformat=".0%", title="Acumulado", overlaying="y", side="right", range=[0, 1.05], gridcolor="rgba(0,0,0,0)", tickfont=dict(color="#f5a623")),
    )
    return fig

def build_shap_by_class(class_name="Adequada"):
    data = SHAP_BY_CLASS.get(class_name, [])
    names, vals = zip(*data) if data else ([], [])
    names_r = list(reversed(names))
    vals_r  = list(reversed(vals))
    color = CLASS_COLORS.get(class_name, "#3fffe7")
    fig = go.Figure(go.Bar(
        x=vals_r, y=names_r, orientation="h",
        marker=dict(color=color, opacity=0.82, line=dict(color="rgba(244,255,254,0.1)", width=1)),
        hovertemplate="%{y}<br>SHAP: %{x:.3f}<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(
        title=dict(text=f"Importância SHAP — {class_name}", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0),
        height=360, margin=dict(l=110, r=18, t=52, b=28),
    )
    return fig

# ============================================================
#  CHARTS — CLUSTERIZAÇÃO (preserved)
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
    vars_keys   = [v[0] for v in CLUSTER_VARIABLES]
    vars_labels = [v[1] for v in CLUSTER_VARIABLES]
    clusters    = [c["label"] for c in CLUSTER_PROFILES]
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
    vals   = [c[var_key] for c in CLUSTER_PROFILES]
    colors = [c["color"] for c in CLUSTER_PROFILES]
    label  = dict(CLUSTER_VARIABLES).get(var_key, var_key)
    fig = go.Figure(go.Bar(x=labels, y=vals, marker=dict(color=colors), hovertemplate=f"%{{x}}<br>{label}: %{{y:.2f}}<extra></extra>"))
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(title=dict(text=f"Valor médio por cluster — {label}", font=dict(family="Syne, sans-serif", size=14, color="#f4fffe"), x=0), height=330)
    return fig

# ============================================================
#  PAGE SECTIONS — HERO (updated)
# ============================================================

def make_ml_hero():
    return html.Section(className="ml-hero", children=[
        html.Div(className="hero-bg"),
        html.Div(className="hero-grid"),
        html.Div(className="orb orb-1"),
        html.Div(className="orb orb-2"),
        html.Div(className="ml-hero-content", children=[
            html.Span("Modelagem Preditiva e Descoberta de Padrões", className="section-label"),
            html.H1("Machine Learning no AquaSense", className="ml-hero-title"),
            html.P("Modelos supervisionados e não supervisionados aplicados à classificação da qualidade da água e à descoberta de padrões ambientais.", className="ml-hero-body"),
            html.Div(className="ml-hero-actions", children=[
                html.A("Evolução experimental", href="#evolucao", className="btn-primary"),
                html.A("Simulador", href="#simulador", className="btn-secondary"),
                html.A("Clusterização", href="#clusterizacao", className="btn-ghost"),
            ]),
        ]),
    ])

# ============================================================
#  SECTION 1 — VISÃO GERAL
# ============================================================

def make_ml_overview():
    return html.Section(className="ml-section", children=[
        html.Div(className="ml-metrics-grid", children=[
            ml_metric_card("lucide:shield-check", "90,4%", "Modelo Final", "Acurácia obtida em dados de teste."),
            ml_metric_card("lucide:activity",     "0,89",  "Macro F1",     "Equilíbrio global entre as três classes."),
            ml_metric_card("lucide:alert-triangle","89%",  "Recall Não Adequada", "Capacidade de identificar condições de risco ambiental."),
            ml_metric_card("lucide:sparkles",     "Ortofosfato + Nitrogênio", "Principais Variáveis", "Variáveis mais influentes para a tomada de decisão do modelo."),
        ]),
    ])

# ============================================================
#  SECTION 2 — EVOLUÇÃO EXPERIMENTAL (timeline)
# ============================================================

def make_evolution_section():
    step_cards = []
    for exp in EXPERIMENTAL_TIMELINE:
        is_final = exp["step"] == "04"
        metrics_items = [
            html.Div(className="ml-evo-metric", children=[
                html.Span("Acurácia", className="ml-evo-metric-label"),
                html.Span(pct(exp["accuracy"]), className="ml-evo-metric-value"),
            ]),
            html.Div(className="ml-evo-metric", children=[
                html.Span("Macro F1", className="ml-evo-metric-label"),
                html.Span(f"{exp['macro_f1']:.2f}", className="ml-evo-metric-value"),
            ]),
        ]
        if exp.get("recall_risk") is not None:
            metrics_items.append(html.Div(className="ml-evo-metric", children=[
                html.Span("Recall Risco", className="ml-evo-metric-label"),
                html.Span(pct(exp["recall_risk"]), className="ml-evo-metric-value"),
            ]))
        step_cards.append(
            html.Div(
                className=f"ml-evo-card {'ml-evo-card--final' if is_final else ''}",
                style={"--evo-accent": exp["color"]},
                children=[
                    html.Div(className="ml-evo-step-badge", children=[exp["step"]]),
                    html.Div(className="ml-evo-algo-tag", children=[exp["algorithm"]]),
                    html.H3(exp["title"], className="ml-evo-title"),
                    html.Span(exp["subtitle"], className="ml-evo-subtitle"),
                    html.Div(className="ml-evo-metrics", children=metrics_items),
                    html.P(exp["insight"], className="ml-evo-insight"),
                    html.Div(className="ml-evo-connector") if exp["step"] != "04" else None,
                ]
            )
        )

    return html.Section(id="evolucao", className="ml-section ml-section-alt", children=[
        section_header(
            "Evolução experimental",
            "Como chegamos ao modelo final",
            "A melhoria de 77,3% para 90,4% não ocorreu pela troca de algoritmo, mas pela reformulação estratégica do problema de classificação.",
        ),
        html.Div(className="ml-evo-timeline", children=step_cards),
        html.Div(className="ml-analysis-card", children=[
            html.H3("Por que a reformulação foi o diferencial?"),
            html.P("Os experimentos mostraram que o principal desafio não estava no algoritmo, mas na sobreposição existente entre as classes. Para reduzir essa ambiguidade, o rótulo foi reconstruído a partir das subclasses identificadas pelas probabilidades do modelo, concentrando os casos mais incertos em uma classe intermediária de atenção."),
            html.P("Essa estratégia tornou as fronteiras de decisão mais claras e elevou o desempenho do LightGBM de 80,7% para 90,4% no cenário final."),
        ]),
    ])

# ============================================================
#  SECTION 3 — MODELO FINAL CONFIG
# ============================================================

def make_final_model_section():
    return html.Section(className="ml-section", children=[
        section_header(
            "Configuração final",
            "Modelo Final do AquaSense",
            "Parâmetros definitivos utilizados no pipeline de produção.",
        ),
        html.Div(className="ml-final-config-grid", children=[
            html.Div(className="ml-config-card", children=[
                html.Div(className="ml-config-icon", children=[ml_icon("lucide:cpu", 24)]),
                html.H4("Algoritmo"),
                html.Div(className="ml-config-value", children=["LightGBM"]),
            ]),
            html.Div(className="ml-config-card", children=[
                html.Div(className="ml-config-icon", children=[ml_icon("lucide:layers", 24)]),
                html.H4("Variáveis"),
                html.Ul(className="ml-config-list", children=[
                    html.Li("Temperature (°C)"),
                    html.Li("Orthophosphate (mg/L)"),
                    html.Li("Nitrogen (mg/L)"),
                    html.Li("Country"),
                    html.Li("Waterbody Type"),
                ]),
            ]),
            html.Div(className="ml-config-card", children=[
                html.Div(className="ml-config-icon", children=[ml_icon("lucide:tag", 24)]),
                html.H4("Classes de saída"),
                html.Div(className="ml-classes-list", children=[
                    html.Span("Adequada",     className="ml-class-badge ml-class-badge--adequada"),
                    html.Span("Atenção",      className="ml-class-badge ml-class-badge--atencao"),
                    html.Span("Não Adequada", className="ml-class-badge ml-class-badge--nao"),
                ]),
            ]),
            html.Div(className="ml-config-card ml-config-card--highlight", children=[
                html.Div(className="ml-config-icon", children=[ml_icon("lucide:trending-up", 24)]),
                html.H4("Resultado de teste"),
                html.Div(className="ml-config-big-metric", children=["90,4%"]),
                html.Span("Acurácia · Macro F1: 0,89", className="ml-config-sub"),
            ]),
        ]),
    ])

# ============================================================
#  SECTION 4 — DESEMPENHO
# ============================================================

def make_performance_section():
    cm_interpretation = [
        html.Li([html.Strong("Adequada: "), "4.010 corretas, 107 confundidas com Atenção — excelente precisão."]),
        html.Li([html.Strong("Atenção: "), "5.149 corretas, 295 confundidas com Adequada e 546 com Não Adequada — maior zona de ambiguidade."]),
        html.Li([html.Strong("Não Adequada: "), "1.674 corretas, 199 confundidas com Atenção — 0 confusões com Adequada, demonstrando separação clara nos extremos."]),
    ]
    return html.Section(className="ml-section ml-section-alt", children=[
        section_header(
            "Desempenho do modelo",
            "Análise completa de métricas",
            "Resultado do LightGBM treinado com a configuração final sobre o conjunto de teste independente.",
        ),
        html.Div(className="ml-two-col", children=[
            html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_train_test_grouped(), config={"displayModeBar": False})]),
            html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_class_radar(), config={"displayModeBar": False})]),
        ]),
        html.Div(className="ml-two-col", children=[
            html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_confusion_heatmap(), config={"displayModeBar": False})]),
            html.Div(className="ml-analysis-card compact", children=[
                html.H3("Leitura da matriz de confusão"),
                html.Ul(className="ml-cm-list", children=cm_interpretation),
                html.P("A ausência de confusão entre Adequada e Não Adequada confirma que o modelo capturou corretamente a separação nos extremos do espectro ambiental, concentrando a ambiguidade residual na classe intermediária de Atenção — comportamento esperado e ambientalmente coerente."),
            ]),
        ]),
        html.Div(className="ml-table-section", children=[
            html.H3("Métricas por classe — conjunto de teste"),
            mini_table(
                ["Classe", "Precision", "Recall", "F1-score"],
                [[cls, f"{m['precision']:.2f}", f"{m['recall']:.2f}", f"{m['f1']:.2f}"] for cls, m in CLASS_METRICS.items()],
            ),
        ]),
    ])

# ============================================================
#  SECTION 5 — COMPARAÇÃO DOS CENÁRIOS
# ============================================================

def make_scenario_section():
    rows = [[e["title"], e["algorithm"], pct(e["accuracy"]), f"{e['macro_f1']:.2f}"] for e in EXPERIMENTAL_TIMELINE]
    return html.Section(className="ml-section", children=[
        section_header(
            "Comparação dos cenários",
            "Evolução de 77,3% para 90,4%",
            "Cada experimento representou uma reformulação estratégica do problema, não apenas uma mudança de hiperparâmetros.",
        ),
        html.Div(className="ml-chart-card", children=[
            dcc.Graph(figure=build_scenario_comparison(), config={"displayModeBar": False}),
        ]),
        html.Div(className="ml-analysis-card", children=[
            html.H3("O que explica o salto de desempenho?"),
            html.P("Ao longo dos experimentos, o algoritmo utilizado (LightGBM) permaneceu praticamente constante. O que mudou foi a forma como o problema foi formulado: a granularidade das classes, o recorte temporal dos dados e, finalmente, a reconstrução do rótulo com critérios ambientais mais precisos."),
            html.P("Esse padrão evidencia uma lição central do projeto: em aprendizado supervisionado aplicado a dados ambientais, a qualidade da definição do target pode ser mais determinante do que a sofisticação do modelo escolhido."),
            html.Div(className="ml-mini-grid", children=[
                html.Div(children=[html.H4("4 Classes → 77,3%"), html.P("Sobreposição elevada entre classes intermediárias do CONAMA.")]),
                html.Div(children=[html.H4("3 Classes → 72,4%"), html.P("Redução parcial da ambiguidade; acurácia global ainda limitada.")]),
                html.Div(children=[html.H4("Binário → 80,7%"), html.P("Separação clara, mas perda de granularidade ambiental.")]),
                html.Div(children=[html.H4("Reconstruído → 90,4%"), html.P("Melhor configuração: equilíbrio entre granularidade e separabilidade.")]),
            ]),
        ]),
        html.Div(className="ml-table-section", children=[
            html.H3("Tabela comparativa dos cenários"),
            mini_table(["Cenário", "Algoritmo", "Acurácia", "Macro F1"], rows),
        ]),
    ])

# ============================================================
#  SECTION 6 — INTERPRETABILIDADE
# ============================================================

def make_interpretability_section():
    interp_cards = [
        ("lucide:zap",       "#3fffe7", "Principal variável", "Orthophosphate", "Indicador de eutrofização. Alta concentração sinaliza enriquecimento por nutrientes e degradação ambiental."),
        ("lucide:droplets",  "#00c4ad", "Segunda variável",   "Nitrogen",       "Nitrogênio total reforça o diagnóstico de eutrofização e distingue fontes de poluição difusa."),
        ("lucide:thermometer","#f5a623","Variável complementar","Temperature",  "Temperatura influencia processos biológicos e a tolerância de espécies aquáticas."),
    ]
    return html.Section(className="ml-section ml-section-alt", children=[
        section_header(
            "Interpretabilidade do modelo",
            "Como o modelo toma decisões?",
            "Análise SHAP (SHapley Additive exPlanations) revela a contribuição individual de cada variável para as previsões do LightGBM.",
        ),
        html.Div(className="ml-interp-cards", children=[
            html.Div(className="ml-interp-card", children=[
                html.Div(className="ml-interp-icon", children=[ml_icon(ic, 22, color=col)]),
                html.Span(label, className="ml-interp-card-label"),
                html.H4(val, className="ml-interp-card-value"),
                html.P(desc, className="ml-interp-card-desc"),
            ]) for ic, col, label, val, desc in interp_cards
        ]),
        html.Div(className="ml-two-col", children=[
            html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_shap_global(), config={"displayModeBar": False})]),
            html.Div(className="ml-chart-card", children=[dcc.Graph(figure=build_shap_pareto(), config={"displayModeBar": False})]),
        ]),
        html.Div(className="ml-two-col", children=[
            html.Div(className="ml-control-card", children=[
                html.H3("Importância por classe"),
                html.P("Selecione uma classe para visualizar quais variáveis mais influenciam a tomada de decisão para aquele grupo específico."),
                dcc.Dropdown(
                    id="ml-shap-class-dropdown",
                    options=[{"label": c, "value": c} for c in SHAP_BY_CLASS.keys()],
                    value="Adequada", clearable=False,
                    className="var-dropdown ml-dropdown",
                ),
                dcc.Graph(id="ml-shap-class-chart", config={"displayModeBar": False}),
            ]),
            html.Div(className="ml-analysis-card compact", children=[
                html.H3("Insights ambientais"),
                html.P("As duas variáveis dominantes — Orthophosphate e Nitrogen — são marcadores clássicos de eutrofização: o processo de enriquecimento excessivo de corpos d'água por nutrientes que leva ao crescimento descontrolado de algas e à redução de oxigênio dissolvido."),
                html.P("A presença de variáveis categoriais como Effluent e Sewage entre as mais importantes reforça que o tipo de uso do corpo hídrico é um preditor relevante da qualidade ambiental, capturando o contexto de pressão antrópica ao qual o ponto está sujeito."),
                html.P("A Temperature, terceira variável mais relevante, conecta o modelo às dinâmicas sazonais e climáticas que modulam a biota aquática e aceleram processos de degradação."),
            ]),
        ]),
    ])

# ============================================================
#  SECTION 7 — SIMULADOR
# ============================================================

def make_simulator_section():
    return html.Section(id="simulador", className="ml-section", children=[
        section_header(
            "Simulador AquaSense",
            "Simulador de Qualidade da Água",
            "Teste o modelo final treinado pelo AquaSense utilizando diferentes condições ambientais.",
        ),
        html.Div(className="ml-simulator-card", children=[
            html.Div(className="ml-sim-inputs", children=[
                html.Div(className="ml-sim-field", children=[
                    html.Label("Temperatura (°C)", className="ml-sim-label"),
                    dcc.Input(id="sim-temperature", type="text", value="15.0",
                              placeholder="Ex: 15.0 ou 15,0", className="ml-sim-input"),
                ]),
                html.Div(className="ml-sim-field", children=[
                    html.Label("Ortofosfato (mg/L)", className="ml-sim-label"),
                    dcc.Input(id="sim-orthophosphate", type="text", value="0.5",
                              placeholder="Ex: 0.5 ou 0,03", className="ml-sim-input"),
                ]),
                html.Div(className="ml-sim-field", children=[
                    html.Label("Nitrogênio (mg/L)", className="ml-sim-label"),
                    dcc.Input(id="sim-nitrogen", type="text", value="2.0",
                              placeholder="Ex: 2.0 ou 0,003", className="ml-sim-input"),
                ]),
                html.Div(className="ml-sim-field", children=[
                    html.Label("País", className="ml-sim-label"),
                    dcc.Dropdown(
                        id="sim-country",
                        options=[{"label": c, "value": c} for c in COUNTRIES],
                        value="Ireland", clearable=False,
                        className="var-dropdown ml-dropdown ml-sim-dropdown",
                    ),
                ]),
                html.Div(className="ml-sim-field", children=[
                    html.Label("Tipo de Corpo Hídrico", className="ml-sim-label"),
                    dcc.Dropdown(
                        id="sim-waterbody",
                        options=[{"label": w, "value": w} for w in WATERBODY_TYPES],
                        value="River", clearable=False,
                        className="var-dropdown ml-dropdown ml-sim-dropdown",
                    ),
                ]),
            ]),
            html.Button(
                [ml_icon("lucide:play-circle", 18, "#011A18"), " Classificar Qualidade da Água"],
                id="sim-predict-btn",
                className="btn-primary ml-sim-btn",
                n_clicks=0,
            ),
            html.Div(id="sim-result", className="ml-sim-result"),
        ]),
    ])

# ============================================================
#  CLUSTERING SECTION (preserved exactly)
# ============================================================

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
    return html.Section(className="ml-section", children=[
        html.Div(className="ml-final-note", children=[
            html.Div(className="ml-final-icon", children=[ml_icon("lucide:sparkles", 28)]),
            html.H2("Síntese da modelagem"),
            html.P("A frente supervisionada — com LightGBM, 90,4% de acurácia e Macro F1 de 0,89 — demonstra a capacidade preditiva do AquaSense sobre condições ambientais reais. A clusterização com K-Means + PCA revela agrupamentos naturais nos dados, sem depender do rótulo. Juntas, as duas abordagens tornam o AquaSense mais robusto: uma classifica, a outra ajuda a interpretar padrões ambientais ocultos."),
        ]),
    ])

# ============================================================
#  LAYOUT ASSEMBLY
# ============================================================

def make_ml_layout():
    return html.Div(className="ml-page", children=[
        make_ml_hero(),
        make_ml_overview(),
        make_evolution_section(),
        make_final_model_section(),
        make_performance_section(),
        make_scenario_section(),
        make_interpretability_section(),
        make_simulator_section(),
        make_clustering_section(),
        make_ml_final_note(),
    ])

# ============================================================
#  INPUT PARSING / VALIDATION HELPERS
# ============================================================

def _parse_decimal(raw_value):
    """
    Parse a user-entered numeric string that may use either ',' or '.' as the
    decimal separator, and may have surrounding whitespace.

    Returns a float, or None if the value is genuinely empty / not numeric.
    Crucially: "0", "0.0", "0,03", "0.003" etc. are all valid and must NOT
    be treated as "empty" (the previous bug treated falsy-looking values as
    missing).
    """
    if raw_value is None:
        return None

    # Already numeric (e.g. came from a dcc.Input type="number")
    if isinstance(raw_value, (int, float)):
        # NaN check without importing math: NaN != NaN
        if raw_value != raw_value:
            return None
        return float(raw_value)

    text = str(raw_value).strip()
    if text == "":
        return None

    # Normalize decimal separator: only swap ',' -> '.' when it's being used
    # as a decimal mark (no thousands-separator support needed here since
    # these are small scientific magnitudes like 0,003).
    normalized = text.replace(",", ".")

    # Guard against multiple dots (e.g. "1.2.3") which would otherwise raise
    try:
        return float(normalized)
    except (TypeError, ValueError):
        return None


def _validate_numeric_field(raw_value, min_value=None, max_value=None):
    """
    Returns (value: float|None, is_valid: bool).
    is_valid is False only when the field is truly empty, non-numeric, or
    outside the allowed [min_value, max_value] range. Small numbers close to
    zero (0.03, 0.003, ...) are explicitly valid.
    """
    value = _parse_decimal(raw_value)
    if value is None:
        return None, False
    if min_value is not None and value < min_value:
        return value, False
    if max_value is not None and value > max_value:
        return value, False
    return value, True

# ============================================================
#  CALLBACKS
# ============================================================

def register_ml_callbacks(app):

    @app.callback(
        Output("ml-cluster-var-chart", "figure"),
        Input("ml-cluster-var-dropdown", "value"),
    )
    def update_cluster_var_chart(var_key):
        return build_cluster_variable_chart(var_key or "dbo")

    @app.callback(
        Output("ml-shap-class-chart", "figure"),
        Input("ml-shap-class-dropdown", "value"),
    )
    def update_shap_class_chart(class_name):
        return build_shap_by_class(class_name or "Adequada")

    @app.callback(
        Output("sim-result", "children"),
        Input("sim-predict-btn", "n_clicks"),
        State("sim-temperature",    "value"),
        State("sim-orthophosphate", "value"),
        State("sim-nitrogen",       "value"),
        State("sim-country",        "value"),
        State("sim-waterbody",      "value"),
        prevent_initial_call=True,
    )
    def run_prediction(n_clicks, temperature_raw, orthophosphate_raw, nitrogen_raw, country, waterbody):
        if not n_clicks:
            return []

        # Parse + validate all three numeric fields with the SAME logic,
        # accepting both ',' and '.' as decimal separators and allowing
        # small values near zero (e.g. 0.03, 0,003) without flagging them
        # as empty/invalid.
        temperature, temp_ok = _validate_numeric_field(temperature_raw)
        orthophosphate, ortho_ok = _validate_numeric_field(orthophosphate_raw, min_value=0)
        nitrogen, nitrogen_ok = _validate_numeric_field(nitrogen_raw, min_value=0)

        missing = []
        if not temp_ok:     missing.append("Temperatura")
        if not ortho_ok:     missing.append("Ortofosfato")
        if not nitrogen_ok:  missing.append("Nitrogênio")
        if not country:      missing.append("País")
        if not waterbody:    missing.append("Tipo de corpo hídrico")
        if missing:
            return html.Div(className="ml-sim-error", children=[
                ml_icon("lucide:alert-circle", 18, "#e25c72"),
                f" Preencha os campos: {', '.join(missing)}",
            ])

        if _MODEL is None:
            return html.Div(className="ml-sim-error", children=[
                ml_icon("lucide:alert-circle", 18, "#e25c72"),
                " Modelo não encontrado. Verifique se os arquivos .joblib estão na pasta models/.",
            ])

        try:
            sample = pd.DataFrame({
                "Temperature (cel)":    [float(temperature)],
                "Orthophosphate (mg/l)":[float(orthophosphate)],
                "Country":              [country],
                "Waterbody Type":       [waterbody],
                "Nitrogen (mg/l)":      [float(nitrogen)],
            })
            # Ensure column order matches exactly what the model was trained on
            sample = sample[_FEATURES]

            pred   = _MODEL.predict(sample)[0]
            probas = _MODEL.predict_proba(sample)[0]
            class_probas = list(zip(_CLASSES, probas))
            class_probas.sort(key=lambda x: x[1], reverse=True)

            interp_map = {
                "Adequada":      "Condição favorável de qualidade hídrica. Os parâmetros inseridos são compatíveis com um ambiente aquático preservado.",
                "Atenção":       "Condição intermediária que merece monitoramento. Alguns indicadores sugerem pressão ambiental que pode evoluir negativamente.",
                "Não adequada":  "Condição potencialmente comprometida e associada a maior risco ambiental. Recomenda-se investigação e intervenção.",
            }
            pred_display = pred if pred != "Não adequada" else "Não Adequada"
            badge_cls = {
                "Adequada":     "ml-class-badge--adequada",
                "Atenção":      "ml-class-badge--atencao",
                "Não adequada": "ml-class-badge--nao",
            }.get(pred, "")

            prob_bars = []
            for cls, prob in class_probas:
                cls_display = cls if cls != "Não adequada" else "Não Adequada"
                bar_color = CLASS_COLORS.get(cls_display, CLASS_COLORS.get(cls, "#3fffe7"))
                prob_bars.append(
                    html.Div(className="ml-prob-row", children=[
                        html.Span(cls_display, className="ml-prob-label"),
                        html.Div(className="ml-prob-bar-wrap", children=[
                            html.Div(className="ml-prob-bar", style={"width": f"{prob*100:.1f}%", "background": bar_color}),
                        ]),
                        html.Span(f"{prob*100:.1f}%", className="ml-prob-pct"),
                    ])
                )

            return html.Div(className="ml-sim-output", children=[
                html.Div(className="ml-sim-prediction", children=[
                    html.Span("Resultado:", className="ml-sim-result-label"),
                    html.Span(pred_display, className=f"ml-class-badge {badge_cls} ml-sim-pred-badge"),
                ]),
                html.Div(className="ml-prob-bars", children=prob_bars),
                html.P(interp_map.get(pred, ""), className="ml-sim-interpretation"),
            ])

        except Exception as exc:
            return html.Div(className="ml-sim-error", children=[
                ml_icon("lucide:alert-circle", 18, "#e25c72"),
                f" Erro ao executar previsão: {str(exc)}",
            ])