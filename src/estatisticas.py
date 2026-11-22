
from configuracoes import (
    VAZIO, ARVORE, FOGO, QUEIMADO, REGENERANDO
)


def calcular_estatisticas(grade):
    """Retorna a quantidade de células de cada estado."""

    contadores = {
        VAZIO: 0,
        ARVORE: 0,
        FOGO: 0,
        QUEIMADO: 0,
        REGENERANDO: 0
    }

    for linha in grade:
        for estado in linha:
            contadores[estado] += 1

    return contadores
