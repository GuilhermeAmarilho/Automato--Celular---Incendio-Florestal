# Projeto de Autômato Celular — Simulação de Incêndio Florestal

## 1. Descrição do Projeto

Este projeto tem como proposta desenvolver uma aplicação que simula a propagação de incêndios florestais utilizando autômatos celulares. O programa foi desenvolvido em Python, utilizando a biblioteca Tkinter para criar a interface gráfica, onde é possível visualizar como o fogo se espalha pela floresta ao longo do tempo.

Para representar a floresta, foi utilizada uma grade de 50 × 50 células, totalizando 2.500 posições. Cada célula representa uma pequena parte da floresta e pode assumir diferentes estados, como árvore saudável, árvore em chamas ou terreno queimado. Esses estados vão mudando conforme as regras definidas para a simulação.

O funcionamento do programa considera alguns fatores, como a probabilidade de o fogo atingir as árvores próximas, a direção e a intensidade do vento e o tempo necessário para a vegetação se recuperar após o incêndio. Com isso, é possível observar como o fogo se comporta em diferentes situações.

Além da simulação, o programa possui algumas funcionalidades que permitem ao usuário interagir com a floresta. É possível iniciar e pausar a execução, avançar uma geração por vez, reiniciar a simulação, modificar as células com o mouse e ajustar a velocidade e as condições do vento. O programa também permite salvar e carregar arquivos com os estados da floresta e acompanhar algumas estatísticas durante a execução.

## 2. Objetivo

O objetivo deste projeto é desenvolver um simulador de incêndios florestais utilizando autômatos celulares, aplicando os conceitos de estados, vizinhança, regras de transição e simulação de eventos discretos estudados na disciplina de Computação Científica.

A ideia é representar de forma simplificada como um incêndio pode se espalhar por uma floresta e observar como fatores como a quantidade de árvores próximas e as condições do vento podem influenciar sua propagação.

Além disso, o projeto permite colocar em prática conhecimentos de programação em Python, criação de interfaces gráficas e leitura e gravação de arquivos.

## 3. Estados das Células

Para representar as diferentes condições da floresta, foram definidos cinco estados, identificados por números de 0 a 4. Cada estado também possui uma cor específica para facilitar a visualização durante a simulação.

**Estado 0 — Terreno vazio:** representa uma área onde não existe vegetação. Essas células aparecem na cor cinza e não podem pegar fogo, permanecendo no mesmo estado durante toda a simulação.

**Estado 1 — Árvore saudável:** representa uma área com vegetação que ainda não foi atingida pelo incêndio. É identificada pela cor verde e pode pegar fogo caso existam árvores em chamas nas proximidades, dependendo da probabilidade de propagação.

**Estado 2 — Árvore em chamas:** representa uma árvore que está queimando. Essas células aparecem na cor vermelha e podem espalhar o fogo para as árvores vizinhas. Depois de duas gerações, passam para o estado de terreno queimado.

**Estado 3 — Terreno queimado:** representa uma área onde a vegetação já foi consumida pelo fogo. É identificada pela cor preta e não espalha mais o incêndio. Após permanecer oito gerações nesse estado, a célula começa a se regenerar.

**Estado 4 — Vegetação regenerando:** representa uma área que está se recuperando depois do incêndio. Essas células aparecem na cor verde-clara e, após cinco gerações, voltam ao estado de árvore saudável.

Com esses cinco estados, é possível acompanhar não apenas o avanço do incêndio, mas também o que acontece com a vegetação depois que o fogo passa.

## 4. Vizinhança Utilizada

Para definir como as células interagem entre si, foi utilizada a vizinhança de Moore, que considera as oito células ao redor de uma posição, incluindo as direções horizontal, vertical e diagonal.

Essa vizinhança foi escolhida porque permite que o fogo se espalhe em diferentes direções, tornando a simulação mais interessante e próxima do comportamento que esperamos observar em um incêndio.

Por exemplo, quando uma árvore está em chamas, ela pode transmitir o fogo para outras árvores que estejam ao seu redor, inclusive nas diagonais. Porém, isso não significa que todas as árvores vizinhas vão pegar fogo, pois a propagação depende de uma probabilidade.

