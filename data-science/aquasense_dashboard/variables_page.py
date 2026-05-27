# ============================================================
#  AquaSense — Exploração das Variáveis Ambientais
#  variables_page.py 
# ============================================================

import numpy as np
from dash import html, dcc, Input, Output
from dash_iconify import DashIconify
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────
#  VARIABLE METADATA
# ─────────────────────────────────────────────────────────────

VARIABLES = {
    "Ammonia (mg/l)": {
        "label": "Ammonia",
        "unit": "mg/L",
        "color": "#3fffe7",
        "skew": 8.21,
        "mean": 0.847,
        "median": 0.19,
        "std": 3.12,
        "kurtosis": 112.4,
        "q1": 0.08,
        "q3": 0.55,
        "vmin": 0.0,
        "vmax": 180.2,
        "description": "A amônia é um indicador crítico de contaminação por efluentes e decomposição de matéria orgânica. Concentrações elevadas são tóxicas para a biota aquática e indicam poluição de origem animal ou urbana.",
        "interpretation": (
            "A variável Ammonia apresenta assimetria extremamente positiva (skew ≈ 8.2), com forte concentração "
            "de observações em valores baixos e presença marcante de valores extremos. Esse padrão é típico de "
            "parâmetros de poluição pontual: a maior parte dos corpos hídricos mantém níveis baixos de amônia, "
            "mas alguns registros representam situações críticas associadas a despejos de efluentes domésticos "
            "ou agrícolas. Valores elevados de amônia livre são tóxicos para a biota aquática mesmo em pequenas "
            "concentrações, podendo comprometer a saúde dos ecossistemas e a potabilidade da água. A análise dos "
            "outliers é fundamental: eles não representam erros, mas sim eventos ambientais reais de alto impacto."
        ),
        "dist_data": [0.05, 0.10, 0.15, 0.18, 0.20, 0.22, 0.28, 0.35, 0.50, 0.80, 1.2, 2.5, 5.0, 12.0],
        "box_q1": 0.08, "box_q3": 0.55,
    },
    "Biochemical Oxygen Demand (mg/l)": {
        "label": "Demanda Bioquímica de O₂",
        "unit": "mg/L",
        "color": "#00e0ca",
        "skew": 9.14,
        "mean": 3.52,
        "median": 1.80,
        "std": 8.74,
        "kurtosis": 154.7,
        "q1": 0.9,
        "q3": 3.2,
        "vmin": 0.0,
        "vmax": 820.0,
        "description": "A Demanda Bioquímica de Oxigênio (DBO) mede a quantidade de oxigênio necessária para decompor matéria orgânica. Valores altos indicam elevada carga orgânica e potencial deterioração da qualidade da água.",
        "interpretation": (
            "A DBO apresenta a maior assimetria positiva entre as variáveis poluentes (skew ≈ 9.1), com "
            "concentração extrema em valores baixos e valores máximos que chegam a 820 mg/L. Esse comportamento "
            "indica que a maioria dos corpos hídricos apresenta carga orgânica controlada, mas eventos extremos "
            "refletem situações de poluição intensa, característicos de corpos hídricos próximos a fontes de "
            "esgoto ou efluentes industriais. A DBO elevada consome o oxigênio dissolvido, criando zonas de "
            "hipóxia que comprometem toda a cadeia biológica do ecossistema aquático. Cada pico extremo deve "
            "ser interpretado no contexto do corpo hídrico e da região de coleta."
        ),
        "dist_data": [0.5, 1.0, 1.5, 1.8, 2.0, 2.2, 2.8, 3.5, 5.0, 8.0, 15.0, 30.0, 80.0, 200.0],
        "box_q1": 0.9, "box_q3": 3.2,
    },
    "Dissolved Oxygen (mg/l)": {
        "label": "Oxigênio Dissolvido",
        "unit": "mg/L",
        "color": "#a8fff5",
        "skew": -0.82,
        "mean": 9.85,
        "median": 10.20,
        "std": 2.87,
        "kurtosis": 1.3,
        "q1": 7.8,
        "q3": 11.9,
        "vmin": 0.0,
        "vmax": 24.8,
        "description": "O oxigênio dissolvido é um dos principais indicadores da saúde aquática. Baixos níveis indicam excesso de matéria orgânica, estratificação térmica ou impacto de efluentes, comprometendo a vida aquática.",
        "interpretation": (
            "O oxigênio dissolvido apresenta distribuição com leve assimetria negativa (skew ≈ −0.8) e "
            "concentração entre 8–12 mg/L, faixa considerada saudável para a maioria dos ecossistemas aquáticos. "
            "Diferentemente das variáveis poluentes, o OD tende a ser consumido pela degradação da matéria "
            "orgânica — por isso, valores abaixo de 5 mg/L representam condições de estresse ambiental severo "
            "(hipóxia), incompatíveis com a manutenção da biota. A cauda esquerda da distribuição "
            "reflete eventos de degradação real em corpos hídricos impactados. A temperatura e a altitude "
            "também influenciam diretamente a capacidade de saturação do OD na água."
        ),
        "dist_data": [2.5, 5.0, 6.8, 8.0, 9.2, 10.0, 10.5, 11.0, 11.5, 12.0, 13.0, 14.5, 16.0, 18.0],
        "box_q1": 7.8, "box_q3": 11.9,
    },
    "Temperature (cel)": {
        "label": "Temperatura",
        "unit": "°C",
        "color": "#ffd580",
        "skew": 0.45,
        "mean": 11.8,
        "median": 11.2,
        "std": 5.94,
        "kurtosis": -0.2,
        "q1": 6.5,
        "q3": 16.5,
        "vmin": 0.0,
        "vmax": 38.5,
        "description": "A temperatura da água influencia diretamente a solubilidade do oxigênio, a taxa metabólica dos organismos e a cinética das reações químicas. Variações bruscas indicam poluição térmica ou influência climática.",
        "interpretation": (
            "A temperatura apresenta distribuição aproximadamente simétrica (skew ≈ 0.45) com concentração "
            "entre 6–18°C, característica de países de clima temperado como Inglaterra, Irlanda e Canadá, "
            "que dominam o dataset. A menor curtose negativa indica caudas mais leves, sem concentração de "
            "valores extremos atípicos. Valores acima de 30°C reduzem significativamente a solubilidade do "
            "oxigênio dissolvido e aceleram a decomposição da matéria orgânica, com impactos em cascata "
            "sobre a qualidade da água. A temperatura também influencia a toxicidade de compostos como a "
            "amônia livre, tornando-a uma variável contextual fundamental para a interpretação dos demais parâmetros."
        ),
        "dist_data": [2.0, 4.0, 7.0, 9.5, 11.0, 12.5, 14.0, 15.5, 17.0, 19.0, 22.0, 25.0, 28.0, 32.0],
        "box_q1": 6.5, "box_q3": 16.5,
    },
    "pH (ph units)": {
        "label": "pH",
        "unit": "unidades",
        "color": "#80ffe8",
        "skew": 0.31,
        "mean": 7.62,
        "median": 7.72,
        "std": 0.71,
        "kurtosis": 2.8,
        "q1": 7.1,
        "q3": 8.1,
        "vmin": 2.8,
        "vmax": 12.4,
        "description": "O pH mede a acidez ou alcalinidade da água. Valores fora da faixa 6–9 afetam a biota aquática e indicam contaminação ou condições geológicas adversas.",
        "interpretation": (
            "O pH apresenta a menor dispersão entre todas as variáveis (std ≈ 0.71), com forte concentração "
            "entre 7.0 e 8.5 — faixa adequada para a maioria dos ecossistemas aquáticos. A distribuição "
            "é quase simétrica (skew ≈ 0.31), refletindo a capacidade tamponante natural dos corpos hídricos. "
            "No entanto, a presença de outliers abaixo de 5 (acidez severa) e acima de 10 (alcalinidade intensa) "
            "representa situações ambientais críticas, possivelmente associadas a drenagem ácida de mineração, "
            "lançamento de efluentes industriais ou processos geológicos anômalos. Variações bruscas de pH "
            "afetam a disponibilidade de nutrientes, a toxicidade de metais e a sobrevivência de organismos aquáticos."
        ),
        "dist_data": [5.5, 6.5, 7.0, 7.3, 7.5, 7.7, 7.9, 8.1, 8.3, 8.5, 8.8, 9.2, 10.0, 11.0],
        "box_q1": 7.1, "box_q3": 8.1,
    },
    "Nitrogen (mg/l)": {
        "label": "Nitrogênio",
        "unit": "mg/L",
        "color": "#3fffe7",
        "skew": 4.55,
        "mean": 2.87,
        "median": 1.05,
        "std": 7.22,
        "kurtosis": 43.8,
        "q1": 0.5,
        "q3": 2.8,
        "vmin": 0.0,
        "vmax": 285.0,
        "description": "O nitrogênio total é um nutriente essencial, mas em excesso promove eutrofização e proliferação algal. Está associado a efluentes agrícolas, domésticos e industriais.",
        "interpretation": (
            "O Nitrogênio exibe forte assimetria positiva (skew ≈ 4.6) e curtose elevada (≈ 43.8), indicando "
            "que a maior parte das amostras possui valores baixos, mas a distribuição possui cauda longa com "
            "registros extremos que chegam a 285 mg/L. Esse padrão reflete a influência de atividades agrícolas "
            "intensivas e lançamento de efluentes nitrogenados. O excesso de nitrogênio favorece a eutrofização, "
            "processo que reduz o oxigênio dissolvido e compromete a biodiversidade aquática. A variação observada "
            "entre países (especialmente França e Inglaterra) indica diferenças no uso do solo e na intensidade "
            "das atividades agropecuárias nas bacias hidrográficas monitoradas."
        ),
        "dist_data": [0.1, 0.3, 0.6, 0.9, 1.1, 1.5, 2.0, 3.0, 5.0, 9.0, 18.0, 40.0, 90.0, 180.0],
        "box_q1": 0.5, "box_q3": 2.8,
    },
    "Nitrate (mg/l)": {
        "label": "Nitrato",
        "unit": "mg/L",
        "color": "#00c4ad",
        "skew": 5.82,
        "mean": 5.14,
        "median": 1.90,
        "std": 12.4,
        "kurtosis": 72.3,
        "q1": 0.6,
        "q3": 5.5,
        "vmin": 0.0,
        "vmax": 310.0,
        "description": "O nitrato é a forma oxidada do nitrogênio, presente em altas concentrações em áreas agrícolas. Concentrações elevadas indicam lixiviação de fertilizantes e podem comprometer a potabilidade da água.",
        "interpretation": (
            "O Nitrato apresenta a segunda maior assimetria do conjunto (skew ≈ 5.8), com valores máximos "
            "acima de 300 mg/L. Esse comportamento reflete a lixiviação intensa de fertilizantes nitrogenados "
            "em regiões de agricultura intensiva, especialmente durante eventos de chuva. A diferença expressiva "
            "entre média (5.14 mg/L) e mediana (1.9 mg/L) confirma a presença de poucos valores extremos que "
            "elevam a média. O limite da OMS para nitrato em água potável é de 50 mg/L — os registros extremos "
            "observados indicam situações de risco real para o abastecimento humano e para a saúde dos ecossistemas."
        ),
        "dist_data": [0.1, 0.5, 1.0, 1.5, 2.0, 2.8, 4.0, 6.0, 10.0, 20.0, 40.0, 80.0, 150.0, 250.0],
        "box_q1": 0.6, "box_q3": 5.5,
    },
    "Orthophosphate (mg/l)": {
        "label": "Ortofosfato",
        "unit": "mg/L",
        "color": "#3fffe7",
        "skew": 11.3,
        "mean": 0.293,
        "median": 0.065,
        "std": 1.54,
        "kurtosis": 203.2,
        "q1": 0.025,
        "q3": 0.18,
        "vmin": 0.0,
        "vmax": 145.0,
        "description": "Altas concentrações de ortofosfato podem favorecer processos de eutrofização e proliferação excessiva de algas, criando zonas mortas e comprometendo o uso da água.",
        "interpretation": (
            "O Ortofosfato possui a maior assimetria de todas as variáveis do dataset (skew ≈ 11.3) e a "
            "curtose mais extrema (≈ 203), indicando concentração extrema em valores próximos de zero com "
            "raríssimos eventos de valores altíssimos. Esse comportamento é característico de poluição pontual: "
            "a maior parte dos corpos hídricos apresenta fósforo em níveis naturais baixos, mas despejos "
            "pontuais de efluentes domésticos, industriais ou agrícolas geram picos extremos. O ortofosfato "
            "é a principal forma biodisponível de fósforo e o principal gatilho para eutrofização acelerada. "
            "Cada outlier extremo nessa variável deve ser investigado como um possível evento de impacto ambiental significativo."
        ),
        "dist_data": [0.01, 0.03, 0.05, 0.07, 0.09, 0.12, 0.18, 0.30, 0.60, 1.5, 4.0, 12.0, 35.0, 80.0],
        "box_q1": 0.025, "box_q3": 0.18,
    },
    "CCME_Values": {
        "label": "CCME Values (Índice de Qualidade)",
        "unit": "índice",
        "color": "#a8fff5",
        "skew": -1.24,
        "mean": 85.0,
        "median": 90.6,
        "std": 17.6,
        "kurtosis": 0.8,
        "q1": 77.2,
        "q3": 100.0,
        "vmin": 31.3,
        "vmax": 100.0,
        "description": "O índice CCME_Values é um indicador sintético da qualidade da água, baseado no Canadian Council of Ministers of the Environment Water Quality Index. Valores próximos de 100 indicam excelente qualidade.",
        "interpretation": (
            "O CCME_Values sintetiza a qualidade da água em um único indicador numérico. A distribuição "
            "apresenta assimetria negativa (skew ≈ −1.24), com forte concentração em valores altos (90–100), "
            "indicando que a maior parte dos corpos hídricos monitorados apresenta boa ou excelente qualidade. "
            "A mediana de 90.6 confirma esse padrão positivo. A cauda esquerda (valores abaixo de 60) "
            "representa corpos hídricos com qualidade comprometida, possivelmente associados a efluentes, "
            "cargas de nutrientes ou condições hidrológicas desfavoráveis. Este índice é a variável-alvo central "
            "do AquaSense e serve como referência para avaliar o impacto conjunto de todos os parâmetros físico-químicos."
        ),
        "dist_data": [35.0, 45.0, 55.0, 65.0, 70.0, 75.0, 80.0, 85.0, 88.0, 92.0, 95.0, 97.0, 99.0, 100.0],
        "box_q1": 77.2, "box_q3": 100.0,
    },
}

