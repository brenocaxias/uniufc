# Gerencia as operações de CRUD para a entidade PROFESSOR.

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry


def abrir_crud_professores(conexao):
    """
    Cria a janela do CRUD de professores.

    :param conexao: Objeto de conexão com o banco de dados.
    """

    def listar_professores():
        """
        Lista todos os professores, exibindo o nome do departamento associado.
        """
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conexao.cursor()
            # Consulta para unir PROFESSOR com DEPARTAMENTO
            cursor.execute("""
                SELECT P.siape, P.nome_completo, P.data_nascimento, P.data_ingresso, D.nome 
                FROM PROFESSOR P
                LEFT JOIN DEPARTAMENTO D ON P.codigo_departamento = D.codigo
            """)
            for siape, nome, nascimento, ingresso, depto in cursor.fetchall():
                tree.insert("", "end", iid=siape, values=(siape, nome, nascimento, ingresso, depto or ""))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar professores:\n{e}")

    def adicionar_professor():
        """
        Abre uma nova janela para adicionar um professor.
        """
        janela_add = tk.Toplevel()
        janela_add.title("Novo Professor")

        tk.Label(janela_add, text="SIAPE:").grid(row=0, column=0)
        siape_entry = tk.Entry(janela_add)
        siape_entry.grid(row=0, column=1)

        tk.Label(janela_add, text="Nome Completo:").grid(row=1, column=0)
        nome_entry = tk.Entry(janela_add)
        nome_entry.grid(row=1, column=1)

        tk.Label(janela_add, text="Data de Nascimento:").grid(row=2, column=0)
        nascimento_entry = DateEntry(janela_add, date_pattern='yyyy-mm-dd')
        nascimento_entry.grid(row=2, column=1)

        tk.Label(janela_add, text="Data de Ingresso:").grid(row=3, column=0)
        ingresso_entry = DateEntry(janela_add, date_pattern='yyyy-mm-dd')
        ingresso_entry.grid(row=3, column=1)

        tk.Label(janela_add, text="Código do Departamento:").grid(row=4, column=0)
        departamento_entry = tk.Entry(janela_add)
        departamento_entry.grid(row=4, column=1)

        def salvar():
            """
            Coleta os dados e insere o novo professor no banco de dados.
            """
            try:
                cursor = conexao.cursor()
                cursor.execute("""
                    INSERT INTO PROFESSOR (siape, nome_completo, data_nascimento, data_ingresso, codigo_departamento)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    siape_entry.get(),
                    nome_entry.get(),
                    nascimento_entry.get_date(),
                    ingresso_entry.get_date(),
                    departamento_entry.get()
                ))
                conexao.commit()
                janela_add.destroy()
                listar_professores()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar professor:\n{e}")

        tk.Button(janela_add, text="Salvar", command=salvar).grid(row=5, columnspan=2, pady=10)

    def editar_professor():
        """
        Abre uma nova janela para editar um professor selecionado.
        Permite a alteração do nome, datas e departamento.
        """
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um professor para editar.")
            return

        valores_atuais = tree.item(item, "values")
        siape_antigo = valores_atuais[0]

        janela_edit = tk.Toplevel()
        janela_edit.title(f"Editar Professor (SIAPE: {siape_antigo})")

        tk.Label(janela_edit, text="Nome Completo:").grid(row=0, column=0)
        nome_entry = tk.Entry(janela_edit)
        nome_entry.insert(0, valores_atuais[1])  # Preenche com valor atual
        nome_entry.grid(row=0, column=1)

        tk.Label(janela_edit, text="Data de Nascimento:").grid(row=1, column=0)
        nascimento_entry = DateEntry(janela_edit, date_pattern='yyyy-mm-dd')
        nascimento_entry.set_date(valores_atuais[2])  # Preenche com valor atual
        nascimento_entry.grid(row=1, column=1)

        tk.Label(janela_edit, text="Data de Ingresso:").grid(row=2, column=0)
        ingresso_entry = DateEntry(janela_edit, date_pattern='yyyy-mm-dd')
        ingresso_entry.set_date(valores_atuais[3])  # Preenche com valor atual
        ingresso_entry.grid(row=2, column=1)

        tk.Label(janela_edit, text="Código do Departamento:").grid(row=3, column=0)
        departamento_entry = tk.Entry(janela_edit)
        # Busca o código do departamento pelo nome para preencher
        try:
            cursor_depto = conexao.cursor()
            cursor_depto.execute("SELECT codigo FROM DEPARTAMENTO WHERE nome = %s", (valores_atuais[4],))
            codigo_depto_atual = cursor_depto.fetchone()
            if codigo_depto_atual:
                departamento_entry.insert(0, codigo_depto_atual[0])
        except Exception:
            departamento_entry.insert(0, "")  # Caso não encontre ou erro

        departamento_entry.grid(row=3, column=1)

        def salvar_edicao():
            """
            Salva as alterações do professor no banco de dados.
            """
            try:
                novo_nome = nome_entry.get()
                nova_data_nascimento = nascimento_entry.get_date()
                nova_data_ingresso = ingresso_entry.get_date()
                novo_codigo_departamento = departamento_entry.get()

                cursor = conexao.cursor()
                cursor.execute("""
                    UPDATE PROFESSOR SET 
                    nome_completo = %s, 
                    data_nascimento = %s, 
                    data_ingresso = %s, 
                    codigo_departamento = %s 
                    WHERE siape = %s
                """, (
                    novo_nome,
                    nova_data_nascimento,
                    nova_data_ingresso,
                    novo_codigo_departamento,
                    siape_antigo
                ))
                conexao.commit()
                janela_edit.destroy()
                listar_professores()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao editar professor:\n{e}")

        tk.Button(janela_edit, text="Salvar Alterações", command=salvar_edicao).grid(row=4, columnspan=2, pady=10)

    def excluir_professor():
        """
        Exclui um professor selecionado.
        """
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um professor para excluir.")
            return
        confirmar = messagebox.askyesno("Confirmar", "Deseja excluir este professor?")
        if confirmar:
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM PROFESSOR WHERE siape = %s", (item,))
                conexao.commit()
                listar_professores()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir professor:\n{e}")

    # ----- Interface da Janela -----
    janela = tk.Toplevel()
    janela.title("CRUD - Professores")
    janela.geometry("700x400")

    tree = ttk.Treeview(janela, columns=("siape", "nome", "nascimento", "ingresso", "departamento"), show="headings")
    tree.heading("siape", text="SIAPE")
    tree.heading("nome", text="Nome")
    tree.heading("nascimento", text="Nascimento")
    tree.heading("ingresso", text="Ingresso")
    tree.heading("departamento", text="Departamento")
    tree.pack(fill="both", expand=True, pady=10)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=5)

    tk.Button(frame_botoes, text="Adicionar", width=15, command=adicionar_professor).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Editar", width=15, command=editar_professor).pack(side="left",
                                                                                    padx=5)  # Botão de Editar
    tk.Button(frame_botoes, text="Excluir", width=15, command=excluir_professor).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)

    listar_professores()