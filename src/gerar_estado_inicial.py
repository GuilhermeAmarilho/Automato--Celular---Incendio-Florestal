import random
from pathlib import Path

# Configurações da floresta
LINHAS = 50
COLUNAS = 50
QUANTIDADE_VAZIOS = 476

# Estados das células
VAZIO = 0
ARVORE = 1
FOGO = 2
QUEIMADO = 3
REGENERANDO = 4

# Caminho do arquivo de saída
PASTA_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO_SAIDA = PASTA_PROJETO / "estados" / "estado_inicial.txt"
ARQUIVO_SAIDA.parent.mkdir(parents=True, exist_ok=True)

# Usei um nro fixo para poder reproduzir sempre o mesmo teste
random.seed(42)

# Cria uma floresta preenchida com árvores
grade = [
    [
        ARVORE for _ in range(COLUNAS)
    ] 
    for _ in range(LINHAS)
]

# Define três células em chamas próximas umas das outras
focos_iniciais = [(24, 10), (25, 10), (25, 11)]

# Seleciona posições disponíveis para terrenos vazios
posicoes_disponiveis = [
    (linha, coluna)
    for linha in range(LINHAS)
    for coluna in range(COLUNAS)
    if (linha, coluna) not in focos_iniciais
]

posicoes_vazias = random.sample(
    posicoes_disponiveis, QUANTIDADE_VAZIOS
)

# Coloca os terrenos vazios
for linha, coluna in posicoes_vazias:
    grade[linha][coluna] = VAZIO

# Coloca os focos iniciais de incêndio
for linha, coluna in focos_iniciais:
    grade[linha][coluna] = FOGO

# Salva a grade em um arquivo de texto
with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as arquivo:
    for linha in grade:
        arquivo.write(" ".join(map(str, linha)) + "\n")

print("Estado inicial criado com sucesso!")
print(f"Arquivo: {ARQUIVO_SAIDA}")
print(f"Dimensões: {LINHAS} x {COLUNAS}")
print(f"Árvores: {LINHAS * COLUNAS - QUANTIDADE_VAZIOS - len(focos_iniciais)}")
print(f"Terrenos vazios: {QUANTIDADE_VAZIOS}")
print(f"Focos de incêndio: {len(focos_iniciais)}")