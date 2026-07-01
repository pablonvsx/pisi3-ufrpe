# AquaSense — PISI 3 / UFRPE

Repositório do projeto **AquaSense**, desenvolvido no componente curricular **Projeto Interdisciplinar em Sistemas de Informação III (BSI/UFRPE)**.

O projeto aplica técnicas de ciência de dados e aprendizado de máquina para classificação da qualidade da água, com integração a um dashboard interativo e API para aplicação mobile.

---

## Equipe

### Docentes Orientadores

- Prof. Dr. Gabriel Alves de Albuquerque Júnior
- Profa. Dra. Maria da Conceição Moraes Batista

### Discentes

- Ana Clara Souza da Silva
- Lucas Gabriel Ferreira de Santana
- Maria Laura Lopes Cordeiro
- Pablo Guilherme de Melo Neves

---

## Estrutura do Repositório

```
pisi3-ufrpe/
└── data-science/
    ├── dataset/                        # Dataset combinado (Combined_dataset.csv)
    ├── notebooks/
    │   ├── EDA/                        # Análise Exploratória de Dados (8 notebooks)
    │   └── ML/                         # Experimentos de Machine Learning
    │       ├── primeira_analise/       # Primeiros experimentos (LightGBM, RF, RL, SVM)
    │       ├── experimentos_amostra_binária/  # Experimentos com classes binárias
    │       └── analise_final/          # Análise e modelo final
    ├── aquasense_dashboard/            # Dashboard interativo (Dash/Plotly)
    │   ├── app.py
    │   ├── models/                     # Modelos treinados (.joblib)
    │   └── *_page.py                   # Páginas do dashboard
    ├── requirements.txt
    └── setup.md                        # Instruções de configuração do ambiente
```

---

## Notebooks — Análise Exploratória de Dados (EDA)

| # | Notebook | Conteúdo |
|---|----------|----------|
| 01 | `general_view` | Visão geral do dataset |
| 02 | `histograms` | Distribuições das variáveis |
| 03 | `boxplots` | Detecção visual de outliers |
| 04 | `asymmetries` | Análise de assimetrias |
| 05 | `analysisbycountry` | Análise por país |
| 06 | `analysisbywaterbody` | Análise por corpo d'água |
| 07 | `correlationsvariables` | Correlações entre variáveis |
| 08 | `integrationconamaresolution` | Integração com a Resolução CONAMA |

---

## Notebooks — Machine Learning

### Primeira Análise

Experimentos iniciais com quatro algoritmos supervisionados:

- **LightGBM** — 8 experimentos
- **Random Forest** — 12 experimentos
- **Regressão Logística** — 7 experimentos
- **SVM** — 7 experimentos

### Experimentos com Amostra Binária

- Construção de classes binárias e subgrupos
- XGBoost com novo rótulo
- LightGBM com validação temporal (2000–2008)
- Reconstrução do rótulo multiclasse a partir das classes binárias
- Interpretabilidade com SHAP

### Análise Final

- Construção e validação do rótulo definitivo
- Random Forest, XGBoost, SVM e Regressão Logística com novo rótulo
- Análise temporal e diagnóstico de classes
- Balanceamento com SMOTE e pesos manuais
- Comparação final entre modelos e conclusão geral

### Não Supervisionado

- KMeans para agrupamento exploratório

---

## Dashboard — AquaSense

Dashboard interativo construído com **Dash** e **Plotly**, com as seguintes páginas:

| Página | Descrição |
|--------|-----------|
| Visão por País | Análise de qualidade da água por país |
| Corpo d'Água | Análise por tipo de corpo hídrico |
| Variáveis | Distribuição e comportamento das variáveis |
| Outliers | Detecção e visualização de outliers |
| Correlações | Mapa de calor e correlações entre parâmetros |
| Monitoramento Ambiental | Tendências temporais de qualidade |
| CONAMA | Classificação segundo a Resolução CONAMA |
| Predição (ML) | Predição da qualidade da água via modelo treinado |

O modelo final (`aquasense_modelo_final.joblib`) é servido por uma **API FastAPI** para integração com aplicativo mobile.

---

## Tecnologias

| Categoria | Bibliotecas |
|-----------|-------------|
| Manipulação de dados | pandas, numpy, scipy |
| Visualização | plotly |
| Machine Learning | scikit-learn, xgboost, lightgbm, imbalanced-learn (SMOTE) |
| Explicabilidade | shap |
| Dashboard | dash |
| API | fastapi, uvicorn |
| Notebooks | jupyterlab, ipykernel |

---

## Configuração do Ambiente

### 1. Clonar o repositório

```bash
git clone https://github.com/pablonvsx/pisi3-ufrpe.git
cd pisi3-ufrpe/data-science
```

### 2. Criar e ativar ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Baixar o dataset

O dataset não está versionado por ser muito grande. Baixe-o pelo link no arquivo [setup.md](data-science/setup.md) e coloque o arquivo `Combined_dataset.csv` em `data-science/dataset/`.

### 5. Executar o dashboard

```bash
cd aquasense_dashboard
python app.py
```

### 6. Executar os notebooks

```bash
cd ..
jupyter lab
```

---

## Instituição

**Universidade Federal Rural de Pernambuco (UFRPE)**
Bacharelado em Sistemas de Informação — PISI 3