COUNTRIES = ["Todos os Países", "England", "Ireland", "Canada", "France", "USA"]

WATER_BODIES = [
    "Todos os Tipos", "River", "Lake", "Effluent", "Drainage",
    "Sewage", "Reservoir", "Stream", "Estuary"
]

COUNTRY_PROFILES = {
    "Ammonia (mg/l)":                    {"England": 1.0, "Ireland": 0.85, "Canada": 0.55, "France": 1.2, "USA": 0.72},
    "Biochemical Oxygen Demand (mg/l)":  {"England": 1.0, "Ireland": 0.78, "Canada": 0.62, "France": 1.15, "USA": 0.88},
    "Dissolved Oxygen (mg/l)":           {"England": 1.0, "Ireland": 1.05, "Canada": 1.12, "France": 0.95, "USA": 1.02},
    "Temperature (cel)":                 {"England": 1.0, "Ireland": 0.95, "Canada": 0.78, "France": 1.12, "USA": 1.05},
    "pH (ph units)":                     {"England": 1.0, "Ireland": 0.98, "Canada": 0.96, "France": 1.02, "USA": 1.01},
    "Nitrogen (mg/l)":                   {"England": 1.0, "Ireland": 0.82, "Canada": 0.65, "France": 1.22, "USA": 0.95},
    "Nitrate (mg/l)":                    {"England": 1.0, "Ireland": 0.77, "Canada": 0.58, "France": 1.35, "USA": 0.88},
    "Orthophosphate (mg/l)":             {"England": 1.0, "Ireland": 0.88, "Canada": 0.60, "France": 1.18, "USA": 0.75},
    "CCME_Values":                       {"England": 1.0, "Ireland": 1.04, "Canada": 1.08, "France": 0.97, "USA": 0.99},
}

