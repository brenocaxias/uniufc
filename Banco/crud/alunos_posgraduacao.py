
# Gerencia as operações de CRUD para a subclasse ALUNO_POS_GRADUACAO.

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


def abrir_crud_alunos_posgraduacao(conexao):
    """
    Cria a janela de gerenciamento para alunos de pós-graduação.

    :param conexao: Objeto de conexão com o banco de dados.
    """

    def listar_alunos():
        """
        Lista todos os alunos de pós-graduação, incluindo o nome do orientador.
        """
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conexao.cursor()
            # Consulta SQL para unir as tabelas ALUNO, ALUNO_POS_GRADUACAO, PROFESSOR e CURSO
            # Seleciona também os códigos do curso e do SIAPE do orientador para facilitar a edição
            cursor.execute("""
                SELECT A.matricula, A.nome, A.endereco, C.nome, P.nome_completo,
                       A.codigo_curso, AP.formacao_basica, AP.siape_orientador
                FROM ALUNO A
                JOIN ALUNO_POS_GRADUACAO AP ON A.matricula = AP.matricula_aluno
                JOIN PROFESSOR P ON AP.siape_orientador = P.siape
                JOIN CURSO C ON A.codigo_curso = C.codigo
                WHERE A.tipo_aluno = 'pos_graduacao'
            """)
            # Insere no Treeview apenas os campos que serão visíveis,
            # mas armazena os códigos para edição
            for matricula, nome, endereco, curso_nome, orientador_nome, \
                    codigo_curso, formacao_basica, siape_orientador in cursor.fetchall():
                tree.insert("", "end", iid=matricula,
                            values=(matricula, nome, endereco, curso_nome, orientador_nome),
                            tags=(codigo_curso, formacao_basica, siape_orientador))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar alunos:\n{e}")

    def adicionar_aluno():
        """
        Adiciona um novo aluno de pós-graduação.
        Insere primeiro na tabela pai (ALUNO) e depois na tabela filha (ALUNO_POS_GRADUACAO).
        """
        matricula = simpledialog.askstring("Matrícula", "Digite a matrícula:")
        nome = simpledialog.askstring("Nome", "Digite o nome do aluno:")
        endereco = simpledialog.askstring("Endereço", "Digite o endereço:")
        codigo_curso = simpledialog.askstring("Código do Curso", "Digite o código do curso:")
        siape_orientador = simpledialog.askstring("SIAPE do Orientador", "Digite o SIAPE do professor orientador:")
        formacao_basica = simpledialog.askstring("Formação Básica",
                                                 "Digite a formação básica (ex: Ciência da Computação):")

        if matricula and nome and codigo_curso and siape_orientador:
            try:
                cursor = conexao.cursor()
                # Insere o registro na tabela ALUNO
                cursor.execute("""
                    INSERT INTO ALUNO (matricula, nome, endereco, tipo_aluno, codigo_curso)
                    VALUES (%s, %s, %s, 'pos_graduacao', %s)
                """, (matricula, nome, endereco, codigo_curso))
                # Insere o registro na tabela ALUNO_POS_GRADUACAO
                cursor.execute(
                    "INSERT INTO ALUNO_POS_GRADUACAO (matricula_aluno, formacao_basica, siape_orientador) VALUES (%s, %s, %s)",
                    (matricula, formacao_basica, siape_orientador))
                conexao.commit()
                listar_alunos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar aluno de pós:\n{e}")

    def editar_aluno():
        """
        Abre uma nova janela para editar um aluno de pós-graduação selecionado.
        Permite a alteração de nome, endereço, curso, formação básica e orientador.
        """
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um aluno para editar.")
            return

        valores_atuais = tree.item(item, "values")
        tags_atuais = tree.item(item, "tags")  # Recupera as tags onde armazenamos os códigos extras

        matricula_aluno = valores_atuais[0]
        codigo_curso_atual = tags_atuais[0] if tags_atuais else ''
        formacao_basica_atual = tags_atuais[1] if len(tags_atuais) > 1 else ''
        siape_orientador_atual = tags_atuais[2] if len(tags_atuais) > 2 else ''

        janela_edit = tk.Toplevel()
        janela_edit.title(f"Editar Aluno Pós-Graduação (Matrícula: {matricula_aluno})")

        tk.Label(janela_edit, text="Nome:").grid(row=0, column=0, sticky="w")
        nome_entry = tk.Entry(janela_edit)
        nome_entry.insert(0, valores_atuais[1])
        nome_entry.grid(row=0, column=1, pady=2)

        tk.Label(janela_edit, text="Endereço:").grid(row=1, column=0, sticky="w")
        endereco_entry = tk.Entry(janela_edit)
        endereco_entry.insert(0, valores_atuais[2])
        endereco_entry.grid(row=1, column=1, pady=2)

        tk.Label(janela_edit, text="Código do Curso:").grid(row=2, column=0, sticky="w")
        codigo_curso_entry = tk.Entry(janela_edit)
        codigo_curso_entry.insert(0, codigo_curso_atual)
        codigo_curso_entry.grid(row=2, column=1, pady=2)

        tk.Label(janela_edit, text="Formação Básica:").grid(row=3, column=0, sticky="w")
        formacao_basica_entry = tk.Entry(janela_edit)
        formacao_basica_entry.insert(0, formacao_basica_atual)
        formacao_basica_entry.grid(row=3, column=1, pady=2)

        tk.Label(janela_edit, text="SIAPE do Orientador:").grid(row=4, column=0, sticky="w")
        siape_orientador_entry = tk.Entry(janela_edit)
        siape_orientador_entry.insert(0, siape_orientador_atual)
        siape_orientador_entry.grid(row=4, column=1, pady=2)

        def salvar_edicao():
            """
            Salva as alterações do aluno de pós-graduação no banco de dados.
            Atualiza as tabelas ALUNO e ALUNO_POS_GRADUACAO.
            """
            try:
                novo_nome = nome_entry.get()
                novo_endereco = endereco_entry.get()
                novo_codigo_curso = codigo_curso_entry.get()
                nova_formacao_basica = formacao_basica_entry.get()
                novo_siape_orientador = siape_orientador_entry.get()

                cursor = conexao.cursor()

                # Atualiza a tabela ALUNO (dados gerais do aluno)
                cursor.execute("""
                    UPDATE ALUNO SET 
                    nome = %s, 
                    endereco = %s, 
                    codigo_curso = %s 
                    WHERE matricula = %s
                """, (novo_nome, novo_endereco, novo_codigo_curso, matricula_aluno))

                # Atualiza a tabela ALUNO_POS_GRADUACAO (dados específicos de pós-graduação)
                cursor.execute("""
                    UPDATE ALUNO_POS_GRADUACAO SET 
                    formacao_basica = %s, 
                    siape_orientador = %s 
                    WHERE matricula_aluno = %s
                """, (nova_formacao_basica, novo_siape_orientador, matricula_aluno))

                conexao.commit()
                janela_edit.destroy()
                listar_alunos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar alterações:\n{e}")

        tk.Button(janela_edit, text="Salvar Alterações", command=salvar_edicao).grid(row=5, columnspan=2, pady=10)

    def ver_formacoes():
        """
        Exibe a formação básica de um aluno de pós-graduação selecionado.
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
        """
        Exclui um aluno de pós-graduação.
        A exclusão da tabela pai (ALUNO) é garantida pelo ON DELETE CASCADE.
        """
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um aluno.")
            return
        if messagebox.askyesno("Confirmar", "Deseja excluir este aluno de pós-graduação?"):
            try:
                cursor = conexao.cursor()
                # A exclusão na tabela ALUNO irá disparar o ON DELETE CASCADE
                # e excluir o registro correspondente em ALUNO_POS_GRADUACAO
                cursor.execute("DELETE FROM ALUNO WHERE matricula = %s", (item,))
                conexao.commit()
                listar_alunos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir aluno:\n{e}")

    # ----- Interface da Janela -----
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
    tk.Button(frame, text="Editar", width=15, command=editar_aluno).pack(side="left", padx=5)  # Botão de Edição
    tk.Button(frame, text="Ver Formação", width=15, command=ver_formacoes).pack(side="left", padx=5)
    tk.Button(frame, text="Excluir", width=15, command=excluir_aluno).pack(side="left", padx=5)
    tk.Button(frame, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)

    listar_alunos()