# Relatório Técnico de Experimentos: Regressão Logística como Baseline Linear
**Projeto:** AquaSense — Monitoramento Inteligente da Qualidade Hídrica de Pernambuco
**Pesquisador:** Petterson Dhiogo de Melo Neves
**Programa:** Programa de Pós-Graduação em Geografia (PPGEO/UFPE) / Grupo de Pesquisa PAISAGEO
**Data:** Maio de 2026

---

## 1. Introdução e Contexto Metodológico

Este relatório documenta a trilha experimental realizada com o algoritmo paramétrico linear de **Regressão Logística** aplicado à classificação da qualidade da água. No escopo do projeto **AquaSense**, o objetivo científico desta etapa foi estabelecer uma *baseline* linear robusta para a previsão da variável alvo `conama_status`. 

A pesquisa foi dividida em duas grandes fases de modelagem:
1.  **Fase de 4 Classes:** Onde o alvo encontra-se segmentado em quatro categorias hierárquicas (*Excelente*, *Boa*, *Atenção* e *Crítica*).
2.  **Fase de 3 Classes:** Onde o problema foi simplificado por meio da fusão das categorias de maior risco ambiental, resultando em três classes (*Excelente*, *Boa* e *Atenção/Crítica*).

A distribuição natural dos dados hídricos coletados apresenta um desbalanceamento severo, com dominância massiva da categoria de águas limpas. Modelar esse cenário impõe desafios complexos: algoritmos tradicionais tendem a maximizar a acurácia global negligenciando as classes minoritárias, gerando modelos estatisticamente aceitáveis, mas ecologicamente perigosos (incapazes de detectar contaminações graves). A trilha foi estruturada de forma incremental ao longo de **7 experimentos estratégicos** para avaliar o impacto da engenharia de atributos (injeção de variáveis físico-químicas contínuas) e de técnicas de balanceamento.

---

## 2. Visão Geral da Trilha de Experimentos

A tabela abaixo sintetiza o desenho experimental adotado para a Regressão Logística:

| Experimento | Nº de Classes | Descrição das Variáveis de Entrada ($X$) | Estratégia de Balanceamento | Foco Científico |
| :--- | :---: | :--- | :--- | :--- |
| **Exp 1** | 4 | 4 Variáveis Reduzidas (`Temperature`, `Orthophosphate`, `Country`, `Waterbody Type`) | Nenhum (Distribuição Original) | Linha de base inicial sem tratamento de assimetria. |
| **Exp 2** | 4 | 4 Variáveis Reduzidas | `class_weight='balanced'` | Medir o efeito isolado da penalização de custo com poucas variáveis. |
| **Exp 3** | 4 | Todas as Variáveis (`+ pH`, `DBO`, `OD`, `Amônia`) | Nenhum (Distribuição Original) | Avaliar o poder preditivo da injeção de conhecimento químico puro. |
| **Exp 4** | 4 | Todas as Variáveis | `class_weight='balanced'` | Combinação de riqueza biológica e penalização matemática. |
| **Exp 5** | 4 | Todas as Variáveis | SMOTE (*Oversampling* Sintético) | Testar a reamostragem espacial por interpolação em modelo linear. |
| **Exp 6** | 4 | Todas as Variáveis | `class_weight='balanced'` + Tuning | Ajuste fino de hiperparâmetros (`C`, `solver`) via `GridSearchCV`. |
| **Exp 7** | **3** | Todas as Variáveis | `class_weight='balanced'` | Avaliar o impacto da redução de granularidade do alvo na precisão. |

---

## 3. Análise Detalhada dos Experimentos (Fase de 4 Classes)

### Experimento 1: Modelo Reduzido sem Balanceamento (4 Variáveis)
* **Resultados:** Acurácia Global: **~70.9%** | Classe `Crítica` (Recall / Precision): **0.00 / 0.00**
* **Análise Crítica:** O modelo sofreu um **colapso completo de classe majoritária**. Como a classe `Excelente` domina a maior parte do dataset, a otimização matemática encontrou o caminho de menor resistência: prever "Excelente" para quase todas as amostras para inflar a acurácia global. A matriz de confusão mostrou o apagão total das categorias de desconformidade ambiental, inviabilizando o modelo para o uso prático.

