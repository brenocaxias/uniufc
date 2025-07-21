import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def abrir_crud_usuarios(conexao):
    def listar_usuarios():
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT login, nome, nivel_acesso FROM USUARIO_ACESSO")
            for login, nome, tipo in cursor.fetchall():
                tree.insert("", "end", iid=login, values=(nome, login, tipo))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar usuários:\n{e}")

    def adicionar_usuario():
        nome = simpledialog.askstring("Nome", "Digite o nome do usuário:")
        login = simpledialog.askstring("Login", "Digite o login do usuário:")
        senha = simpledialog.askstring("Senha", "Digite a senha:")
        tipo = simpledialog.askstring("Nível de Acesso", "Digite o nível (DBA, funcionario, aluno, professor):")
        if nome and login and senha and tipo:
            try:
                cursor = conexao.cursor()
                cursor.execute("""
                    INSERT INTO USUARIO_ACESSO (login, nome, senha, nivel_acesso)
                    VALUES (%s, %s, %s, %s)
                """, (login, nome, senha, tipo))
                conexao.commit()
                listar_usuarios()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar usuário:\n{e}")

    def excluir_usuario():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um usuário para excluir.")
            return
        confirmar = messagebox.askyesno("Confirmar", "Deseja excluir este usuário?")
        if confirmar:
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM USUARIO_ACESSO WHERE login = %s", (item,))
                conexao.commit()
                listar_usuarios()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir usuário:\n{e}")

    janela = tk.Toplevel()
    janela.title("CRUD - Usuários do Sistema")
    janela.geometry("650x350")

    tree = ttk.Treeview(janela, columns=("nome", "login", "tipo"), show="headings")
    tree.heading("nome", text="Nome")
    tree.heading("login", text="Login")
    tree.heading("tipo", text="Nível de Acesso")
    tree.pack(fill="both", expand=True, pady=10)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=5)

    tk.Button(frame_botoes, text="Adicionar", width=15, command=adicionar_usuario).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Excluir", width=15, command=excluir_usuario).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)

    listar_usuarios()