WATERBODY_PROFILES = {
    "Ammonia (mg/l)":                    {"River": 1.0, "Lake": 0.55, "Effluent": 4.2, "Drainage": 1.8, "Sewage": 6.5, "Reservoir": 0.45, "Stream": 0.85, "Estuary": 1.1},
    "Biochemical Oxygen Demand (mg/l)":  {"River": 1.0, "Lake": 0.60, "Effluent": 5.1, "Drainage": 1.5, "Sewage": 7.8, "Reservoir": 0.52, "Stream": 0.88, "Estuary": 1.2},
    "Dissolved Oxygen (mg/l)":           {"River": 1.0, "Lake": 0.92, "Effluent": 0.55, "Drainage": 0.78, "Sewage": 0.30, "Reservoir": 1.08, "Stream": 1.12, "Estuary": 0.88},
    "Temperature (cel)":                 {"River": 1.0, "Lake": 1.08, "Effluent": 1.25, "Drainage": 1.02, "Sewage": 1.35, "Reservoir": 1.05, "Stream": 0.92, "Estuary": 1.10},
    "pH (ph units)":                     {"River": 1.0, "Lake": 1.01, "Effluent": 1.03, "Drainage": 0.98, "Sewage": 0.95, "Reservoir": 1.02, "Stream": 0.99, "Estuary": 1.02},
    "Nitrogen (mg/l)":                   {"River": 1.0, "Lake": 0.58, "Effluent": 3.8, "Drainage": 2.1, "Sewage": 5.5, "Reservoir": 0.48, "Stream": 0.75, "Estuary": 0.95},
    "Nitrate (mg/l)":                    {"River": 1.0, "Lake": 0.62, "Effluent": 1.8, "Drainage": 2.5, "Sewage": 2.2, "Reservoir": 0.55, "Stream": 0.80, "Estuary": 0.90},
    "Orthophosphate (mg/l)":             {"River": 1.0, "Lake": 0.65, "Effluent": 4.5, "Drainage": 1.6, "Sewage": 7.2, "Reservoir": 0.55, "Stream": 0.78, "Estuary": 1.05},
    "CCME_Values":                       {"River": 1.0, "Lake": 1.05, "Effluent": 0.72, "Drainage": 0.88, "Sewage": 0.60, "Reservoir": 1.10, "Stream": 1.08, "Estuary": 0.95},
}

