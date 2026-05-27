# Relatório Técnico de Experimentos: Regressão Logística como Baseline Linear
**Projeto:** AquaSense — Monitoramento Inteligente da Qualidade Hídrica de Pernambuco
**Pesquisador:** Petterson Dhiogo de Melo Neves
**Programa:** Programa de Pós-Graduação em Geografia (PPGEO/UFPE) / Grupo de Pesquisa PAISAGEO
**Data:** Maio de 2026

---

## 1. Introdução e Contexto Metodológico

Este relatório documenta a trilha experimental realizada com o algoritmo paramétrico linear de **Regressão Logística** aplicado à classificação da qualidade da água. No escopo do projeto **AquaSense**, o objetivo científico desta etapa foi estabelecer uma *baseline* linear robusta para a previsão da variável alvo `conama_status`, dividida em quatro categorias hierárquicas ordenadas de acordo com as resoluções ambientais vigentes: **Excelente**, **Boa**, **Atenção** e **Crítica**.

A distribuição natural dos dados hídricos coletados apresenta um severo desbalanceamento de classes, com uma predominância massiva da categoria `Excelente`. Modelar esse cenário impõe desafios metodológicos significativos: algoritmos de machine learning tendem a otimizar a acurácia global negligenciando as classes minoritárias, o que gera modelos estatisticamente aceitáveis, mas ecologicamente perigosos (incapazes de detectar contaminações graves).

A trilha de Regressão Logística foi estruturada de forma incremental ao longo de **6 experimentos estratégicos**, investigando o impacto da engenharia de atributos (injeção de variáveis físico-químicas contínuas) e de técnicas de balanceamento (ajuste de pesos na função de custo vs. amostragem sintética via SMOTE).

---

## 2. Visão Geral da Trilha de Experimentos

A tabela abaixo sintetiza o desenho experimental adotado para a Regressão Logística:

| Experimento | Descrição das Variáveis de Entrada ($X$) | Estratégia de Balanceamento | Foco Científico |
| :--- | :--- | :--- | :--- |
| **Exp 1** | 4 Variáveis Reduzidas (`Temperature`, `Orthophosphate`, `Country`, `Waterbody Type`) | Nenhum (Distribuição Original) | Linha de base inicial sem tratamento de assimetria. |
| **Exp 2** | 4 Variáveis Reduzidas | `class_weight='balanced'` | Medir o efeito isolado da penalização de custo com poucas variáveis. |
| **Exp 3** | Todas as Variáveis (`+ pH`, `DBO`, `OD`, `Amônia`) | Nenhum (Distribuição Original) | Avaliar o poder preditivo da injeção de conhecimento químico puro. |
| **Exp 4** | Todas as Variáveis | `class_weight='balanced'` | Combinação de riqueza biológica e penalização matemática. |
| **Exp 5** | Todas as Variáveis | SMOTE (*Oversampling* Sintético) | Testar a reamostragem espacial por interpolação em modelo linear. |
| **Exp 6** | Todas as Variáveis | `class_weight='balanced'` + Tuning | Ajuste fino de hiperparâmetros (`C`, `solver`) via `GridSearchCV`. |

---

## 3. Análise Detalhada dos Experimentos

### Experimento 1: Modelo Reduzido sem Balanceamento (4 Variáveis)
* **Objetivo:** Estabelecer a linha de base mais simples possível para avaliar o comportamento do algoritmo diante do desbalanceamento estrutural.
* **Resultados Obtidos:**
  * Acurácia Global: **~70.9%**
  * Classe `Crítica` (Recall / Precision): **0.00 / 0.00**
  * Classe `Atenção` (Recall / Precision): **0.00 / 0.00**
* **Análise Crítica:** O modelo sofreu um **colapso completo de classe majoritária**. Como a classe `Excelente` domina cerca de 73% do dataset, a otimização matemática encontrou o caminho de menor resistência: prever "Excelente" para quase todas as amostras para inflar artificialmente a acurácia global. A matriz de confusão mostrou o apagão total das categorias de desconformidade ambiental, inviabilizando o modelo para o uso prático.

### Experimento 2: Modelo Reduzido com Pesos Balanceados (4 Variáveis)
* **Objetivo:** Mitigar o colapso do Experimento 1 alterando a função de custo do classificador sem introduzir novas variáveis.
* **Resultados Obtidos:**
  * Acurácia Global: **0.6440** (64.40%) | F1-Score Ponderado: **0.66**
  * Classe `Crítica` (Recall): **0.63** | Classe `Atenção` (Recall): **0.46**
  * Classe `Crítica` (Precision): **0.08**
* **Análise Crítica:** A ativação do parâmetro `class_weight='balanced'` calculou penalidades inversamente proporcionais à frequência das classes. O modelo foi forçado a "enxergar" as minorias, tirando o recall crítico do zero absoluto para 63%. Contudo, operando com poucas variáveis, a precisão desabou para 8%. O modelo passou a gerar uma quantidade massiva de **falsos alarmes**, classificando 670 águas de pureza extrema (`Excelente`) como críticas devido à rigidez da fronteira linear.

### Experimento 3: Expansão de Atributos sem Balanceamento (Todas as Variáveis)
* **Objetivo:** Analisar se a introdução de parâmetros físico-químicos diretos e causais da qualidade da água resolve o desbalanceamento por si só.
* **Resultados Obtidos:**
  * Acurácia Global: **0.7813** (78.13%)
  * Classe `Crítica` (Recall / Precision): **0.00 / 0.00**
  * Classe `Atenção` (Recall): Melhoria localizada (315 acertos corretos).
