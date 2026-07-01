# Setup do Projeto AquaSense — PISI

Este documento apresenta as instruções necessárias para acessar, visualizar e executar o projeto AquaSense. O projeto está organizado em repositório no GitHub, permitindo a consulta dos arquivos, notebooks, códigos, resultados e documentação diretamente pela plataforma.

## 1. Acesso ao Repositório

O código-fonte, os notebooks, os arquivos de apoio e a documentação do projeto podem ser acessados pelo GitHub no link abaixo:

 `https://github.com/pablonvsx/pisi3-ufrpe.git`

Por meio do repositório, é possível visualizar a estrutura do projeto, consultar os arquivos desenvolvidos, acessar os notebooks utilizados nos experimentos e acompanhar a organização geral da solução.

## 2. Acesso ao Dashboard

O dashboard do AquaSense foi disponibilizado em servidor, permitindo a visualização dos resultados finais sem necessidade de instalação local.

Acesse o dashboard pelo link abaixo:

`https://dashboard-aquasense.onrender.com`

O dashboard reúne as principais etapas dos experimentos realizados com aprendizado de máquina, apresentando a evolução dos testes, a reconstrução dos rótulos de classificação, os resultados obtidos e a interpretação das variáveis mais relevantes para o modelo.

## 3. Clonando o Repositório

Caso seja necessário executar o projeto localmente, o primeiro passo é clonar o repositório do GitHub.

No terminal, execute:

```bash
git clone https://github.com/pablonvsx/pisi3-ufrpe.git
```

Em seguida, acesse a pasta do projeto:

```bash
cd data-science
```

## 4. Abrindo o Projeto no VS Code

Após clonar o repositório, o projeto pode ser aberto no Visual Studio Code.

Na pasta do projeto, execute:

```bash
code .
```

Também é possível abrir manualmente o VS Code e selecionar a pasta do projeto por meio da opção:

```text
File > Open Folder
```

## 5. Criando o Ambiente Virtual

Para evitar conflitos com bibliotecas instaladas globalmente, recomenda-se criar um ambiente virtual Python.

No terminal, dentro da pasta do projeto, execute:

```bash
python -m venv .venv
```

Depois, ative o ambiente virtual.

No Windows:

```bash
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

## 6. Instalando as Dependências

Com o ambiente virtual ativado, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

O arquivo `requirements.txt` contém as principais bibliotecas utilizadas para execução dos recursos associados ao projeto. 


## 7. Executando o Dashboard Localmente

Primeiro, acesse a pasta do dashboard: 

```bash
cd aquasense_dashboard
```

Em seguida, instale as dependências necessárias para a execução: 

```bash
pip install -r requirements-dashboard.txt
```

Após a instalação das dependências, execute o arquivo principal do dashboard:

```bash
python app.py
```

Em seguida, acesse no navegador o endereço exibido no terminal. O endereço local será:

```text
http://127.0.0.1:8050/  
```

## 8. Visualização dos Notebooks e Experimentos

Os notebooks utilizados nos experimentos podem ser visualizados diretamente pelo GitHub.

Caso seja necessário executá-los, recomenda-se abrir os arquivos `.ipynb` no VS Code com a extensão Jupyter instalada, ou executá-los em outro ambiente compatível com notebooks Python.

Os notebooks documentam as etapas de análise, preparação dos dados, featureização, treinamento dos modelos, avaliação dos resultados e interpretação das variáveis.


## 9. Observações Importantes

O acesso pelo link do dashboard é a forma recomendada para visualização rápida dos resultados finais.

A execução local deve ser utilizada caso seja necessário validar o funcionamento do projeto, inspecionar o código, testar ajustes ou executar novamente os arquivos disponíveis no repositório.

Caso ocorra algum erro relacionado a dependências, recomenda-se confirmar se o ambiente virtual está ativado e se todas as bibliotecas dos arquivos `requirements.txt` e `requirements-dashboard.txt` foram instaladas corretamente.

## 10. Responsáveis

Integrantes:

[Ana Clara Souza ](https://github.com/eianaxz) •  [Maria Laura Cordeiro](https://github.com/mlcordeiro) •  [Pablo Neves](https://github.com/pablonvsx) •  [Lucas Gabriel](https://github.com/lux0blivion)
