import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


def abrir_gerenciador_contatos(conexao):
    def listar():
        tipo = tipo_var.get()
        id_pessoa = entry_id.get()
        if not id_pessoa:
            messagebox.showwarning("Atenção", "Informe o ID da pessoa (Matrícula ou SIAPE).")
            return

        for i in tree_email.get_children():
            tree_email.delete(i)
        for i in tree_fone.get_children():
            tree_fone.delete(i)

        try:
            cursor = conexao.cursor()

            if tipo == "Professor":
                cursor.execute("SELECT id_email, email FROM EMAIL_PROFESSOR WHERE siape_professor = %s", (id_pessoa,))
                for id_, email in cursor.fetchall():
                    tree_email.insert("", "end", iid=f"e{id_}", values=(email,))

                cursor.execute("SELECT id_telefone, numero FROM TELEFONE_PROFESSOR WHERE siape_professor = %s",
                               (id_pessoa,))
                for id_, numero in cursor.fetchall():
                    tree_fone.insert("", "end", iid=f"t{id_}", values=(numero, "Sem Descrição"))
            elif tipo == "Aluno":
                cursor.execute("SELECT id_telefone, numero, descricao FROM TELEFONE_ALUNO WHERE matricula_aluno = %s",
                               (id_pessoa,))
                for id_, numero, desc in cursor.fetchall():
                    tree_fone.insert("", "end", iid=f"t{id_}", values=(numero, desc))


        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar contatos:\n{e}")

    def adicionar_email():
        tipo = tipo_var.get()
        if tipo != "Professor":
            messagebox.showerror("Erro", "E-mails só podem ser adicionados a professores.")
            return
        id_pessoa = entry_id.get()
        email = simpledialog.askstring("Novo E-mail", "Digite o e-mail:")
        if email:
            try:
                cursor = conexao.cursor()
                cursor.execute("INSERT INTO EMAIL_PROFESSOR (email, siape_professor) VALUES (%s, %s)",
                               (email, id_pessoa))
                conexao.commit()
                listar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar e-mail:\n{e}")

    def adicionar_telefone():
        tipo = tipo_var.get()
        id_pessoa = entry_id.get()
        numero = simpledialog.askstring("Número", "Digite o telefone:")
        desc = simpledialog.askstring("Descrição", "Digite a descrição (Ex: Celular, Residencial):")
        if numero:
            try:
                cursor = conexao.cursor()
                if tipo == "Professor":
                    cursor.execute("INSERT INTO TELEFONE_PROFESSOR (numero, siape_professor) VALUES (%s, %s)",
                                   (numero, id_pessoa))
                elif tipo == "Aluno":
                    cursor.execute(
                        "INSERT INTO TELEFONE_ALUNO (numero, descricao, matricula_aluno) VALUES (%s, %s, %s)",
                        (numero, desc, id_pessoa))
                conexao.commit()
                listar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar telefone:\n{e}")

    def excluir_email():
        item = tree_email.focus()
        if not item: return
        id_ = item[1:]
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM EMAIL_PROFESSOR WHERE id_email = %s", (id_,))
            conexao.commit()
            listar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir e-mail:\n{e}")

    def excluir_telefone():
        item = tree_fone.focus()
        if not item: return
        id_ = item[1:]
        tipo = tipo_var.get()
        try:
            cursor = conexao.cursor()
            if tipo == "Professor":
                cursor.execute("DELETE FROM TELEFONE_PROFESSOR WHERE id_telefone = %s", (id_,))
            elif tipo == "Aluno":
                cursor.execute("DELETE FROM TELEFONE_ALUNO WHERE id_telefone = %s", (id_,))
            conexao.commit()
            listar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir telefone:\n{e}")

    janela = tk.Toplevel()
    janela.title("Contatos: Telefones e E-mails")
    janela.geometry("700x500")

    tk.Label(janela, text="Tipo de Pessoa:").pack()
    tipo_var = tk.StringVar(value="Aluno")
    tipo_menu = ttk.Combobox(janela, textvariable=tipo_var, values=["Aluno", "Professor"], state="readonly")
    tipo_menu.pack()

    tk.Label(janela, text="ID da Pessoa: (Matrícula ou SIAPE)").pack(pady=5)
    entry_id = tk.Entry(janela)
    entry_id.pack()

    tk.Button(janela, text="Buscar Contatos", command=listar).pack(pady=5)

    tk.Label(janela, text="E-mails").pack()
    tree_email = ttk.Treeview(janela, columns=("email",), show="headings")
    tree_email.heading("email", text="E-mail")
    tree_email.pack(pady=5, fill="x")

    frame_email = tk.Frame(janela)
    frame_email.pack(pady=2)
    tk.Button(frame_email, text="Adicionar E-mail", command=adicionar_email).pack(side="left", padx=5)
    tk.Button(frame_email, text="Excluir E-mail", command=excluir_email).pack(side="left", padx=5)

    tk.Label(janela, text="Telefones").pack(pady=5)
    tree_fone = ttk.Treeview(janela, columns=("numero", "descricao"), show="headings")
    tree_fone.heading("numero", text="Número")
    tree_fone.heading("descricao", text="Descrição")
    tree_fone.pack(pady=5, fill="x")

    frame_fone = tk.Frame(janela)
    frame_fone.pack(pady=2)
    tk.Button(frame_fone, text="Adicionar Telefone", command=adicionar_telefone).pack(side="left", padx=5)
    tk.Button(frame_fone, text="Excluir Telefone", command=excluir_telefone).pack(side="left", padx=5)