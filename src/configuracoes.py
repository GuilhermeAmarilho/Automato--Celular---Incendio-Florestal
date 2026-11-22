
from pathlib import Path

# Dimensões visuais
TAMANHO_CELULA = 12

# Estados possíveis
VAZIO = 0
ARVORE = 1
FOGO = 2
QUEIMADO = 3
REGENERANDO = 4

# Cores dos estados
CORES = {
    VAZIO: "#A3A3A3",
    ARVORE: "#16A34A",
    FOGO: "#EF4444",
    QUEIMADO: "#404040",
    REGENERANDO: "#86EFAC"
}

# Nomes para o editor da floresta
NOMES_ESTADOS = {
    "Terreno vazio": VAZIO,
    "Árvore saudável": ARVORE,
    "Árvore em chamas": FOGO,
    "Terreno queimado": QUEIMADO,
    "Vegetação regenerando": REGENERANDO
}

# Regras de evolução
PROBABILIDADE_FOGO = 0.30
DURACAO_FOGO = 2
DURACAO_QUEIMADO = 8
DURACAO_REGENERACAO = 5

# Direções do vento (x, y)
DIRECOES = {
    "Norte": (0, -1),
    "Nordeste": (1, -1),
    "Leste": (1, 0),
    "Sudeste": (1, 1),
    "Sul": (0, 1),
    "Sudoeste": (-1, 1),
    "Oeste": (-1, 0),
    "Noroeste": (-1, -1)
}

# Intensidades do vento
INTENSIDADES = {
    "Sem vento": 0.0,
    "Moderado": 0.5,
    "Forte": 1.0
}

# Velocidade inicial em milissegundos
VELOCIDADE_INICIAL = 200

# Caminhos do projeto
PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_ESTADOS = PASTA_PROJETO / "estados"
ARQUIVO_ESTADO = PASTA_ESTADOS / "estado_inicial.txt"
