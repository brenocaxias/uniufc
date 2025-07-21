import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


def abrir_crud_alunos_posgraduacao(conexao):
    """
        Cria a janela de gerenciamento para alunos de pós-graduação.

        :param conexao: Objeto de conexão com o banco de dados.
        """
    def listar_alunos():
        """ Lista todos os alunos de pós-graduação, incluindo o nome do orientador.
                """
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT A.matricula, A.nome, A.endereco, C.nome, P.nome_completo
                FROM ALUNO A
                JOIN ALUNO_POS_GRADUACAO AP ON A.matricula = AP.matricula_aluno
                JOIN PROFESSOR P ON AP.siape_orientador = P.siape
                JOIN CURSO C ON A.codigo_curso = C.codigo
                WHERE A.tipo_aluno = 'pos_graduacao'
            """)
            for matricula, nome, endereco, curso, orientador in cursor.fetchall():
                tree.insert("", "end", iid=matricula, values=(matricula, nome, endereco, curso, orientador))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar alunos:\n{e}")

    def adicionar_aluno():
        """     Adiciona um novo aluno de pós-graduação.
                Insere primeiro na tabela pai (ALUNO) e depois na tabela filha (ALUNO_POS_GRADUACAO).
                """
        matricula = simpledialog.askstring("Matrícula", "Digite a matrícula:")
        nome = simpledialog.askstring("Nome", "Digite o nome do aluno:")
        endereco = simpledialog.askstring("Endereço", "Digite o endereço:")
        codigo_curso = simpledialog.askstring("Código do Curso", "Digite o código do curso:")
        siape_orientador = simpledialog.askstring("SIAPE do Orientador", "Digite o SIAPE do professor orientador:")
        formacao_basica = simpledialog.askstring("Formação Básica", "Digite a formação básica (ex: Ciência da Computação):")

        if matricula and nome and codigo_curso and siape_orientador:
            try:
                cursor = conexao.cursor()
                cursor.execute("""
                    INSERT INTO ALUNO (matricula, nome, endereco, tipo_aluno, codigo_curso)
                    VALUES (%s, %s, %s, 'pos_graduacao', %s)
                """, (matricula, nome, endereco, codigo_curso))
                cursor.execute(
                    "INSERT INTO ALUNO_POS_GRADUACAO (matricula_aluno, formacao_basica, siape_orientador) VALUES (%s, %s, %s)",
                    (matricula, formacao_basica, siape_orientador))
                conexao.commit()
                listar_alunos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar aluno de pós:\n{e}")

    def ver_formacoes():
        """ Exibe a formação básica de um aluno de pós-graduação selecionado.
                """
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um aluno.")
            return
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT formacao_basica FROM ALUNO_POS_GRADUACAO WHERE matricula_aluno = %s", (item,))
            formacao = cursor.fetchone()
            formacao_str = formacao[0] if formacao and formacao[0] else "Nenhuma formação registrada."
            messagebox.showinfo("Formação Acadêmica", formacao_str)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar formação:\n{e}")

    def excluir_aluno():
        #exclui aluno de pós gradaucao
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um aluno.")
            return
        if messagebox.askyesno("Confirmar", "Deseja excluir este aluno de pós-graduação?"):
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM ALUNO_POS_GRADUACAO WHERE matricula_aluno = %s", (item,))
                cursor.execute("DELETE FROM ALUNO WHERE matricula = %s", (item,))
                conexao.commit()
                listar_alunos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir aluno:\n{e}")

    janela = tk.Toplevel()
    janela.title("CRUD - Alunos de Pós-Graduação")
    janela.geometry("850x400")

    tree = ttk.Treeview(janela, columns=("matricula", "nome", "endereco", "curso", "orientador"), show="headings")
    for col in ("matricula", "nome", "endereco", "curso", "orientador"):
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=150)
    tree.pack(fill="both", expand=True, pady=10)

    frame = tk.Frame(janela)
    frame.pack(pady=5)
    tk.Button(frame, text="Adicionar", width=15, command=adicionar_aluno).pack(side="left", padx=5)
    tk.Button(frame, text="Ver Formação", width=15, command=ver_formacoes).pack(side="left", padx=5)
    tk.Button(frame, text="Excluir", width=15, command=excluir_aluno).pack(side="left", padx=5)
    tk.Button(frame, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)

    listar_alunos()