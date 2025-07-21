# Realiza consultas sobre os dados de um aluno.

import tkinter as tk
from tkinter import messagebox, ttk


def abrir_consulta_aluno(conexao, matricula_pre_definida=None):
    """
    Cria a interface para consultar os dados de um aluno.

    :param conexao: O objeto de conexão com o banco de dados.
    :param matricula_pre_definida: Matrícula para preencher automaticamente, opcional.
    """

    def consultar():
        """
        Executa as consultas no banco de dados com base na matrícula do aluno.
        """
        matricula = entry_matricula.get()
        if not matricula:
            messagebox.showwarning("Atenção", "Informe a matrícula do aluno.")
            return

        try:
            cursor = conexao.cursor(dictionary=True)

            # 1.1 Disciplinas matriculadas (atualmente cursando)
            cursor.execute("""
                SELECT
                    D.NOME AS NOME_DISCIPLINA
                FROM
                    ALUNO AS A
                JOIN
                    ALUNO_DISCIPLINA AS AD ON A.MATRICULA = AD.MATRICULA_ALUNO
                JOIN
                    DISCIPLINA AS D ON AD.CODIGO_DISCIPLINA = D.CODIGO
                WHERE
                    A.MATRICULA = %s
            """, (matricula,))
            result1 = cursor.fetchall()
            txt1 = "\n".join([r['NOME_DISCIPLINA'] for r in result1]) or "Nenhuma"

            # 1.2 Disciplinas concluídas (com média final >= 7.0)
            cursor.execute("""
                SELECT
                    D.NOME AS NOME_DISCIPLINA
                FROM
                    ALUNO AS A
                JOIN
                    ALUNO_DISCIPLINA AS AD ON A.MATRICULA = AD.MATRICULA_ALUNO
                JOIN
                    DISCIPLINA AS D ON AD.CODIGO_DISCIPLINA = D.CODIGO
                WHERE
                    A.MATRICULA = %s
                    AND AD.MEDIA_FINAL >= 7.0;
            """, (matricula,))
            result2 = cursor.fetchall()
            txt2 = "\n".join([r['NOME_DISCIPLINA'] for r in result2]) or "Nenhuma"

            # 1.3 Curso do aluno
            cursor.execute("""
                SELECT
                    C.NOME AS NOME_CURSO
                FROM
                    ALUNO AS A
                JOIN
                    CURSO AS C ON A.CODIGO_CURSO = C.CODIGO
                WHERE
                    A.MATRICULA = %s;
            """, (matricula,))
            curso = cursor.fetchone()
            txt3 = curso['NOME_CURSO'] if curso else "Desconhecido"

            # 1.4 Dados pessoais
            cursor.execute("""
                SELECT
                    A.MATRICULA,
                    A.NOME,
                    A.ENDERECO,
                    A.TIPO_ALUNO,
                    C.NOME AS NOME_CURSO
                FROM
                    ALUNO AS A
                JOIN
                    CURSO AS C ON A.CODIGO_CURSO = C.CODIGO
                WHERE
                    A.MATRICULA = %s;
            """, (matricula,))
            dados = cursor.fetchone()
            txt4 = f"Matrícula: {dados['MATRICULA']}\nNome: {dados['NOME']}\nEndereço: {dados['ENDERECO']}\nTipo: {dados['TIPO_ALUNO']}\nCurso: {dados['NOME_CURSO']}" if dados else "Não encontrado"

            # Exibe os resultados na caixa de texto
            txt_resultado.config(state="normal")
            txt_resultado.delete("1.0", tk.END)
            txt_resultado.insert(tk.END, f"📘 Disciplinas Matriculadas:\n{txt1}\n\n")
            txt_resultado.insert(tk.END, f"📗 Disciplinas Concluídas:\n{txt2}\n\n")
            txt_resultado.insert(tk.END, f"📙 Curso do Aluno:\n{txt3}\n\n")
            txt_resultado.insert(tk.END, f"📕 Dados Pessoais:\n{txt4}")
            txt_resultado.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao consultar:\n{e}")

    # ----- Interface da Janela -----
    janela = tk.Toplevel()
    janela.title("Consulta - Aluno")
    janela.geometry("600x500")

    tk.Label(janela, text="Matrícula do Aluno:").pack(pady=5)
    entry_matricula = tk.Entry(janela, width=30)
    entry_matricula.pack()

    # Preenche o campo se uma matrícula foi fornecida
    if matricula_pre_definida:
        entry_matricula.insert(0, matricula_pre_definida)
        entry_matricula.config(state='readonly')  # Opcional, para impedir a edição

    tk.Button(janela, text="Consultar", command=consultar).pack(pady=10)

    txt_resultado = tk.Text(janela, wrap="word", height=25, state="disabled")
    txt_resultado.pack(padx=10, pady=10, fill="both", expand=True)