* **Análise Crítica:** A injeção de `pH`, `DBO`, `OD` e `Amônia` padronizados pelo `StandardScaler` provocou um salto de qualidade na acurácia global, provando que variáveis do domínio bioquímico possuem forte poder de separação. No entanto, a classe `Crítica` continuou completamente invisível. Esse experimento trouxe uma importante conclusão metodológica: **a engenharia de atributos de alta qualidade é estritamente insuficiente se o desbalanceamento estatístico não for tratado ativamente**.

### Experimento 4: Expansão de Atributos com Pesos Balanceados (Todas as Variáveis)
* **Objetivo:** Unir o contexto químico completo com a penalização matemática da função de custo.
* **Resultados Obtidos:**
  * Acurácia Global: **0.6974** (69.74%) | F1-Score Ponderado: **0.71**
  * Classe `Crítica` (Recall / Precision): **0.77 / 0.15**
  * Classe `Atenção` (Recall / Precision): **0.53 / 0.28**
* **Análise Crítica:** Este representou o **marco mais seguro da trilha linear**. Ao dispor de dados bioquímicos, o algoritmo ajustou melhor a linha de separação balanceada. O recall crítico subiu para **77%** e a precisão subiu para **15%** (reduzindo significativamente os falsos positivos do Exp 2). O dado mais expressivo foi a conquista da **falha segura**: a matriz de confusão registrou **zero (0) falsos negativos graves** de águas Críticas classificadas como Excelentes. É o melhor comportamento que uma reta matemática consegue atingir neste cenário.

### Experimento 5: Expansão de Atributos com Oversampling Sintético (SMOTE)
* **Objetivo:** Avaliar a eficácia de equilibrar as classes fisicamente gerando dados sintéticos por interpolação espacial no treino.
* **Resultados Obtidos:**
  * Acurácia Global: **0.6131** (61.31%) | F1-Score Ponderado: **0.66**
  * Classe `Crítica` (Recall / Precision): **0.81 / 0.12**
  * Classe `Atenção` (Recall): **0.65**
* **Análise Crítica:** O SMOTE estendeu a sensibilidade do modelo ao limite, registrando o recorde de recall crítico (**81%**). Contudo, o preço ecológico e computacional foi inaceitável. Ao espalhar amostras artificiais pela fronteira de dados, o SMOTE gerou ruído espacial que confundiu o algoritmo linear. A precisão despencou (gerando mais de 1.480 falsos alarmes de águas Excelentes rotuladas como Críticas) e o modelo voltou a cometer o erro fatal de classificar **13 amostras realmente Críticas como Excelentes**. Para modelos lineares, o balanceamento por peso provou ser mais estável e seguro do que o SMOTE.

### Experimento 6: Otimização de Hiperparâmetros (GridSearchCV)
* **Objetivo:** Encontrar o limite absoluto de desempenho físico da Regressão Logística refinando a regularização matemática (`C`) e o algoritmo solucionador (`solver`).
* **Resultados Obtidos:**
  * O modelo final consolidou a configuração base do Experimento 4 (`class_weight='balanced'`) refinando a força da penalidade de coeficientes.
  * Manteve o perfil conservador e protetivo de alto recall, demonstrando estabilidade na validação cruzada.
* **Análise Crítica:** O Experimento 6 confirmou o **diagnóstico definitivo de sobrediagnóstico por subajuste (Underfitting)**. A proximidade quase exata entre as métricas de treino e teste indica um alto viés metodológico. O modelo linear alcançou o seu "teto físico": ele não sofre de *overfitting* (memorização), mas não possui a flexibilidade geométrica necessária para dobrar suas fronteiras em torno dos nichos químicos complexos do dataset AquaSense.

---

## 4. Síntese Comparativa de Desempenho

| Métrica de Teste | Exp 1 (Reduzido) | Exp 2 (Red_Bal) | Exp 3 (Completo) | Exp 4 (Comp_Bal) | Exp 5 (SMOTE) | Exp 6 (Tuned) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Acurácia Global** | 70.90% | 64.40% | 78.13% | 69.74% | 61.31% | Estável |
| **F1-Score (Weighted)**| — | 0.6600 | — | 0.7100 | 0.6600 | 0.7100 |
| **Recall (Crítica)** | 0.00 | 0.63 | 0.00 | **0.77** | **0.81** | 0.77 |
| **Precision (Crítica)**| 0.00 | 0.08 | 0.00 | **0.15** | 0.12 | 0.15 |
| **Falsos Negativos** <br>*(Crítica → Excelente)* | Alta Taxa | Reduzida | Alta Taxa | **ZERO (0)** | 13 Amostras | **ZERO (0)** |

---

## 5. Conclusões Finais 

A exaustão da trilha de Regressão Logística cumpre um papel epistemológico fundamental no desenvolvimento do sistema **AquaSense**:

1. **Validação da Pipeline de Pré-processamento:** O uso integrado do `ColumnTransformer`, `OneHotEncoder` e `StandardScaler` funcionou perfeitamente e garantiu o rigor matemático necessário para algoritmos baseados em gradiente, evitando que variáveis com ordens de grandeza distintas distorcessem os pesos do modelo.
2. **Justificativa para Modelos Não Lineares:** Os limites de precisão encontrados (estagnação em torno de 15% de precisão para classes críticas nos melhores cenários balanceados) provam cientificamente que as interações biogeoquímicas que determinam o enquadramento CONAMA são de natureza fortemente não-linear.
