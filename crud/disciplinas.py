import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


def gerenciar_prerequisitos(conexao, disciplina_id, disciplina_nome):
    janela_pr = tk.Toplevel()
    janela_pr.title(f"Pré-requisitos - {disciplina_nome}")
    janela_pr.geometry("600x400")

    lista = tk.Listbox(janela_pr, width=70)
    lista.pack(pady=10, fill="both", expand=True)

    def carregar():
        lista.delete(0, tk.END)
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT D2.codigo, D2.nome FROM PRE_REQUISITO_DISCIPLINA PR
            JOIN DISCIPLINA D2 ON D2.codigo = PR.codigo_pre_requisito
            WHERE PR.codigo_disciplina = %s
        """, (disciplina_id,))
        for codigo, nome in cursor.fetchall():
            lista.insert(tk.END, f"{codigo} - {nome}")

    def adicionar():
        codigo_pr = simpledialog.askstring("Adicionar Pré-requisito", "Código da disciplina que será pré-requisito:")
        try:
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO PRE_REQUISITO_DISCIPLINA (codigo_disciplina, codigo_pre_requisito) VALUES (%s, %s)",
                (disciplina_id, codigo_pr))
            conexao.commit()
            carregar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar pré-requisito:\n{e}")

    def remover():
        selecionado = lista.get(tk.ACTIVE)
        if not selecionado:
            return
        codigo_remover = selecionado.split(" - ")[0]
        try:
            cursor = conexao.cursor()
            cursor.execute(
                "DELETE FROM PRE_REQUISITO_DISCIPLINA WHERE codigo_disciplina = %s AND codigo_pre_requisito = %s",
                (disciplina_id, codigo_remover))
            conexao.commit()
            carregar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover pré-requisito:\n{e}")

    frame = tk.Frame(janela_pr)
    frame.pack(pady=10)
    tk.Button(frame, text="Adicionar", width=15, command=adicionar).pack(side="left", padx=5)
    tk.Button(frame, text="Remover", width=15, command=remover).pack(side="left", padx=5)
    tk.Button(frame, text="Fechar", width=15, command=janela_pr.destroy).pack(side="left", padx=5)

    carregar()


def abrir_crud_disciplinas(conexao):
    def listar_disciplinas():
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT D.codigo, D.nome, D.ementa, D.numero_creditos, D.tipo, C.nome 
                FROM DISCIPLINA D
                LEFT JOIN CURSO C ON D.codigo_curso = C.codigo
            """)
            for codigo, nome, ementa, creditos, tipo, curso in cursor.fetchall():
                tree.insert("", "end", iid=codigo, values=(codigo, nome, ementa[:40], creditos, tipo, curso or ""))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar disciplinas:\n{e}")

    def adicionar_disciplina():
        janela_add = tk.Toplevel()
        janela_add.title("Nova Disciplina")

        campos = {
            "Código": tk.Entry(janela_add),
            "Nome": tk.Entry(janela_add),
            "Ementa": tk.Text(janela_add, height=4, width=40),
            "Créditos": tk.Entry(janela_add),
            "Tipo (obrigatoria/optativa)": tk.Entry(janela_add),
            "Código do Curso": tk.Entry(janela_add)
        }

        for i, (label, widget) in enumerate(campos.items()):
            tk.Label(janela_add, text=label + ":").grid(row=i, column=0, sticky="w")
            widget.grid(row=i, column=1, pady=2)

        def salvar():
            try:
                codigo = campos["Código"].get()
                nome = campos["Nome"].get()
                ementa = campos["Ementa"].get("1.0", "end").strip()
                creditos = int(campos["Créditos"].get())
                tipo = campos["Tipo (obrigatoria/optativa)"].get()
                codigo_curso = int(campos["Código do Curso"].get())

                cursor = conexao.cursor()
                cursor.execute("""
                    INSERT INTO DISCIPLINA (codigo, nome, ementa, numero_creditos, tipo, codigo_curso)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (codigo, nome, ementa, creditos, tipo, codigo_curso))
                conexao.commit()
                janela_add.destroy()
                listar_disciplinas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar disciplina:\n{e}")

        tk.Button(janela_add, text="Salvar", command=salvar).grid(row=len(campos), columnspan=2, pady=10)

    def excluir_disciplina():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione uma disciplina para excluir.")
            return
        confirmar = messagebox.askyesno("Confirmar", "Deseja excluir esta disciplina?")
        if confirmar:
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM DISCIPLINA WHERE codigo = %s", (item,))
                conexao.commit()
                listar_disciplinas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir disciplina:\n{e}")

    janela = tk.Toplevel()
    janela.title("CRUD - Disciplinas")
    janela.geometry("850x400")

    tree = ttk.Treeview(janela, columns=("codigo", "nome", "ementa", "creditos", "tipo", "curso"), show="headings")
    for col in ("codigo", "nome", "ementa", "creditos", "tipo", "curso"):
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=120 if col != "ementa" else 200)

    tree.pack(fill="both", expand=True, pady=10)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=5)

    tk.Button(frame_botoes, text="Adicionar", width=15, command=adicionar_disciplina).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Excluir", width=15, command=excluir_disciplina).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)

    tk.Button(frame_botoes, text="Pré-requisitos", width=15, command=lambda: abrir_prerequisitos()).pack(side="left",
                                                                                                         padx=5)

    def abrir_prerequisitos():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione uma disciplina para gerenciar pré-requisitos.")
            return
        nome = tree.item(item)["values"][1]
        gerenciar_prerequisitos(conexao, item, nome)

    listar_disciplinas()