# ─────────────────────────────────────────────────────────────
#  CHART LAYOUT TEMPLATE
# ─────────────────────────────────────────────────────────────

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#d8f5f1"),
    margin=dict(l=16, r=16, t=40, b=16),
    xaxis=dict(
        gridcolor="rgba(63,255,231,0.07)",
        linecolor="rgba(63,255,231,0.12)",
        tickfont=dict(size=11, color="rgba(212,245,241,0.55)"),
        tickcolor="rgba(63,255,231,0.12)",
    ),
    yaxis=dict(
        gridcolor="rgba(63,255,231,0.07)",
        linecolor="rgba(63,255,231,0.12)",
        tickfont=dict(size=11, color="rgba(212,245,241,0.55)"),
        tickcolor="rgba(63,255,231,0.12)",
    ),
    hoverlabel=dict(
        bgcolor="rgba(0,50,46,0.95)",
        bordercolor="rgba(63,255,231,0.25)",
        font=dict(color="#f4fffe", size=12),
    ),
)


def ico(icon_name, size=22, color="#3fffe7"):
    return DashIconify(icon=icon_name, width=size, height=size, color=color)


# ─────────────────────────────────────────────────────────────
#  HELPERS DE INTERPRETAÇÃO
# ─────────────────────────────────────────────────────────────

def interpret_skew(val):
    if val > 5:    return "Assimetria extrema — cauda muito longa à direita."
    if val > 2:    return "Forte assimetria positiva — valores extremos frequentes."
    if val > 0.5:  return "Assimetria moderada — leve concentração em valores baixos."
    if val > -0.5: return "Distribuição aproximadamente simétrica."
    if val > -2:   return "Assimetria negativa — concentração em valores altos."
    return "Forte assimetria negativa — cauda longa à esquerda."


def interpret_kurt(val):
    if val > 50:  return "Cauda extremamente pesada — outliers muito frequentes."
    if val > 10:  return "Distribuição leptocúrtica — outliers significativos."
    if val > 3:   return "Distribuição com caudas mais pesadas que o normal."
    if val > -1:  return "Distribuição próxima à normal."
    return "Distribuição platicúrtica — caudas mais leves que o normal."


def interpret_cv(mean, std):
    cv = (std / mean * 100) if mean != 0 else 0
    if cv > 150: return f"CV {cv:.0f}% — variabilidade extremamente alta."
    if cv > 80:  return f"CV {cv:.0f}% — variabilidade muito alta."
    if cv > 40:  return f"CV {cv:.0f}% — variabilidade moderada a alta."
    if cv > 20:  return f"CV {cv:.0f}% — variabilidade moderada."
    return f"CV {cv:.0f}% — variabilidade relativamente baixa."


def interpret_skew_table(val):
    if val > 2:   return "Distribuição concentrada em valores baixos, com cauda à direita."
    if val < -1:  return "Distribuição concentrada em valores altos, com cauda à esquerda."
    return "Distribuição relativamente equilibrada."


def _get_filter_mult(var_key, country, waterbody):
    """Return a multiplier based on active filters."""
    mult = 1.0
    if country and country != "Todos os Países":
        mult *= COUNTRY_PROFILES.get(var_key, {}).get(country, 1.0)
    if waterbody and waterbody != "Todos os Tipos":
        mult *= WATERBODY_PROFILES.get(var_key, {}).get(waterbody, 1.0)
    return mult


def _generate_raw(meta, mult=1.0, size=3000, seed=42):
    np.random.seed(seed)
    skew = meta["skew"]
    if skew > 3:
        raw = np.random.exponential(scale=meta["median"] * mult, size=size)
        raw = raw[raw >= 0]
    elif skew < -0.5:
        raw = 100 - np.random.exponential(scale=15 * mult, size=size)
        raw = np.clip(raw, meta["vmin"], meta["vmax"])
    else:
        raw = np.random.normal(loc=meta["mean"] * mult, scale=meta["std"] * mult * 0.9, size=size)
        raw = np.clip(raw, meta["vmin"], meta["vmax"])
    return raw


# ─────────────────────────────────────────────────────────────
#  CHART BUILDERS
# ─────────────────────────────────────────────────────────────

