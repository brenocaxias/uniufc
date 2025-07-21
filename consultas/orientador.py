# Realiza consultas sobre os dados de um professor orientador.

import tkinter as tk
from tkinter import messagebox

def abrir_consulta_orientador(conexao):
    """
    Cria a interface para consultar os dados de um professor orientador.
    
    :param conexao: O objeto de conexão com o banco de dados.
    """
    def consultar():
        """
        Executa as consultas no banco de dados com base no SIAPE do professor.
        """
        prof_id = entry_id.get()
        if not prof_id:
            messagebox.showwarning("Atenção", "Informe o ID do professor orientador.")
            return

        try:
            cursor = conexao.cursor(dictionary=True)

            # 5.1 Alunos orientandos (pós-graduação)

            cursor.execute("""
                SELECT
                    A.NOME AS NOME_ALUNO_POS_GRADUACAO
                FROM
                    PROFESSOR AS P
                JOIN
                    ALUNO_POS_GRADUACAO AS APG ON P.SIAPE = APG.SIAPE_ORIENTADOR
                JOIN
                    ALUNO AS A ON APG.MATRICULA_ALUNO = A.MATRICULA
                WHERE
                    P.SIAPE = %s;
            """, (prof_id,))
            orientandos = [r['NOME_ALUNO_POS_GRADUACAO'] for r in cursor.fetchall()] or ["Nenhum"]

            # 5.2 Disciplinas ministradas

            cursor.execute("""
                SELECT
                    D.NOME AS NOME_DISCIPLINA,
                    D.NUMERO_CREDITOS AS CREDITOS
                FROM
                    PROFESSOR AS P
                JOIN
                    MINISTRA_DISCIPLINA AS MD ON P.SIAPE = MD.SIAPE_PROFESSOR
                JOIN
                    DISCIPLINA AS D ON MD.CODIGO_DISCIPLINA = D.CODIGO
                WHERE
                    P.SIAPE = %s;
            """, (prof_id,))
            disciplinas = cursor.fetchall()
            lista_disciplinas = [f"{d['NOME_DISCIPLINA']} ({d['CREDITOS']} créditos)" for d in disciplinas] or ["Nenhuma"]

            # 5.3 Total de créditos

            total_creditos = sum([d['CREDITOS'] for d in disciplinas])

            # Exibe os resultados na caixa de texto
            txt_resultado.config(state="normal")
            txt_resultado.delete("1.0", tk.END)
            txt_resultado.insert(tk.END, f"📘 Alunos Orientandos (Pós):\n" + "\n".join(orientandos) + "\n\n")
            txt_resultado.insert(tk.END, f"📗 Disciplinas Ministradas:\n" + "\n".join(lista_disciplinas) + "\n\n")
            txt_resultado.insert(tk.END, f"📙 Total de Créditos Ministrados: {total_creditos}")
            txt_resultado.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ----- Interface da Janela -----
    janela = tk.Toplevel()
    janela.title("Consulta - Orientador")
    janela.geometry("650x500")

    tk.Label(janela, text="ID do Professor (Orientador):").pack(pady=5)
    entry_id = tk.Entry(janela)
    entry_id.pack()

    tk.Button(janela, text="Consultar", command=consultar).pack(pady=10)

    txt_resultado = tk.Text(janela, wrap="word", height=25, state="disabled")
    txt_resultado.pack(padx=10, pady=10, fill="both", expand=True)