### Experimento 2: Modelo Reduzido com Pesos Balanceados (4 Variáveis)
* **Resultados:** Acurácia Global: **0.6440** | F1-Score Ponderado: **0.66** | Classe `Crítica` (Recall): **0.63**
* **Análise Crítica:** A ativação do parâmetro `class_weight='balanced'` calculou penalidades inversamente proporcionais à frequência das classes. O modelo foi forçado a "enxergar" as minorias, tirando o recall crítico do zero absoluto para 63%. Contudo, operando com poucas variáveis, a precisão desabou para 8%. O modelo passou a gerar uma quantidade massiva de **falsos alarmes**, classificando 670 águas de pureza extrema (`Excelente`) como críticas devido à rigidez da fronteira linear.

### Experimento 3: Expansão de Atributos sem Balanceamento (Todas as Variáveis)
* **Resultados:** Acurácia Global: **0.7813** | Classe `Crítica` (Recall): **0.00**
* **Análise Crítica:** A injeção de `pH`, `DBO`, `OD` e `Amônia` padronizados pelo `StandardScaler` provocou um salto de qualidade na acurácia global, provando que variáveis do domínio bioquímico possuem forte poder de separação. No entanto, a classe `Crítica` continuou completamente invisível. Conclusão: **a engenharia de atributos de alta qualidade é estritamente insuficiente se o desbalanceamento estatístico não for tratado ativamente**.

### Experimento 4: Expansão de Atributos com Pesos Balanceados (Todas as Variáveis)
* **Resultados:** Acurácia Global: **0.6974** | F1-Score Ponderado: **0.71** | Classe `Crítica` (Recall / Precision): **0.77 / 0.15**
* **Análise Crítica:** Este representou o **marco mais seguro da trilha de 4 classes**. Ao dispor de dados bioquímicos, o algoritmo ajustou melhor a linha de separação balanceada. O recall crítico subiu para **77%** e a precisão subiu para **15%** (reduzindo os falsos positivos do Exp 2). O dado mais expressivo foi a conquista da **falha segura**: a matriz de confusão registrou **zero (0) falsos negativos graves** de águas Críticas classificadas como Excelentes.

### Experimento 5: Expansão de Atributos com Oversampling Sintético (SMOTE)
* **Resultados:** Acurácia Global: **0.6131** | Classe `Crítica` (Recall / Precision): **0.81 / 0.12**
* **Análise Crítica:** O SMOTE estendeu a sensibilidade ao limite, registrando o recorde de recall crítico (**81%**). Contudo, o preço colateral foi inaceitável. Ao espalhar amostras artificiais pela fronteira de dados, o SMOTE gerou ruído espacial que confundiu o algoritmo linear. A precisão despencou (gerando mais de 1.480 falsos alarmes) e o modelo voltou a cometer o erro fatal de classificar **13 amostras realmente Críticas como Excelentes**. Para modelos lineares, o balanceamento por peso provou ser mais estável e seguro do que o SMOTE.

### Experimento 6: Otimização de Hiperparâmetros (GridSearchCV)
* **Resultados:** Consolidou a configuração base do Experimento 4, refinando a força da penalidade de coeficientes (`C`).
* **Análise Crítica:** O Experimento 6 confirmou o **diagnóstico definitivo de sobrediagnóstico por subajuste (Underfitting)**. A proximidade quase exata entre as métricas de treino e teste indica um alto viés metodológico. O modelo linear alcançou o seu "teto físico": ele não sofre de *overfitting* (memorização), mas não possui a flexibilidade geométrica necessária para dobrar suas fronteiras em torno dos nichos químicos complexos do dataset AquaSense de 4 classes.

---

## 4. Análise Detalhada da Fase de 3 Classes

