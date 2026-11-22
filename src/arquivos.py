
from configuracoes import CORES


def carregar_estado(caminho):
    """Carrega uma floresta de um arquivo TXT."""

    grade = []
    tempos = []
    geracao = 0

    with open(caminho, "r", encoding="utf-8") as arquivo:
        for numero_linha, conteudo in enumerate(arquivo, 1):

            conteudo = conteudo.strip()

            if not conteudo:
                continue

            if conteudo.startswith("#"):
                partes = conteudo[1:].strip().split()

                if partes and partes[0].upper() == "GERACAO":
                    if len(partes) != 2:
                        raise ValueError(
                            "Cabeçalho de geração inválido."
                        )

                    geracao = int(partes[1])

                    if geracao < 0:
                        raise ValueError(
                            "A geração não pode ser negativa."
                        )

                continue

            linha_estados = []
            linha_tempos = []

            for celula in conteudo.split():
                partes = celula.split(":")

                if len(partes) == 1:
                    estado = int(partes[0])
                    tempo = 0
                elif len(partes) == 2:
                    estado = int(partes[0])
                    tempo = int(partes[1])
                else:
                    raise ValueError(
                        f"Célula inválida na linha {numero_linha}."
                    )

                if estado not in CORES:
                    raise ValueError(
                        f"Estado inválido: {estado}"
                    )

                if tempo < 0:
                    raise ValueError(
                        "O tempo não pode ser negativo."
                    )

                linha_estados.append(estado)
                linha_tempos.append(tempo)

            grade.append(linha_estados)
            tempos.append(linha_tempos)

    if not grade:
        raise ValueError("O arquivo não contém células.")

    colunas = len(grade[0])

    if any(len(linha) != colunas for linha in grade):
        raise ValueError(
            "Todas as linhas devem ter o mesmo tamanho."
        )

    return grade, tempos, geracao


def salvar_estado(caminho, grade, tempos, geracao):
    """Salva os estados, tempos e geração atual."""

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(
            "# AUTOMATO CELULAR - INCENDIO FLORESTAL\n"
        )
        arquivo.write(f"# GERACAO {geracao}\n")

        for linha_estados, linha_tempos in zip(grade, tempos):
            celulas = [
                f"{estado}:{tempo}"
                for estado, tempo in zip(
                    linha_estados, linha_tempos
                )
            ]

            arquivo.write(" ".join(celulas) + "\n")
