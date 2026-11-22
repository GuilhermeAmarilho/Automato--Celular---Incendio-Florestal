
import math

from configuracoes import (
    VAZIO, ARVORE, FOGO, QUEIMADO, REGENERANDO,
    PROBABILIDADE_FOGO,
    DURACAO_FOGO,
    DURACAO_QUEIMADO,
    DURACAO_REGENERACAO
)


def calcular_probabilidade(
    linha, coluna, grade, direcao_vento, intensidade_vento
):
    """Calcula a probabilidade de uma árvore incendiar."""

    linhas = len(grade)
    colunas = len(grade[0])

    prob_nao_queimar = 1.0

    vento_x, vento_y = direcao_vento
    tamanho_vento = math.hypot(vento_x, vento_y)

    # Vizinhança de Moore
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:

            if dx == 0 and dy == 0:
                continue

            vl = linha + dy
            vc = coluna + dx

            if not (0 <= vl < linhas and 0 <= vc < colunas):
                continue

            if grade[vl][vc] != FOGO:
                continue

            # Direção do vizinho em chamas até a árvore
            direcao_x = -dx
            direcao_y = -dy

            tamanho_direcao = math.hypot(
                direcao_x, direcao_y
            )

            if intensidade_vento == 0 or tamanho_vento == 0:
                influencia = 0
            else:
                influencia = (
                    direcao_x * vento_x
                    + direcao_y * vento_y
                ) / (tamanho_direcao * tamanho_vento)

            probabilidade = PROBABILIDADE_FOGO * (
                1 + intensidade_vento * influencia
            )

            probabilidade = max(
                0.0, min(1.0, probabilidade)
            )

            prob_nao_queimar *= (1 - probabilidade)

    return 1 - prob_nao_queimar


def proxima_geracao(
    grade, tempos, direcao_vento, intensidade_vento, gerador
):
    """Calcula a próxima geração do autômato celular."""

    linhas = len(grade)
    colunas = len(grade[0])

    # Grades auxiliares garantem atualização simultânea
    nova_grade = [linha.copy() for linha in grade]
    novos_tempos = [linha.copy() for linha in tempos]

    for linha in range(linhas):
        for coluna in range(colunas):

            estado = grade[linha][coluna]
            tempo = tempos[linha][coluna]

            if estado == VAZIO:
                continue

            elif estado == ARVORE:
                probabilidade = calcular_probabilidade(
                    linha, coluna, grade,
                    direcao_vento, intensidade_vento
                )

                if gerador.random() < probabilidade:
                    nova_grade[linha][coluna] = FOGO
                    novos_tempos[linha][coluna] = 0

            elif estado == FOGO:
                if tempo + 1 >= DURACAO_FOGO:
                    nova_grade[linha][coluna] = QUEIMADO
                    novos_tempos[linha][coluna] = 0
                else:
                    novos_tempos[linha][coluna] = tempo + 1

            elif estado == QUEIMADO:
                if tempo + 1 >= DURACAO_QUEIMADO:
                    nova_grade[linha][coluna] = REGENERANDO
                    novos_tempos[linha][coluna] = 0
                else:
                    novos_tempos[linha][coluna] = tempo + 1

            elif estado == REGENERANDO:
                if tempo + 1 >= DURACAO_REGENERACAO:
                    nova_grade[linha][coluna] = ARVORE
                    novos_tempos[linha][coluna] = 0
                else:
                    novos_tempos[linha][coluna] = tempo + 1

    return nova_grade, novos_tempos
