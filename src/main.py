
import tkinter as tk
from tkinter import messagebox

from interface import Simulador


def main():
    janela = tk.Tk()

    try:
        Simulador(janela)

    except (OSError, ValueError) as erro:
        messagebox.showerror(
            "Erro ao iniciar",
            str(erro)
        )
        janela.destroy()
        return

    janela.mainloop()


if __name__ == "__main__":
    main()
