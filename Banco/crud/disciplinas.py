
# Gerencia as operações de CRUD para a entidade DISCIPLINA,
# incluindo o gerenciamento de pré-requisitos (relacionamento N:M recursivo).

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


def gerenciar_prerequisitos(conexao, disciplina_id, disciplina_nome):
    """
    Cria uma nova janela para gerenciar os pré-requisitos de uma disciplina.

    :param conexao: Objeto de conexão com o banco de dados.
    :param disciplina_id: O código da disciplina principal.
    :param disciplina_nome: O nome da disciplina principal.
    """
    janela_pr = tk.Toplevel()
    janela_pr.title(f"Pré-requisitos - {disciplina_nome}")
    janela_pr.geometry("600x400")

    lista = tk.Listbox(janela_pr, width=70)
    lista.pack(pady=10, fill="both", expand=True)

    def carregar():
        """
        Carrega a lista de pré-requisitos da disciplina selecionada.
        """
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
        """
        Adiciona uma nova disciplina como pré-requisito.
        """
        codigo_pr = simpledialog.askstring("Adicionar Pré-requisito", "Código da disciplina que será pré-requisito:")
        if codigo_pr:
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
        """
        Remove um pré-requisito selecionado.
        """
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
    """
    Cria a janela do CRUD de disciplinas.

    :param conexao: Objeto de conexão com o banco de dados.
    """

    def listar_disciplinas():
        """
        Lista todas as disciplinas, exibindo o nome do curso associado.
        """
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
        """
        Abre uma nova janela para adicionar uma disciplina.
        """
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
            """
            Coleta os dados e insere a nova disciplina no banco.
            """
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

    def editar_disciplina():
        """
        Abre uma nova janela para editar uma disciplina selecionada.
        """
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione uma disciplina para editar.")
            return

        valores_atuais = tree.item(item, "values")
        codigo_antigo = valores_atuais[0]

        janela_edit = tk.Toplevel()
        janela_edit.title(f"Editar Disciplina (Código: {codigo_antigo})")

        tk.Label(janela_edit, text="Nome:").grid(row=0, column=0)
        nome_entry = tk.Entry(janela_edit)
        nome_entry.insert(0, valores_atuais[1])
        nome_entry.grid(row=0, column=1)

        tk.Label(janela_edit, text="Ementa:").grid(row=1, column=0)
        ementa_text = tk.Text(janela_edit, height=4, width=40)
        # Buscar a ementa completa, pois o Treeview mostra uma versão truncada
        try:
            cursor_ementa = conexao.cursor()
            cursor_ementa.execute("SELECT ementa FROM DISCIPLINA WHERE codigo = %s", (codigo_antigo,))
            ementa_completa = cursor_ementa.fetchone()
            if ementa_completa:
                ementa_text.insert("1.0", ementa_completa[0])
        except Exception:
            ementa_text.insert("1.0", valores_atuais[2])  # Usa a truncada se der erro
        ementa_text.grid(row=1, column=1)

        tk.Label(janela_edit, text="Créditos:").grid(row=2, column=0)
        creditos_entry = tk.Entry(janela_edit)
        creditos_entry.insert(0, valores_atuais[3])
        creditos_entry.grid(row=2, column=1)

        tk.Label(janela_edit, text="Tipo (obrigatoria/optativa):").grid(row=3, column=0)
        tipo_entry = tk.Entry(janela_edit)
        tipo_entry.insert(0, valores_atuais[4])
        tipo_entry.grid(row=3, column=1)

        tk.Label(janela_edit, text="Código do Curso:").grid(row=4, column=0)
        curso_codigo_entry = tk.Entry(janela_edit)
        # Tenta preencher o código do curso pelo nome atual
        try:
            cursor_curso = conexao.cursor()
            cursor_curso.execute("SELECT codigo FROM CURSO WHERE nome = %s", (valores_atuais[5],))
            codigo_curso_atual = cursor_curso.fetchone()
            if codigo_curso_atual:
                curso_codigo_entry.insert(0, codigo_curso_atual[0])
        except Exception:
            curso_codigo_entry.insert(0, "")  # Caso não encontre ou erro
        curso_codigo_entry.grid(row=4, column=1)

        def salvar_edicao():
            """
            Salva as alterações da disciplina no banco de dados.
            """
            try:
                novo_nome = nome_entry.get()
                nova_ementa = ementa_text.get("1.0", "end").strip()
                novos_creditos = int(creditos_entry.get())
                novo_tipo = tipo_entry.get()
                novo_codigo_curso = int(curso_codigo_entry.get())

                cursor = conexao.cursor()
                cursor.execute("""
                    UPDATE DISCIPLINA SET 
                    nome = %s, 
                    ementa = %s, 
                    numero_creditos = %s, 
                    tipo = %s, 
                    codigo_curso = %s 
                    WHERE codigo = %s
                """, (novo_nome, nova_ementa, novos_creditos, novo_tipo, novo_codigo_curso, codigo_antigo))
                conexao.commit()
                janela_edit.destroy()
                listar_disciplinas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao editar disciplina:\n{e}")

        tk.Button(janela_edit, text="Salvar Alterações", command=salvar_edicao).grid(row=5, columnspan=2, pady=10)

    def excluir_disciplina():
        """
        Exclui uma disciplina selecionada do banco de dados.
        """
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

    def abrir_prerequisitos():
        """
        Abre a janela de gerenciamento de pré-requisitos para a disciplina selecionada.
        """
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione uma disciplina para gerenciar pré-requisitos.")
            return
        nome = tree.item(item)["values"][1]
        gerenciar_prerequisitos(conexao, item, nome)

    # ----- Interface da Janela -----
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
    tk.Button(frame_botoes, text="Editar", width=15, command=editar_disciplina).pack(side="left",
                                                                                     padx=5)  # Botão de Editar
    tk.Button(frame_botoes, text="Excluir", width=15, command=excluir_disciplina).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Pré-requisitos", width=15, command=abrir_prerequisitos).pack(side="left", padx=5)

    listar_disciplinas()