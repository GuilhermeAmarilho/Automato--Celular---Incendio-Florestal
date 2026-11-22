
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random

from configuracoes import (
    TAMANHO_CELULA, VAZIO, FOGO, CORES,
    NOMES_ESTADOS, DIRECOES, INTENSIDADES,
    VELOCIDADE_INICIAL, PASTA_ESTADOS, ARQUIVO_ESTADO
)
from arquivos import carregar_estado, salvar_estado
from automato import proxima_geracao
from estatisticas import calcular_estatisticas


class Simulador:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title(
            "Autômato Celular - Incêndio Florestal"
        )
        self.janela.resizable(False, False)

        # Estado da simulação
        self.grade, self.tempos, self.geracao = (
            carregar_estado(ARQUIVO_ESTADO)
        )
        self.linhas = len(self.grade)
        self.colunas = len(self.grade[0])

        self.gerador = random.Random(42)
        self.executando = False
        self.agendamento = None
        self.velocidade = VELOCIDADE_INICIAL

        # Variáveis da interface
        self.direcao_var = tk.StringVar(value="Leste")
        self.intensidade_var = tk.StringVar(value="Moderado")
        self.estado_var = tk.StringVar(value="Árvore em chamas")

        self.registrar_estado_inicial()
        self.criar_interface()

        self.janela.protocol(
            "WM_DELETE_WINDOW", self.fechar
        )

    # ======================================
    # CONSTRUÇÃO DA INTERFACE
    # ======================================

    def criar_interface(self):
        tk.Label(
            self.janela,
            text="Simulador de Incêndio Florestal",
            font=("Arial", 16, "bold"),
            pady=10
        ).pack()

        frame_principal = tk.Frame(self.janela)
        frame_principal.pack(padx=12, pady=5)

        self.canvas = tk.Canvas(
            frame_principal,
            width=self.colunas * TAMANHO_CELULA,
            height=self.linhas * TAMANHO_CELULA,
            highlightthickness=0
        )
        self.canvas.pack(side="left")

        self.celulas_visuais = []
        self.criar_grade_visual()

        self.canvas.bind("<Button-1>", self.pintar_celula)
        self.canvas.bind("<B1-Motion>", self.pintar_celula)
        self.canvas.bind("<Button-3>", self.apagar_celula)
        self.canvas.bind("<B3-Motion>", self.apagar_celula)

        self.criar_painel_estatisticas(frame_principal)

        self.label_geracao = tk.Label(
            self.janela,
            text=f"Geração: {self.geracao}",
            font=("Arial", 12, "bold")
        )
        self.label_geracao.pack(pady=5)

        self.criar_botoes()
        self.criar_configuracoes()
        self.criar_editor()

        tk.Label(
            self.janela,
            text=(
                "Cinza: Vazio | Verde: Árvore | Vermelho: Fogo\n"
                "Preto: Queimado | Verde-claro: Regenerando"
            ),
            font=("Arial", 9),
            pady=5
        ).pack()

        self.atualizar_estatisticas()

    # ======================================
    # GRADE
    # ======================================

    def criar_grade_visual(self):
        self.canvas.delete("all")
        self.canvas.config(
            width=self.colunas * TAMANHO_CELULA,
            height=self.linhas * TAMANHO_CELULA
        )

        self.celulas_visuais = []

        for linha in range(self.linhas):
            celulas_linha = []

            for coluna in range(self.colunas):
                x1 = coluna * TAMANHO_CELULA
                y1 = linha * TAMANHO_CELULA

                retangulo = self.canvas.create_rectangle(
                    x1, y1,
                    x1 + TAMANHO_CELULA,
                    y1 + TAMANHO_CELULA,
                    fill=CORES[self.grade[linha][coluna]],
                    outline="#222222",
                    width=0.3
                )
                celulas_linha.append(retangulo)

            self.celulas_visuais.append(celulas_linha)

    def atualizar_visualizacao(self):
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                self.canvas.itemconfig(
                    self.celulas_visuais[linha][coluna],
                    fill=CORES[self.grade[linha][coluna]]
                )

        self.label_geracao.config(
            text=f"Geração: {self.geracao}"
        )
        self.atualizar_estatisticas()

    # ======================================
    # PAINEL ESTATÍSTICO
    # ======================================

    def criar_painel_estatisticas(self, frame_pai):
        painel = tk.LabelFrame(
            frame_pai,
            text="Estatísticas da Floresta",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=12
        )
        painel.pack(side="left", padx=(15, 0), fill="y")

        self.labels_estatisticas = {}

        for estado, nome in [
            (0, "Terreno vazio"),
            (1, "Árvores saudáveis"),
            (2, "Árvores em chamas"),
            (3, "Terreno queimado"),
            (4, "Regenerando")
        ]:
            item = tk.Frame(painel)
            item.pack(fill="x", pady=8, anchor="w")

            tk.Label(
                item, bg=CORES[estado],
                width=2, height=1
            ).pack(side="left", padx=(0, 8))

            texto = tk.Frame(item)
            texto.pack(side="left")

            tk.Label(
                texto, text=nome,
                font=("Arial", 9)
            ).pack(anchor="w")

            label = tk.Label(
                texto, text="0",
                font=("Arial", 13, "bold")
            )
            label.pack(anchor="w")

            self.labels_estatisticas[estado] = label

        ttk.Separator(
            painel, orient="horizontal"
        ).pack(fill="x", pady=10)

        tk.Label(
            painel, text="Total de células",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.label_total = tk.Label(
            painel, text="0",
            font=("Arial", 16, "bold")
        )
        self.label_total.pack(anchor="w")

        tk.Label(
            painel, text="Área em chamas",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(15, 0))

        self.label_percentual = tk.Label(
            painel, text="0,00%",
            font=("Arial", 14, "bold"),
            fg="#DC2626"
        )
        self.label_percentual.pack(anchor="w")

    def atualizar_estatisticas(self):
        contadores = calcular_estatisticas(self.grade)
        total = self.linhas * self.colunas

        for estado, quantidade in contadores.items():
            self.labels_estatisticas[estado].config(
                text=f"{quantidade:,}".replace(",", ".")
            )

        self.label_total.config(
            text=f"{total:,}".replace(",", ".")
        )

        percentual = (
            contadores[FOGO] / total * 100 if total else 0
        )
        self.label_percentual.config(
            text=f"{percentual:.2f}%".replace(".", ",")
        )

    # ======================================
    # BOTÕES
    # ======================================

    def criar_botoes(self):
        frame = tk.Frame(self.janela)
        frame.pack(pady=5)

        botoes = [
            ("Play", self.play, "#16A34A", "white"),
            ("Pause", self.pause, "#EAB308", "black"),
            ("Step", self.step, "#2563EB", "white"),
            ("Reset", self.reset, "#DC2626", "white")
        ]

        for coluna, (texto, comando, cor, fonte) in enumerate(botoes):
            tk.Button(
                frame, text=texto, command=comando,
                bg=cor, fg=fonte, width=12,
                font=("Arial", 10, "bold")
            ).grid(row=0, column=coluna, padx=5)

        frame_arquivos = tk.Frame(self.janela)
        frame_arquivos.pack(pady=5)

        tk.Button(
            frame_arquivos,
            text="Salvar floresta",
            command=self.salvar_arquivo,
            bg="#0F766E", fg="white",
            width=20, font=("Arial", 10, "bold")
        ).grid(row=0, column=0, padx=6)

        tk.Button(
            frame_arquivos,
            text="Carregar floresta",
            command=self.carregar_arquivo,
            bg="#475569", fg="white",
            width=20, font=("Arial", 10, "bold")
        ).grid(row=0, column=1, padx=6)

    # ======================================
    # CONFIGURAÇÕES
    # ======================================

    def criar_configuracoes(self):
        painel = tk.LabelFrame(
            self.janela,
            text="Configurações da Simulação",
            font=("Arial", 10, "bold"),
            padx=12, pady=8
        )
        painel.pack(fill="x", padx=15, pady=6)

        tk.Label(
            painel, text="Direção do vento:"
        ).grid(row=0, column=0, padx=5, pady=5)

        ttk.Combobox(
            painel, textvariable=self.direcao_var,
            values=list(DIRECOES.keys()),
            state="readonly", width=16
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            painel, text="Intensidade:"
        ).grid(row=0, column=2, padx=5, pady=5)

        ttk.Combobox(
            painel, textvariable=self.intensidade_var,
            values=list(INTENSIDADES.keys()),
            state="readonly", width=14
        ).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(
            painel, text="Intervalo entre gerações:"
        ).grid(row=1, column=0, columnspan=2, padx=5)

        self.label_velocidade = tk.Label(
            painel, text=f"{self.velocidade} ms"
        )
        self.label_velocidade.grid(row=1, column=3)

        slider = tk.Scale(
            painel, from_=50, to=1000,
            resolution=50, orient="horizontal",
            showvalue=False,
            command=self.alterar_velocidade,
            length=230
        )
        slider.set(self.velocidade)
        slider.grid(row=1, column=2, pady=5)

    def alterar_velocidade(self, valor):
        self.velocidade = int(float(valor))
        self.label_velocidade.config(
            text=f"{self.velocidade} ms"
        )

    # ======================================
    # EDITOR DA FLORESTA
    # ======================================

    def criar_editor(self):
        painel = tk.LabelFrame(
            self.janela, text="Editor da Floresta",
            font=("Arial", 10, "bold"),
            padx=12, pady=8
        )
        painel.pack(fill="x", padx=15, pady=6)

        tk.Label(
            painel, text="Estado para desenhar:"
        ).pack(side="left", padx=5)

        ttk.Combobox(
            painel, textvariable=self.estado_var,
            values=list(NOMES_ESTADOS.keys()),
            state="readonly", width=24
        ).pack(side="left", padx=5)

        tk.Label(
            painel,
            text="Esquerdo: pintar | Direito: apagar",
            font=("Arial", 9), fg="#555555"
        ).pack(side="left", padx=10)

    def obter_posicao_mouse(self, evento):
        coluna = evento.x // TAMANHO_CELULA
        linha = evento.y // TAMANHO_CELULA

        if 0 <= linha < self.linhas and 0 <= coluna < self.colunas:
            return linha, coluna

        return None

    def alterar_celula(self, evento, novo_estado):
        posicao = self.obter_posicao_mouse(evento)

        if posicao is None:
            return

        self.pause()
        linha, coluna = posicao

        if self.grade[linha][coluna] == novo_estado:
            return

        self.grade[linha][coluna] = novo_estado
        self.tempos[linha][coluna] = 0

        self.canvas.itemconfig(
            self.celulas_visuais[linha][coluna],
            fill=CORES[novo_estado]
        )
        self.atualizar_estatisticas()

    def pintar_celula(self, evento):
        estado = NOMES_ESTADOS[self.estado_var.get()]
        self.alterar_celula(evento, estado)

    def apagar_celula(self, evento):
        self.alterar_celula(evento, VAZIO)

    # ======================================
    # SALVAR E CARREGAR
    # ======================================

    def registrar_estado_inicial(self):
        self.grade_inicial = [
            linha.copy() for linha in self.grade
        ]
        self.tempos_iniciais = [
            linha.copy() for linha in self.tempos
        ]
        self.geracao_inicial = self.geracao

    def salvar_arquivo(self):
        self.pause()

        caminho = filedialog.asksaveasfilename(
            title="Salvar estado da floresta",
            initialdir=str(PASTA_ESTADOS),
            initialfile="floresta_salva.txt",
            defaultextension=".txt",
            filetypes=[("Arquivos de texto", "*.txt")]
        )

        if not caminho:
            return

        try:
            salvar_estado(
                caminho, self.grade,
                self.tempos, self.geracao
            )
            messagebox.showinfo(
                "Arquivo salvo",
                "A floresta foi salva com sucesso!"
            )
        except OSError as erro:
            messagebox.showerror("Erro ao salvar", str(erro))

    def carregar_arquivo(self):
        self.pause()

        caminho = filedialog.askopenfilename(
            title="Carregar estado da floresta",
            initialdir=str(PASTA_ESTADOS),
            filetypes=[("Arquivos de texto", "*.txt")]
        )

        if not caminho:
            return

        try:
            grade, tempos, geracao = carregar_estado(caminho)
        except (OSError, ValueError) as erro:
            messagebox.showerror("Erro ao carregar", str(erro))
            return

        self.grade = grade
        self.tempos = tempos
        self.geracao = geracao
        self.linhas = len(grade)
        self.colunas = len(grade[0])

        self.gerador.seed(42)
        self.registrar_estado_inicial()
        self.criar_grade_visual()
        self.atualizar_visualizacao()

        messagebox.showinfo(
            "Arquivo carregado",
            "A floresta foi carregada com sucesso!"
        )

    # ======================================
    # CONTROLES DA SIMULAÇÃO
    # ======================================

    def avancar(self):
        direcao = DIRECOES[self.direcao_var.get()]
        intensidade = INTENSIDADES[self.intensidade_var.get()]

        self.grade, self.tempos = proxima_geracao(
            self.grade, self.tempos,
            direcao, intensidade, self.gerador
        )

        self.geracao += 1
        self.atualizar_visualizacao()

    def play(self):
        if self.executando:
            return

        self.executando = True
        self.executar_automaticamente()

    def executar_automaticamente(self):
        self.agendamento = None

        if not self.executando:
            return

        self.avancar()

        self.agendamento = self.janela.after(
            self.velocidade,
            self.executar_automaticamente
        )

    def pause(self):
        self.executando = False

        if self.agendamento is not None:
            self.janela.after_cancel(self.agendamento)
            self.agendamento = None

    def step(self):
        self.pause()
        self.avancar()

    def reset(self):
        self.pause()

        self.grade = [
            linha.copy() for linha in self.grade_inicial
        ]
        self.tempos = [
            linha.copy() for linha in self.tempos_iniciais
        ]

        self.geracao = self.geracao_inicial
        self.gerador.seed(42)

        self.atualizar_visualizacao()

    def fechar(self):
        self.pause()
        self.janela.destroy()