Nas bordas da floresta, o programa considera apenas as células vizinhas que estão dentro da grade. Dessa forma, o fogo não passa de uma borda para a outra.

## 5. Regras de Evolução

O funcionamento do autômato celular acontece por meio de gerações. A cada geração, o programa verifica o estado de todas as células e aplica as regras que determinam se elas vão continuar na mesma condição ou mudar para outro estado.

No caso das árvores saudáveis, foi definida uma probabilidade básica de 30% de pegar fogo a partir de cada árvore vizinha que esteja em chamas. Quando existem vários vizinhos queimando, a chance de propagação aumenta, pois o programa considera a contribuição de cada um deles.

Outro fator utilizado na simulação é o vento. Dependendo da direção escolhida, o fogo terá uma probabilidade maior de se espalhar para determinadas regiões da floresta. Por exemplo, quando o vento está soprando para o leste, a propagação tende a ser maior nessa direção. Também é possível escolher entre três intensidades: sem vento, moderado e forte.

Quando uma árvore pega fogo, ela permanece em chamas durante duas gerações. Depois disso, passa para o estado de terreno queimado, onde permanece por oito gerações antes de iniciar a regeneração. A vegetação leva mais cinco gerações para se recuperar e voltar a ser uma árvore saudável.

Para controlar essas mudanças, o programa utiliza contadores que registram quanto tempo cada célula permanece em determinado estado.

Uma característica importante é que todas as células são atualizadas ao mesmo tempo, considerando os estados da geração anterior. Isso evita que uma árvore que acabou de pegar fogo já espalhe o incêndio durante a mesma geração.

## 6. Funcionalidades da Aplicação

O programa possui uma interface gráfica desenvolvida com Tkinter, que permite acompanhar o incêndio e controlar o funcionamento da simulação.

Foram adicionados quatro botões principais. O botão **Play** inicia a execução automática, enquanto o **Pause** interrompe a simulação. O botão **Step** permite avançar apenas uma geração por vez, facilitando a observação das mudanças, e o **Reset** retorna a floresta ao estado de referência.

Também foi criado um painel de configurações, onde o usuário pode alterar a velocidade da simulação, escolher a direção do vento e definir sua intensidade. Essas opções permitem testar diferentes situações e observar como o comportamento do incêndio muda.

Outra funcionalidade é o editor da floresta. Utilizando o mouse, é possível modificar as células da grade, adicionando árvores, criando terrenos vazios, marcando áreas queimadas ou iniciando novos focos de incêndio. Isso permite criar diferentes cenários sem precisar alterar diretamente o código.

O programa também possui opções para salvar e carregar arquivos de texto. Ao salvar, são registrados os estados das células, seus contadores de tempo e o número da geração atual. Dessa forma, é possível carregar uma configuração posteriormente e continuar a simulação a partir daquele ponto, embora a sequência futura dos sorteios probabilísticos não seja necessariamente a mesma.

Por fim, foi adicionado um painel estatístico que mostra a quantidade de células em cada estado, o total de células da floresta e a porcentagem da área que está em chamas. Essas informações são atualizadas durante a execução e ajudam a acompanhar as mudanças que acontecem na floresta.

## 7. Considerações sobre o Modelo

O simulador desenvolvido representa de forma simplificada o comportamento de um incêndio florestal. A intenção não é reproduzir exatamente um incêndio real, já que existem muitos outros fatores que influenciam esse fenômeno, como temperatura, umidade, tipo de vegetação e condições do terreno.

Mesmo assim, o modelo permite observar como o fogo pode se espalhar a partir de um pequeno foco inicial e como a direção e a intensidade do vento podem alterar esse comportamento. Também é possível acompanhar o processo de recuperação das áreas queimadas.

Durante o desenvolvimento, foi possível aplicar os conceitos de autômatos celulares estudados na disciplina, principalmente a utilização de uma grade de células, a definição de estados, as regras de transição e a atualização simultânea das células.

Além disso, o projeto envolveu a utilização de Python, a organização do código em diferentes arquivos, a criação de uma interface gráfica e a manipulação de arquivos de texto.

De modo geral, o trabalho permitiu compreender melhor como regras relativamente simples podem ser utilizadas para representar e simular fenômenos mais complexos, mostrando uma das aplicações dos autômatos celulares na Computação Científica.