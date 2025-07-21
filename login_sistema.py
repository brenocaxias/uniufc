
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from telaprincipal import menu_principal

def abrir_menu_principal(nivel_acesso, nome, conexao, id_usuario=None):
    """
    Função que abre o menu principal do sistema após o login.

    :param nivel_acesso: O nível de acesso do usuário (DBA, professor, etc.).
    :param nome: O nome do usuário.
    :param conexao: O objeto de conexão com o banco de dados.
    :param id_usuario: O login do usuário (SIAPE, matrícula, etc.), opcional.
    """
    menu_principal(nivel_acesso, nome, conexao, id_usuario)

def login_sistema(conexao):
    def autenticar():
        login = entry_login.get()
        senha = entry_senha.get()

        try:
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT * FROM USUARIO_ACESSO WHERE login = %s AND senha = %s"
            cursor.execute(query, (login, senha))
            usuario = cursor.fetchone()

            if usuario:
                # Login bem-sucedido via tabela
                root.destroy()  # Destruir a janela de login antes de abrir a próxima
                messagebox.showinfo("Bem-vindo", f"Acesso concedido a {usuario['nome']} ({usuario['nivel_acesso']})")
                abrir_menu_principal(usuario['nivel_acesso'], usuario['nome'], conexao, login)

            elif login.lower() == "admin" and senha == "Root":
                # Verifica se é o Admin padrão, caso não tenha sido encontrado na tabela
                root.destroy()  # Destruir a janela de login antes de abrir a próxima
                messagebox.showinfo("Bem-vindo", f"Acesso concedido a Administrador (DBA)")
                abrir_menu_principal("DBA", "Administrador", conexao, login)

            else:
                messagebox.showerror("Erro", "Usuário ou senha inválidos.")
        except mysql.connector.Error as e:
            messagebox.showerror("Erro de BD", str(e))

    global root
    root = tk.Tk()
    root.title("Login - Sistema UniUFC-BD")
    root.geometry("350x200")
    root.resizable(False, False)

    tk.Label(root, text="Login:").pack(pady=(20, 0))
    entry_login = tk.Entry(root)
    entry_login.pack()

    tk.Label(root, text="Senha:").pack()
    entry_senha = tk.Entry(root, show="*")
    entry_senha.pack()

    btn_login = tk.Button(root, text="Entrar", command=autenticar)
    btn_login.pack(pady=15)

    root.mainloop()