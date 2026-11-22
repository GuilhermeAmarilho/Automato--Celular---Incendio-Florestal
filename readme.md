# Simulador de Incêndio Florestal

Projeto desenvolvido para a disciplina de Computação Científica do curso de Engenharia da Computação da Universidade Federal do Rio Grande.

## Sobre o Projeto

O projeto consiste em um simulador de incêndios florestais utilizando autômatos celulares, desenvolvido em Python com a biblioteca Tkinter.

A aplicação representa uma floresta por meio de uma grade de células, permitindo acompanhar a propagação do fogo, a queima das árvores e a regeneração da vegetação ao longo das gerações.

O comportamento do incêndio depende de regras de transição, da quantidade de células vizinhas em chamas e das condições do vento.

## Tecnologias Utilizadas

- Python — linguagem utilizada no desenvolvimento.
- Tkinter — biblioteca utilizada para a interface gráfica.
- Random — utilizada para a propagação probabilística do fogo.
- Math — utilizada nos cálculos relacionados à influência do vento.
- Pathlib — utilizada para trabalhar com os caminhos dos arquivos.

## Estrutura do Projeto

O código foi dividido em diferentes arquivos para facilitar sua organização e manutenção.

- `src/main.py` — inicia a aplicação.
- `src/configuracoes.py` — contém os estados, cores e parâmetros do modelo.
- `src/automato.py` — implementa as regras de evolução e propagação do incêndio.
- `src/arquivos.py` — realiza a leitura e o salvamento dos arquivos de texto.
- `src/estatisticas.py` — calcula a quantidade de células em cada estado.
- `src/interface.py` — contém a interface gráfica e seus controles.
- `src/gerar_estado_inicial.py` — gera uma configuração inicial da floresta.
- `estados/` — armazena os arquivos de estado da simulação.
- `documentacao/` — contém a descrição completa do modelo.

## Requisitos

Para executar o projeto, é necessário ter o Python 3 instalado no computador, com suporte à biblioteca Tkinter.

As demais bibliotecas utilizadas fazem parte da biblioteca padrão do Python, não sendo necessária a instalação de pacotes adicionais pelo pip.

## Como Executar

1. Abra a pasta do projeto no Visual Studio Code.
2. Abra o terminal na pasta principal.
3. Execute o comando:

   `python src/main.py`

A interface gráfica será aberta, carregando automaticamente a floresta armazenada no arquivo `estados/estado_inicial.txt`.

Caso o arquivo inicial ainda não exista, execute primeiro:

`python src/gerar_estado_inicial.py`

Depois, execute o programa normalmente.

## Como Utilizar

A interface possui quatro controles principais:

- **Play:** inicia a simulação automaticamente.
- **Pause:** interrompe a execução.
- **Step:** avança uma geração por vez.
- **Reset:** retorna a floresta ao estado de referência.

No painel de configurações, é possível alterar a direção e a intensidade do vento, além de ajustar a velocidade da simulação.

O editor permite selecionar diferentes estados e modificar diretamente a floresta. O botão esquerdo do mouse desenha o estado escolhido, enquanto o botão direito transforma as células em terreno vazio.

Também é possível salvar a floresta atual em um arquivo de texto ou carregar uma configuração existente.

## Estados da Floresta

O modelo utiliza cinco estados:

- **0 — Terreno vazio:** área sem vegetação.
- **1 — Árvore saudável:** vegetação que pode pegar fogo.
- **2 — Árvore em chamas:** vegetação atingida pelo incêndio.
- **3 — Terreno queimado:** área onde o fogo já consumiu a vegetação.
- **4 — Vegetação regenerando:** área em processo de recuperação.

Cada estado possui uma cor específica para facilitar a visualização.

## Estatísticas

Durante a execução, o programa apresenta a quantidade de células em cada estado, o total de células da grade e a porcentagem da área que está em chamas.

Essas informações são atualizadas conforme a simulação avança ou a floresta é modificada.

## Documentação

A explicação completa do funcionamento do autômato celular, incluindo os estados, a vizinhança de Moore, as regras de evolução e a influência do vento, está disponível em:

`documentacao/descricao_modelo.md`

## Observações

O simulador utiliza um modelo simplificado de incêndio florestal, com o objetivo de demonstrar o funcionamento dos autômatos celulares e a evolução de sistemas baseados em regras locais.

Os resultados representam comportamentos simulados e não devem ser utilizados como previsões de incêndios reais.