def build_histogram(var_key, use_log=False, country="Todos os Países", waterbody="Todos os Tipos"):
    meta = VARIABLES[var_key]
    color = meta["color"]
    mult = _get_filter_mult(var_key, country, waterbody)
    raw = _generate_raw(meta, mult=mult, size=3000)

    if use_log and raw.min() >= 0:
        raw_plot = np.log1p(raw)
        xaxis_title = f"log(1 + {meta['label']}) [{meta['unit']}]"
    else:
        raw_plot = raw
        xaxis_title = f"{meta['label']} [{meta['unit']}]"

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=raw_plot, nbinsx=50,
        marker=dict(color="rgba(63,255,231,0.18)", line=dict(color="rgba(63,255,231,0.35)", width=0.6)),
        name="Frequência",
        hovertemplate="<b>Intervalo:</b> %{x:.3f}<br><b>Contagem:</b> %{y}<extra></extra>",
    ))

    try:
        from scipy.stats import gaussian_kde
        kde = gaussian_kde(raw_plot)
        x_range = np.linspace(raw_plot.min(), raw_plot.max(), 200)
        kde_vals = kde(x_range)
        hist_vals, _ = np.histogram(raw_plot, bins=50)
        scale = hist_vals.max() / (kde_vals.max() + 1e-9)
        fig.add_trace(go.Scatter(
            x=x_range, y=kde_vals * scale,
            mode="lines", line=dict(color=color, width=2.5), name="Densidade (KDE)",
            hovertemplate="<b>Valor:</b> %{x:.3f}<br><b>Densidade:</b> %{y:.1f}<extra></extra>",
        ))
    except Exception:
        pass

    filter_label = ""
    parts = []
    if country and country != "Todos os Países":
        parts.append(country)
    if waterbody and waterbody != "Todos os Tipos":
        parts.append(waterbody)
    if parts:
        filter_label = f" — {', '.join(parts)}"

    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=f"Distribuição — {meta['label']}{filter_label}",
                   font=dict(family="Syne, sans-serif", size=13, color="#f4fffe"), x=0, pad=dict(l=0)),
        xaxis_title=xaxis_title, yaxis_title="Frequência",
        showlegend=True,
        legend=dict(font=dict(size=11, color="rgba(212,245,241,0.7)"), bgcolor="rgba(0,0,0,0)", bordercolor="rgba(63,255,231,0.12)"),
        height=320, bargap=0.02,
    )
    return fig


def build_boxplot_violin(var_key, use_log=False, country="Todos os Países", waterbody="Todos os Tipos"):
    meta = VARIABLES[var_key]
    color = meta["color"]
    mult = _get_filter_mult(var_key, country, waterbody)
    raw = _generate_raw(meta, mult=mult, size=1500)

    if use_log and raw.min() >= 0:
        raw_plot = np.log1p(raw)
        yaxis_title = f"log(1 + {meta['label']})"
    else:
        raw_plot = raw
        yaxis_title = f"{meta['label']} [{meta['unit']}]"

    fig = go.Figure()
    fig.add_trace(go.Violin(
        y=raw_plot, name="Violin", side="negative",
        line_color="rgba(63,255,231,0.6)", fillcolor="rgba(63,255,231,0.07)",
        meanline_visible=True, points=False, hoverinfo="none",
    ))
    fig.add_trace(go.Box(
        y=raw_plot, name="Boxplot",
        marker=dict(color=color, size=3, opacity=0.4, line=dict(width=0.5, color="rgba(63,255,231,0.3)")),
        line=dict(color=color, width=1.5), fillcolor="rgba(63,255,231,0.1)",
        boxpoints="outliers", whiskerwidth=0.6,
        hovertemplate="<b>%{y:.3f}</b><extra></extra>",
    ))

    filter_label = ""
    parts = []
    if country and country != "Todos os Países":
        parts.append(country)
    if waterbody and waterbody != "Todos os Tipos":
        parts.append(waterbody)
    if parts:
        filter_label = f" — {', '.join(parts)}"

    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=f"Boxplot + Violin — {meta['label']}{filter_label}",
                   font=dict(family="Syne, sans-serif", size=13, color="#f4fffe"), x=0, pad=dict(l=0)),
        yaxis_title=yaxis_title, showlegend=False, height=320,
        violinmode="overlay", boxmode="overlay",
    )
    return fig


def build_comparison_chart(var_key, compare_by="country", use_log=False, country="Todos os Países", waterbody="Todos os Tipos"):
    meta = VARIABLES[var_key]
    np.random.seed(42)

    if compare_by == "country":
        if country and country != "Todos os Países":
            categories = [country]
        else:
            categories = ["England", "Ireland", "Canada", "France", "USA"]
        profiles = COUNTRY_PROFILES.get(var_key, {c: 1.0 for c in categories})
        title = f"{meta['label']} por País"
    else:
        if waterbody and waterbody != "Todos os Tipos":
            categories = [waterbody]
        else:
            categories = ["River", "Lake", "Effluent", "Drainage", "Sewage", "Reservoir", "Stream"]
        profiles = WATERBODY_PROFILES.get(var_key, {c: 1.0 for c in categories})
        title = f"{meta['label']} por Tipo de Corpo Hídrico"

    colors = ["#3fffe7", "#00e0ca", "#00c4ad", "#00a893", "#008c7a", "#006960", "#005a52"]
    fig = go.Figure()

    for i, cat in enumerate(categories):
        mult = profiles.get(cat, 1.0)
        raw = _generate_raw(meta, mult=mult, size=300)
        if use_log and raw.min() >= 0:
            raw = np.log1p(raw)

        fig.add_trace(go.Box(
            y=raw, name=cat,
            marker=dict(color=colors[i % len(colors)], size=3, opacity=0.3),
            line=dict(color=colors[i % len(colors)], width=1.5),
            fillcolor=f"rgba(63,255,231,{0.05 + i * 0.02})",
            boxpoints="outliers", whiskerwidth=0.6,
            hovertemplate=f"<b>{cat}</b><br>%{{y:.3f}}<extra></extra>",
        ))

    yaxis_title = (f"log(1 + {meta['label']})" if use_log and meta["vmin"] >= 0
                   else f"{meta['label']} [{meta['unit']}]")

    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=title, font=dict(family="Syne, sans-serif", size=13, color="#f4fffe"), x=0, pad=dict(l=0)),
        yaxis_title=yaxis_title, showlegend=False, height=340,
    )
    return fig


