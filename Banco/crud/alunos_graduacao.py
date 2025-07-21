import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def abrir_crud_alunos_graduacao(conexao):
    """
        Cria a janela de gerenciamento para alunos de graduação.

        :param conexao: Objeto de conexão com o banco de dados.
        """
    def listar_alunos():
        """
            Lista todos os alunos de graduação, incluindo o ano de ingresso e o nome do curso.
             """
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT A.matricula, A.nome, A.endereco, C.nome, AG.ano_ingresso
                FROM ALUNO A
                JOIN ALUNO_GRADUACAO AG ON A.matricula = AG.matricula_aluno
                JOIN CURSO C ON A.codigo_curso = C.codigo
                WHERE A.tipo_aluno = 'graduacao'
            """)
            for matricula, nome, endereco, curso, ano in cursor.fetchall():
                tree.insert("", "end", iid=matricula, values=(matricula, nome, endereco, curso, ano))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar alunos:\n{e}")

    def adicionar_aluno():
        """"    Adiciona um novo aluno de graduação.
                Insere primeiro na tabela pai (ALUNO) e depois na tabela filha (ALUNO_GRADUACAO).
        """
        matricula = simpledialog.askstring("Matrícula", "Digite a matrícula:")
        nome = simpledialog.askstring("Nome", "Digite o nome do aluno:")
        endereco = simpledialog.askstring("Endereço", "Digite o endereço:")
        codigo_curso = simpledialog.askstring("Código do Curso", "Digite o código do curso:")
        ano = simpledialog.askinteger("Ano de Ingresso", "Digite o ano de ingresso:")
        if matricula and nome and codigo_curso and ano:
            try:
                cursor = conexao.cursor()
                cursor.execute("""
                    INSERT INTO ALUNO (matricula, nome, endereco, tipo_aluno, codigo_curso)
                    VALUES (%s, %s, %s, 'graduacao', %s)
                """, (matricula, nome, endereco, codigo_curso))
                cursor.execute("INSERT INTO ALUNO_GRADUACAO (matricula_aluno, ano_ingresso) VALUES (%s, %s)", (matricula, ano))
                conexao.commit()
                listar_alunos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar aluno:\n{e}")

    def editar_ano():
        """ Edita o ano de ingresso de um aluno de graduação selecionado.
               """
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um aluno.")
            return
        novo_ano = simpledialog.askinteger("Editar Ano", "Digite o novo ano de ingresso:")
        if novo_ano:
            try:
                cursor = conexao.cursor()
                cursor.execute("UPDATE ALUNO_GRADUACAO SET ano_ingresso = %s WHERE matricula_aluno = %s", (novo_ano, item))
                conexao.commit()
                listar_alunos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao editar ano:\n{e}")

    def excluir_aluno():
        """ Exclui um aluno de graduação.
            A exclusão da tabela pai (ALUNO) é garantida pelo ON DELETE CASCADE.
               """
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um aluno.")
            return
        if messagebox.askyesno("Confirmar", "Deseja excluir este aluno?"):
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM ALUNO_GRADUACAO WHERE matricula_aluno = %s", (item,))
                cursor.execute("DELETE FROM ALUNO WHERE matricula = %s", (item,))
                conexao.commit()
                listar_alunos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir aluno:\n{e}")

    janela = tk.Toplevel()
    janela.title("CRUD - Alunos de Graduação")
    janela.geometry("800x400")

    tree = ttk.Treeview(janela, columns=("matricula", "nome", "endereco", "curso", "ano"), show="headings")
    for col in ("matricula", "nome", "endereco", "curso", "ano"):
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=150)
    tree.pack(fill="both", expand=True, pady=10)

    frame = tk.Frame(janela)
    frame.pack(pady=5)
    tk.Button(frame, text="Adicionar", width=15, command=adicionar_aluno).pack(side="left", padx=5)
    tk.Button(frame, text="Editar Ano", width=15, command=editar_ano).pack(side="left", padx=5)
    tk.Button(frame, text="Excluir", width=15, command=excluir_aluno).pack(side="left", padx=5)
    tk.Button(frame, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)

    listar_alunos()