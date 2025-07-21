# Gerencia as operações de CRUD para a entidade CURSO.

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


def abrir_crud_cursos(conexao):
    """
    Cria a janela do CRUD de cursos.

    :param conexao: Objeto de conexão com o banco de dados.
    """

    def listar_cursos():
        """
        Lista todos os cursos, exibindo o nome do departamento associado.
        """
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT C.codigo, C.nome, C.quantidade_minima_creditos, D.nome 
                FROM CURSO C
                LEFT JOIN DEPARTAMENTO D ON C.codigo_departamento = D.codigo
            """)
            for codigo, nome, creditos, departamento in cursor.fetchall():
                tree.insert("", "end", iid=codigo, values=(codigo, nome, creditos, departamento or ""))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar cursos:\n{e}")

    def adicionar_curso():
        """
        Abre uma nova janela para adicionar um curso.
        """
        janela_add = tk.Toplevel()
        janela_add.title("Novo Curso")

        campos = {
            "Código": tk.Entry(janela_add),
            "Nome": tk.Entry(janela_add),
            "Créditos Mínimos": tk.Entry(janela_add),
            "Código do Departamento": tk.Entry(janela_add)
        }

        for i, (label, widget) in enumerate(campos.items()):
            tk.Label(janela_add, text=label + ":").grid(row=i, column=0, sticky="w")
            widget.grid(row=i, column=1, pady=2)

        def salvar():
            """
            Coleta os dados da janela de adição e insere o novo curso no banco.
            """
            try:
                codigo = campos["Código"].get()
                nome = campos["Nome"].get()
                creditos = int(campos["Créditos Mínimos"].get())
                depto_codigo = int(campos["Código do Departamento"].get())

                cursor = conexao.cursor()
                cursor.execute("""
                    INSERT INTO CURSO (codigo, nome, quantidade_minima_creditos, codigo_departamento)
                    VALUES (%s, %s, %s, %s)
                """, (codigo, nome, creditos, depto_codigo))
                conexao.commit()
                janela_add.destroy()
                listar_cursos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar curso:\n{e}")

        tk.Button(janela_add, text="Salvar", command=salvar).grid(row=len(campos), columnspan=2, pady=10)

    def editar_curso():
        """
        Abre uma nova janela para editar um curso selecionado.
        """
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um curso para editar.")
            return

        valores_atuais = tree.item(item, "values")
        codigo_antigo = valores_atuais[0]

        janela_edit = tk.Toplevel()
        janela_edit.title(f"Editar Curso (Código: {codigo_antigo})")

        tk.Label(janela_edit, text="Nome:").grid(row=0, column=0)
        nome_entry = tk.Entry(janela_edit)
        nome_entry.insert(0, valores_atuais[1])
        nome_entry.grid(row=0, column=1)

        tk.Label(janela_edit, text="Créditos Mínimos:").grid(row=1, column=0)
        creditos_entry = tk.Entry(janela_edit)
        creditos_entry.insert(0, valores_atuais[2])
        creditos_entry.grid(row=1, column=1)

        tk.Label(janela_edit, text="Código do Departamento:").grid(row=2, column=0)
        depto_codigo_entry = tk.Entry(janela_edit)
        # Tenta preencher o código do departamento pelo nome atual, ou deixa vazio se não encontrar
        try:
            cursor_depto = conexao.cursor()
            cursor_depto.execute("SELECT codigo FROM DEPARTAMENTO WHERE nome = %s", (valores_atuais[3],))
            codigo_depto_atual = cursor_depto.fetchone()
            if codigo_depto_atual:
                depto_codigo_entry.insert(0, codigo_depto_atual[0])
        except Exception:
            depto_codigo_entry.insert(0, "")  # Caso não encontre ou erro
        depto_codigo_entry.grid(row=2, column=1)

        def salvar_edicao():
            """
            Salva as alterações do curso no banco de dados.
            """
            try:
                novo_nome = nome_entry.get()
                novos_creditos = int(creditos_entry.get())
                novo_depto_codigo = int(depto_codigo_entry.get())

                cursor = conexao.cursor()
                cursor.execute("""
                    UPDATE CURSO SET 
                    nome = %s, 
                    quantidade_minima_creditos = %s, 
                    codigo_departamento = %s 
                    WHERE codigo = %s
                """, (novo_nome, novos_creditos, novo_depto_codigo, codigo_antigo))
                conexao.commit()
                janela_edit.destroy()
                listar_cursos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao editar curso:\n{e}")

        tk.Button(janela_edit, text="Salvar Alterações", command=salvar_edicao).grid(row=3, columnspan=2, pady=10)

    def excluir_curso():
        """
        Exclui um curso selecionado do banco de dados.
        """
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um curso para excluir.")
            return
        confirmar = messagebox.askyesno("Confirmar", "Deseja excluir este curso?")
        if confirmar:
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM CURSO WHERE codigo = %s", (item,))
                conexao.commit()
                listar_cursos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir curso:\n{e}")

    # ----- Interface da Janela -----
    janela = tk.Toplevel()
    janela.title("CRUD - Cursos")
    janela.geometry("700x400")

    tree = ttk.Treeview(janela, columns=("codigo", "nome", "creditos", "departamento"), show="headings")
    for col in ("codigo", "nome", "creditos", "departamento"):
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=150)

    tree.pack(fill="both", expand=True, pady=10)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=5)

    tk.Button(frame_botoes, text="Adicionar", width=15, command=adicionar_curso).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Editar", width=15, command=editar_curso).pack(side="left", padx=5)  # Botão de Editar
    tk.Button(frame_botoes, text="Excluir", width=15, command=excluir_curso).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)

    listar_cursos()