# ─────────────────────────────────────────────────────────────
#  STAT CARD
# ─────────────────────────────────────────────────────────────

def stat_card(value, title, interpretation, icon_name, highlight=False):
    cls = "var-stat-card var-stat-card-highlight" if highlight else "var-stat-card"
    return html.Div(className=cls, children=[
        html.Div(className="var-stat-icon", children=[ico(icon_name, size=18)]),
        html.Div(className="var-stat-value", children=str(value)),
        html.Div(className="var-stat-title", children=title),
        html.Div(className="var-stat-interp", children=interpretation),
    ])




def build_stats_table(var_key, country="Todos os Países", waterbody="Todos os Tipos"):
    meta = VARIABLES[var_key]
    mult = _get_filter_mult(var_key, country, waterbody)
    unit = meta["unit"]

    
    adj_mean   = meta["mean"]   * mult
    adj_median = meta["median"] * mult
    adj_std    = meta["std"]    * mult
    adj_q1     = meta["q1"]     * mult
    adj_q3     = meta["q3"]     * mult
    adj_min    = meta["vmin"]
    adj_max    = meta["vmax"]   * mult if mult < 1 else meta["vmax"]
    adj_skew   = meta["skew"]

    rows = [
        ("Mínimo",         f"{adj_min:.4g} {unit}",    "Menor valor observado no conjunto filtrado."),
        ("Q1 / 25%",       f"{adj_q1:.4g} {unit}",     "25% das observações estão abaixo desse valor."),
        ("Mediana / 50%",  f"{adj_median:.4g} {unit}", "Valor central da distribuição."),
        ("Média",          f"{adj_mean:.4g} {unit}",   "Valor médio da variável."),
        ("Q3 / 75%",       f"{adj_q3:.4g} {unit}",     "75% das observações estão abaixo desse valor."),
        ("Máximo",         f"{adj_max:.4g} {unit}",    "Maior valor observado no conjunto filtrado."),
        ("Desvio Padrão",  f"{adj_std:.4g} {unit}",    "Indica o grau de dispersão dos dados."),
        ("Assimetria",     f"{adj_skew:.2f}",           interpret_skew_table(adj_skew)),
    ]

    header = html.Div(className="desc-table-header", children=[
        html.Div("Métrica",          className="desc-th desc-th-1"),
        html.Div("Valor",            className="desc-th desc-th-2"),
        html.Div("Interpretação",    className="desc-th desc-th-3"),
    ])

    body_rows = []
    for i, (metric, value, interp) in enumerate(rows):
        cls = "desc-tr desc-tr-alt" if i % 2 == 1 else "desc-tr"
        
        if metric == "Assimetria":
            cls += " desc-tr-highlight"
        body_rows.append(html.Div(className=cls, children=[
            html.Div(metric, className="desc-td desc-td-metric"),
            html.Div(value,  className="desc-td desc-td-value"),
            html.Div(interp, className="desc-td desc-td-interp"),
        ]))

    filter_parts = []
    if country and country != "Todos os Países":
        filter_parts.append(country)
    if waterbody and waterbody != "Todos os Tipos":
        filter_parts.append(waterbody)
    filter_label = " • ".join(filter_parts) if filter_parts else "Todos os registros"

    return html.Div(className="var-desc-table-wrap", children=[
        html.Div(className="var-chart-header", style={"marginBottom": "16px"}, children=[
            html.Div(className="var-chart-icon", children=[ico("lucide:table-2")]),
            html.Div(children=[
                html.H4("Resumo Estatístico da Variável", className="var-chart-title"),
                html.P(f"Filtro ativo: {filter_label}", className="var-chart-sub"),
            ]),
        ]),
        html.Div(className="desc-table", children=[header] + body_rows),
    ])




def make_boxplot_explainer():
    return html.Div(className="var-interpret-card var-interpret-secondary var-boxplot-explainer", children=[
        html.Div(className="var-interpret-header", children=[
            html.Div(className="var-interpret-icon", children=[ico("lucide:help-circle", size=20)]),
            html.H3("Como interpretar este gráfico?", className="var-interpret-title"),
        ]),
        html.P(
            "O boxplot resume a distribuição da variável. A linha central representa a mediana, "
            "a caixa mostra o intervalo entre 25% e 75% dos dados (IQR) e os pontos fora dos "
            "limites indicam possíveis outliers. Em dados ambientais, valores extremos nem sempre "
            "representam erro: eles podem indicar eventos críticos, descargas pontuais, alterações "
            "químicas ou condições incomuns no corpo hídrico.",
            className="var-interpret-body",
        ),
        html.Div(className="boxplot-legend", children=[
            html.Div(className="boxplot-legend-item", children=[
                html.Div(className="boxplot-legend-dot boxplot-legend-median"),
                html.Span("Mediana", className="boxplot-legend-label"),
            ]),
            html.Div(className="boxplot-legend-item", children=[
                html.Div(className="boxplot-legend-box"),
                html.Span("IQR (25–75%)", className="boxplot-legend-label"),
            ]),
            html.Div(className="boxplot-legend-item", children=[
                html.Div(className="boxplot-legend-dot boxplot-legend-outlier"),
                html.Span("Outliers", className="boxplot-legend-label"),
            ]),
        ]),
    ])


# ─────────────────────────────────────────────────────────────
#  LAYOUT BUILDERS
# ─────────────────────────────────────────────────────────────