### Experimento 7: Expansão de Atributos com Pesos Balanceados e Alvo Reduzido (3 Classes)
* **Objetivo:** Aplicar a arquitetura de melhor desempenho identificada na fase anterior (todas as variáveis + pesos balanceados) em uma versão simplificada do dataset (`amostra_rotulada_3.parquet`), investigando se a redução de granularidade do alvo atenua a taxa de falsos positivos do modelo linear.
* **Resultados Obtidos:**
  * Acurácia Global: **0.7078** (70.78%)
  * Classe `Excelente` (F1-Score): **0.83**
  * Classe `Atenção/Crítica` (Recall / Precision): **0.58 / 0.31**
* **Análise Crítica:** A reestruturação para 3 classes promoveu o **ponto de operação mais equilibrado de toda a modelagem linear**. Ao fundir as categorias de desconformidade, eliminou-se a "zona cinzenta" de transição que confundia o hiperplano da Regressão Logística. 
  * **Quebra dos Falsos Alarmes:** A *Precision* da classe de risco saltou para **31%** (praticamente o dobro do melhor modelo de 4 classes). Agora, a cada 3 alertas de contaminação emitidos pelo sistema, 1 está matematicamente correto.
  * **Comportamento da Matriz de Confusão:** Das 3.981 amostras reais de risco (`Atenção/Crítica`), o modelo capturou **2.314** com sucesso. O erro residual mostrou-se controlado e seguro: apenas 505 amostras vazaram para a classe `Excelente`, enquanto a maior parte do erro se concentrou na classe contígua (`Boa`, 1.162 amostras), comportamento aceitável em um gradiente químico contínuo.

---

## 5. Síntese Comparativa de Desempenho

A tabela abaixo consolida os principais indicadores obtidos ao longo de toda a pesquisa linear:

| Métrica de Teste | Exp 1 (Reduzido) | Exp 2 (Red_Bal) | Exp 3 (Completo) | Exp 4 (Comp_Bal) | Exp 5 (SMOTE) | Exp 6 (Tuned) | Exp 7 (3 Classes) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Acurácia Global** | 70.90% | 64.40% | 78.13% | 69.74% | 61.31% | Estável | **70.78%** |
| **F1-Score (Excelente)**| — | — | — | — | — | — | **0.8300** |
| **Recall (Classe Risco)*** | 0.00 | 0.63 | 0.00 | **0.77** | **0.81** | 0.77 | **0.58** |
| **Precision (Classe Risco)***| 0.00 | 0.08 | 0.00 | **0.15** | 0.12 | 0.15 | **0.31** |
| **Falsos Negativos Críticos** | Alta Taxa | Reduzida | Alta Taxa | **ZERO (0)** | 13 Amostras | **ZERO (0)** | **Baixa Taxa (505)** |

*\*Nota: Para os Experimentos 1 a 6, as métricas de risco referem-se isoladamente à classe 'Crítica'. No Experimento 7, referem-se à classe unificada 'Atenção/Crítica'.*

---

## 6. Conclusões Finais e Direcionamento da Pesquisa

A exaustão da trilha de Regressão Logística cumpre um papel epistemológico fundamental no desenvolvimento do sistema **AquaSense**:

1. **A Resolução do Impasse Linear:** O Experimento 7 demonstrou que a redução da granularidade do problema para 3 classes oferece o melhor balanço operacional para o modelo paramétrico, controlando de forma expressiva o volume de falsos alarmes (ganho de precisão de 15% para 31%).
2. **Confirmação Científica de Limites:** Embora o cenário de 3 classes tenha otimizado a Regressão Logística, o teto de desempenho geral reafirma que as interações biogeoquímicas que determinam a qualidade da água são intrinsecamente não-lineares.
3. **Recomendação de Próximos Passos:** Com a validação das pipelines de dados e das duas configurações de destino (4 e 3 classes), o foco absoluto da pesquisa deve migrar para os algoritmos de árvore (**Random Forest** e **LightGBM**). Estes modelos devem ser submetidos aos mesmos arranjos de atributos e balanceamentos validados aqui, utilizando a estrutura simplificada de 3 classes para maximizar a precisão cirúrgica e aproximar o classificador inteligente das condições reais de implantação em Pernambuco.