# Gerencia as operações de CRUD para a tabela de controle de acesso USUARIO_ACESSO.

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


def abrir_crud_usuarios(conexao):
    """
    Cria a janela do CRUD de usuários do sistema.

    :param conexao: Objeto de conexão com o banco de dados.
    """

    def listar_usuarios():
        """
        Lista todos os usuários de acesso ao sistema.
        """
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT login, nome, senha, nivel_acesso FROM USUARIO_ACESSO")  # Adicionei 'senha' para facilitar a edição
            for login, nome, senha, tipo in cursor.fetchall():
                tree.insert("", "end", iid=login, values=(nome, login, senha, tipo))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar usuários:\n{e}")

    def adicionar_usuario():
        """
        Adiciona um novo usuário de acesso.
        """
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

    def editar_usuario():
        """
        Abre uma nova janela para editar um usuário de acesso selecionado.
        """
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um usuário para editar.")
            return

        valores_atuais = tree.item(item, "values")
        login_antigo = valores_atuais[1]  # Login é o segundo valor na Treeview

        janela_edit = tk.Toplevel()
        janela_edit.title(f"Editar Usuário (Login: {login_antigo})")

        tk.Label(janela_edit, text="Nome:").grid(row=0, column=0)
        nome_entry = tk.Entry(janela_edit)
        nome_entry.insert(0, valores_atuais[0])  # Nome é o primeiro valor na Treeview
        nome_entry.grid(row=0, column=1)

        tk.Label(janela_edit, text="Senha:").grid(row=1, column=0)
        senha_entry = tk.Entry(janela_edit, show="*")  # Campo de senha, oculto
        senha_entry.insert(0, valores_atuais[2])  # Senha é o terceiro valor
        senha_entry.grid(row=1, column=1)

        tk.Label(janela_edit, text="Nível de Acesso:").grid(row=2, column=0)
        tipo_entry = tk.Entry(janela_edit)
        tipo_entry.insert(0, valores_atuais[3])  # Tipo é o quarto valor
        tipo_entry.grid(row=2, column=1)

        def salvar_edicao():
            """
            Salva as alterações do usuário no banco de dados.
            """
            try:
                novo_nome = nome_entry.get()
                nova_senha = senha_entry.get()
                novo_tipo = tipo_entry.get()

                cursor = conexao.cursor()
                cursor.execute("""
                    UPDATE USUARIO_ACESSO SET 
                    nome = %s, 
                    senha = %s, 
                    nivel_acesso = %s 
                    WHERE login = %s
                """, (novo_nome, nova_senha, novo_tipo, login_antigo))
                conexao.commit()
                janela_edit.destroy()
                listar_usuarios()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao editar usuário:\n{e}")

        tk.Button(janela_edit, text="Salvar Alterações", command=salvar_edicao).grid(row=3, columnspan=2, pady=10)

    def excluir_usuario():
        """
        Exclui um usuário de acesso selecionado.
        """
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

    # ----- Interface da Janela -----
    janela = tk.Toplevel()
    janela.title("CRUD - Usuários do Sistema")
    janela.geometry("650x350")

    tree = ttk.Treeview(janela, columns=("nome", "login", "senha", "tipo"),
                        show="headings")  # Adicionado 'senha' para exibição
    tree.heading("nome", text="Nome")
    tree.heading("login", text="Login")
    tree.heading("senha", text="Senha")  # Cabeçalho para a nova coluna de senha
    tree.heading("tipo", text="Nível de Acesso")
    tree.pack(fill="both", expand=True, pady=10)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=5)

    tk.Button(frame_botoes, text="Adicionar", width=15, command=adicionar_usuario).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Editar", width=15, command=editar_usuario).pack(side="left",
                                                                                  padx=5)  # Botão de Editar
    tk.Button(frame_botoes, text="Excluir", width=15, command=excluir_usuario).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)

    listar_usuarios()