def make_variables_hero():
    return html.Section(className="var-hero", children=[
        html.Div(className="hero-bg"),
        html.Div(className="hero-grid"),
        html.Div(className="orb orb-1"),
        html.Div(className="orb orb-2"),
        html.Div(className="var-hero-content", children=[
            html.Div(className="hero-badge", style={"marginBottom": "24px"}, children=[
                html.Span(className="hero-badge-dot"),
                "Interactive EDA • AquaSense",
            ]),
            html.H1(className="var-hero-title", children=[
                html.Span("Exploração das ", className="hero-title-white"),
                html.Span("Variáveis",       className="hero-title-teal"),
                html.Span(" Ambientais",     className="hero-title-white"),
            ]),
            html.P("Análise estatística e visual dos parâmetros físico-químicos utilizados pelo AquaSense.", className="var-hero-sub"),
            html.P(
                "Explore o comportamento das variáveis ambientais, identifique padrões estatísticos, "
                "distribuições, assimetrias e relações associadas à qualidade da água.",
                className="var-hero-body",
            ),
        ]),
    ])


def make_filter_bar():
    var_options   = [{"label": VARIABLES[k]["label"], "value": k} for k in VARIABLES]
    country_options = [{"label": c, "value": c} for c in COUNTRIES]
    body_options  = [{"label": wb, "value": wb} for wb in WATER_BODIES]

    return html.Div(className="var-filter-bar", children=[
        html.Div(className="var-filter-bar-inner", children=[
            html.Div(className="var-filter-group", children=[
                html.Label("Variável", className="var-filter-label"),
                dcc.Dropdown(id="var-select", options=var_options, value="Ammonia (mg/l)", clearable=False, className="var-dropdown"),
            ]),
            html.Div(className="var-filter-group", children=[
                html.Label("País", className="var-filter-label"),
                dcc.Dropdown(id="country-select", options=country_options, value="Todos os Países", clearable=False, className="var-dropdown"),
            ]),
            html.Div(className="var-filter-group", children=[
                html.Label("Corpo Hídrico", className="var-filter-label"),
                dcc.Dropdown(id="waterbody-select", options=body_options, value="Todos os Tipos", clearable=False, className="var-dropdown"),
            ]),
            html.Div(className="var-filter-group var-filter-group-scale", children=[
                html.Label("Escala", className="var-filter-label"),
                html.Div(className="var-scale-toggle-wrap", children=[
                    dcc.RadioItems(
                        id="scale-select",
                        options=[{"label": "Linear", "value": "linear"}, {"label": "Log", "value": "log"}],
                        value="linear", className="var-scale-toggle",
                        inputClassName="var-scale-radio", labelClassName="var-scale-label",
                    ),
                ]),
            ]),
            html.Div(className="var-filter-group var-filter-group-compare", children=[
                html.Label("Comparar por", className="var-filter-label"),
                html.Div(className="var-scale-toggle-wrap", children=[
                    dcc.RadioItems(
                        id="compare-select",
                        options=[{"label": "País", "value": "country"}, {"label": "Corpo Hídrico", "value": "waterbody"}],
                        value="country", className="var-scale-toggle",
                        inputClassName="var-scale-radio", labelClassName="var-scale-label",
                    ),
                ]),
            ]),
        ]),
    ])


def make_stats_row():
    return html.Div(id="var-stats-row", className="var-stats-row")


def make_viz_area():
    return html.Div(className="var-viz-area", children=[

        
        html.Div(className="var-viz-row", children=[
            html.Div(className="var-chart-card var-chart-full", children=[
                html.Div(className="var-chart-header", children=[
                    html.Div(className="var-chart-icon", children=[ico("lucide:bar-chart-2")]),
                    html.Div(children=[
                        html.H4("Distribuição de Frequência", className="var-chart-title"),
                        html.P("Histograma com curva de densidade (KDE)", className="var-chart-sub"),
                    ]),
                ]),
                dcc.Graph(id="var-histogram", config={"displayModeBar": False}, style={"width": "100%"}),
            ]),
        ]),

        
        html.Div(className="var-viz-row var-viz-row-split", children=[
            html.Div(className="var-chart-card", children=[
                html.Div(className="var-chart-header", children=[
                    html.Div(className="var-chart-icon", children=[ico("lucide:box-select")]),
                    html.Div(children=[
                        html.H4("Boxplot & Violin", className="var-chart-title"),
                        html.P("Dispersão, quartis e outliers", className="var-chart-sub"),
                    ]),
                ]),
                dcc.Graph(id="var-boxviolin", config={"displayModeBar": False}, style={"width": "100%"}),
            ]),

            
            html.Div(className="var-chart-card", style={"display": "flex", "flexDirection": "column", "gap": "20px"}, children=[
                html.Div(id="var-desc-table"),
            ]),
        ]),

        
        html.Div(className="var-viz-row var-viz-row-split", children=[
            html.Div(className="var-chart-card", children=[
                html.Div(className="var-chart-header", children=[
                    html.Div(className="var-chart-icon", children=[ico("lucide:layers")]),
                    html.Div(children=[
                        html.H4("Comparação Categórica", className="var-chart-title"),
                        html.P("Por país ou tipo de corpo hídrico", className="var-chart-sub"),
                    ]),
                ]),
                dcc.Graph(id="var-comparison", config={"displayModeBar": False}, style={"width": "100%"}),
            ]),

            make_boxplot_explainer(),
        ]),
    ])


def make_interpretation_block():
    return html.Div(className="var-interpret-section", children=[
        html.Div(className="var-interpret-grid", children=[
            html.Div(id="var-interpretation-card", className="var-interpret-card var-interpret-main"),
            html.Div(id="var-definition-card",     className="var-interpret-card var-interpret-secondary"),
        ]),
    ])


