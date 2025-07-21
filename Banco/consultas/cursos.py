# Realiza consultas sobre os dados de um curso.

import tkinter as tk
from tkinter import messagebox

def abrir_consulta_curso(conexao):
    """
    Cria a interface para consultar os dados de um curso.
    
    :param conexao: O objeto de conexão com o banco de dados.
    """
    def consultar():
        """
        Executa as consultas no banco de dados com base no código do curso.
        """
        curso_id = entry_id.get()
        if not curso_id:
            messagebox.showwarning("Atenção", "Informe o ID do curso.")
            return

        try:
            cursor = conexao.cursor()

            # 3.1 Disciplinas obrigatórias

            cursor.execute("SELECT D.NOME FROM DISCIPLINA D WHERE D.TIPO = 'obrigatoria' AND D.CODIGO_CURSO = %s", (curso_id,))
            obrigatorias = [r[0] for r in cursor.fetchall()] or ["Nenhuma"]

            # 3.2 Disciplinas optativas

            cursor.execute("SELECT D.NOME FROM DISCIPLINA D WHERE D.TIPO = 'optativa' AND D.CODIGO_CURSO = %s", (curso_id,))
            optativas = [r[0] for r in cursor.fetchall()] or ["Nenhuma"]

            # 3.3 Alunos do curso

            cursor.execute("SELECT A.NOME FROM ALUNO A WHERE A.CODIGO_CURSO = %s", (curso_id,))
            alunos = [r[0] for r in cursor.fetchall()] or ["Nenhum"]

            # 3.4 Alunos que fizeram todas as obrigatórias

            cursor.execute("""
                SELECT
                    A.NOME AS NOME_ALUNO
                FROM
                    ALUNO AS A
                JOIN
                    CURSO AS C ON A.CODIGO_CURSO = C.CODIGO
                WHERE
                    C.CODIGO = %s
                    AND (
                        SELECT COUNT(DISTINCT D.codigo)
                        FROM DISCIPLINA AS D
                        WHERE D.CODIGO_CURSO = C.CODIGO AND D.TIPO = 'obrigatoria'
                    ) = (
                        SELECT COUNT(DISTINCT AD.CODIGO_DISCIPLINA) 
                        FROM ALUNO_DISCIPLINA AS AD
                        JOIN DISCIPLINA AS D2 ON AD.CODIGO_DISCIPLINA = D2.CODIGO
                        WHERE AD.MATRICULA_ALUNO = A.MATRICULA
                        AND D2.CODIGO_CURSO = C.CODIGO
                        AND D2.TIPO = 'obrigatoria'
                        AND AD.MEDIA_FINAL >= 7.0
                    );
            """, (curso_id,))
            completos = [r[0] for r in cursor.fetchall()] or ["Nenhum"]

            # 3.5 Alunos que não fizeram nenhuma optativa

            cursor.execute("""
                SELECT
                    A.NOME AS NOME_ALUNO
                FROM
                    ALUNO AS A
                JOIN
                    CURSO AS C ON A.CODIGO_CURSO = C.CODIGO
                WHERE
                    C.CODIGO = %s
                    AND A.MATRICULA NOT IN (
                        SELECT AD.MATRICULA_ALUNO
                        FROM ALUNO_DISCIPLINA AS AD
                        JOIN DISCIPLINA AS D ON AD.CODIGO_DISCIPLINA = D.CODIGO
                        WHERE D.CODIGO_CURSO = C.CODIGO AND D.TIPO = 'optativa'
                    );
            """, (curso_id,))
            nenhum_optativa = [r[0] for r in cursor.fetchall()] or ["Nenhum"]

            # Exibe os resultados na caixa de texto
            txt_resultado.config(state="normal")
            txt_resultado.delete("1.0", tk.END)
            txt_resultado.insert(tk.END, f"📘 Disciplinas Obrigatórias:\n" + "\n".join(obrigatorias) + "\n\n")
            txt_resultado.insert(tk.END, f"📗 Disciplinas Optativas:\n" + "\n".join(optativas) + "\n\n")
            txt_resultado.insert(tk.END, f"📙 Alunos Matriculados:\n" + "\n".join(alunos) + "\n\n")
            txt_resultado.insert(tk.END, f"📕 Alunos que concluíram TODAS obrigatórias:\n" + "\n".join(completos) + "\n\n")
            txt_resultado.insert(tk.END, f"📕 Alunos que NÃO fizeram nenhuma optativa:\n" + "\n".join(nenhum_optativa))
            txt_resultado.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ----- Interface da Janela -----
    janela = tk.Toplevel()
    janela.title("Consulta - Curso")
    janela.geometry("700x500")

    tk.Label(janela, text="ID do Curso:").pack(pady=5)
    entry_id = tk.Entry(janela)
    entry_id.pack()

    tk.Button(janela, text="Consultar", command=consultar).pack(pady=10)

    txt_resultado = tk.Text(janela, wrap="word", height=25, state="disabled")
    txt_resultado.pack(padx=10, pady=10, fill="both", expand=True)