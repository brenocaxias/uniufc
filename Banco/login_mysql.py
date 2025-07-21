# Gerencia a tela de login inicial para o banco de dados MySQL.

import tkinter as tk
from tkinter import messagebox
from conexao import conectar_bd


def login_bd():
    """
    Cria a interface de login do BD.
    Retorna o objeto de conexão se for bem-sucedida, caso contrário, None.
    """
    conexao_result = None

    def conectar():
        nonlocal conexao_result
        usuario = entry_usuario.get()
        senha = entry_senha.get()

        conexao = conectar_bd(usuario, senha)

        if conexao:
            conexao_result = conexao
            root.destroy()
        else:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.\nVerifique as credenciais.")

    # ----- Interface gráfica da janela de login do BD -----
    root = tk.Tk()
    root.title("Login - Banco de Dados UniUFC-BD")
    root.geometry("350x200")
    root.resizable(False, False)

    tk.Label(root, text="Usuário MySQL:").pack(pady=(20, 0))
    entry_usuario = tk.Entry(root)
    entry_usuario.pack()

    tk.Label(root, text="Senha MySQL:").pack()
    entry_senha = tk.Entry(root, show="*")
    entry_senha.pack()

    btn_login = tk.Button(root, text="Conectar", command=conectar)
    btn_login.pack(pady=15)

    root.mainloop()

    # Retorna o resultado da conexão após a janela ser fechada
    return conexao_result