def make_variables_page():
    return html.Div(id="root", className="var-root", children=[
        make_variables_hero(),
        make_filter_bar(),
        make_stats_row(),
        make_viz_area(),
        make_interpretation_block(),
    ])


# ─────────────────────────────────────────────────────────────
#  CALLBACKS
# ─────────────────────────────────────────────────────────────

def register_callbacks(app):

    @app.callback(
        Output("var-stats-row", "children"),
        Input("var-select",      "value"),
        Input("country-select",  "value"),
        Input("waterbody-select","value"),
    )
    def update_stats(var_key, country, waterbody):
        if not var_key or var_key not in VARIABLES:
            return []
        m    = VARIABLES[var_key]
        mult = _get_filter_mult(var_key, country, waterbody)
        unit = m["unit"]
        mean   = m["mean"]   * mult
        median = m["median"] * mult
        std    = m["std"]    * mult
        return html.Div(className="var-stats-inner", children=[
            stat_card(f"{mean:.3g}",      "Média",         f"Valor médio: {mean:.3g} {unit}.",              "lucide:activity"),
            stat_card(f"{median:.3g}",    "Mediana",       "50% dos valores estão abaixo deste ponto.",     "lucide:minus"),
            stat_card(f"{std:.3g}",       "Desvio Padrão", interpret_cv(mean, std),                         "lucide:expand"),
            stat_card(f"{m['skew']:.2f}", "Assimetria",    interpret_skew(m["skew"]),                       "lucide:trending-up", highlight=abs(m["skew"]) > 3),
            stat_card(f"{m['kurtosis']:.1f}", "Curtose",   interpret_kurt(m["kurtosis"]),                   "lucide:move-vertical"),
            stat_card(f"{m['vmin']:.3g}", "Mínimo",        "Menor valor registrado no dataset.",            "lucide:arrow-down-left"),
            stat_card(f"{m['vmax']:.3g}", "Máximo",        "Maior valor registrado no dataset.",            "lucide:arrow-up-right", highlight=True),
        ])

    @app.callback(
        Output("var-histogram", "figure"),
        Input("var-select",       "value"),
        Input("scale-select",     "value"),
        Input("country-select",   "value"),
        Input("waterbody-select", "value"),
    )
    def update_histogram(var_key, scale, country, waterbody):
        if not var_key or var_key not in VARIABLES:
            return go.Figure()
        return build_histogram(var_key, use_log=(scale == "log"), country=country, waterbody=waterbody)

    @app.callback(
        Output("var-boxviolin", "figure"),
        Input("var-select",       "value"),
        Input("scale-select",     "value"),
        Input("country-select",   "value"),
        Input("waterbody-select", "value"),
    )
    def update_boxviolin(var_key, scale, country, waterbody):
        if not var_key or var_key not in VARIABLES:
            return go.Figure()
        return build_boxplot_violin(var_key, use_log=(scale == "log"), country=country, waterbody=waterbody)

    @app.callback(
        Output("var-comparison", "figure"),
        Input("var-select",       "value"),
        Input("compare-select",   "value"),
        Input("scale-select",     "value"),
        Input("country-select",   "value"),
        Input("waterbody-select", "value"),
    )
    def update_comparison(var_key, compare_by, scale, country, waterbody):
        if not var_key or var_key not in VARIABLES:
            return go.Figure()
        return build_comparison_chart(var_key, compare_by=compare_by, use_log=(scale == "log"), country=country, waterbody=waterbody)

    @app.callback(
        Output("var-desc-table", "children"),
        Input("var-select",       "value"),
        Input("country-select",   "value"),
        Input("waterbody-select", "value"),
    )
    def update_desc_table(var_key, country, waterbody):
        if not var_key or var_key not in VARIABLES:
            return []
        return build_stats_table(var_key, country=country, waterbody=waterbody)

    @app.callback(
        Output("var-interpretation-card", "children"),
        Input("var-select",       "value"),
        Input("country-select",   "value"),
        Input("waterbody-select", "value"),
    )
    def update_interpretation(var_key, country, waterbody):
        if not var_key or var_key not in VARIABLES:
            return []
        m    = VARIABLES[var_key]
        mult = _get_filter_mult(var_key, country, waterbody)

        filter_tags = []
        if country and country != "Todos os Países":
            filter_tags.append(html.Span(f"País: {country}", className="eda-insight-tag"))
        if waterbody and waterbody != "Todos os Tipos":
            filter_tags.append(html.Span(f"Corpo: {waterbody}", className="eda-insight-tag"))

        return [
            html.Div(className="var-interpret-header", children=[
                html.Div(className="var-interpret-icon", children=[ico("lucide:lightbulb", size=20)]),
                html.H3("Interpretação Analítica", className="var-interpret-title"),
            ]),
            html.P(m["interpretation"], className="var-interpret-body"),
            html.Div(className="var-interpret-tags", children=[
                html.Span(f"Assimetria: {m['skew']:.2f}",        className="eda-insight-tag"),
                html.Span(f"Mediana: {m['median'] * mult:.3g} {m['unit']}", className="eda-insight-tag"),
                html.Span(f"Máx: {m['vmax']:.3g} {m['unit']}",  className="eda-insight-tag eda-insight-tag-teal"),
                *filter_tags,
            ]),
        ]

    @app.callback(
        Output("var-definition-card", "children"),
        Input("var-select", "value"),
    )
    def update_definition(var_key):
        if not var_key or var_key not in VARIABLES:
            return []
        m = VARIABLES[var_key]
        return [
            html.Div(className="var-interpret-header", children=[
                html.Div(className="var-interpret-icon", children=[ico("lucide:flask-conical", size=20)]),
                html.H3("O que essa variável representa?", className="var-interpret-title"),
            ]),
            html.Div(className="var-def-pill", children=m["label"]),
            html.P(m["description"], className="var-interpret-body"),
        ]