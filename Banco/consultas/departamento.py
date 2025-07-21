# Realiza consultas sobre os dados de um departamento.

import tkinter as tk
from tkinter import messagebox

def abrir_consulta_departamento(conexao):
    """
    Cria a interface para consultar os dados de um departamento.
    
    :param conexao: O objeto de conexão com o banco de dados.
    """
    def consultar():
        """
        Executa as consultas no banco de dados com base no código do departamento.
        """
        depto_id = entry_id.get()
        if not depto_id:
            messagebox.showwarning("Atenção", "Informe o ID do departamento.")
            return

        try:
            cursor = conexao.cursor(dictionary=True)

            # 2.1 Cursos do departamento

            cursor.execute("""
                SELECT
                    C.NOME AS NOME_CURSO
                FROM
                    DEPARTAMENTO AS D
                JOIN
                    CURSO AS C ON D.CODIGO = C.CODIGO_DEPARTAMENTO
                WHERE
                    D.CODIGO = %s;
            """, (depto_id,))
            cursos = [c['NOME_CURSO'] for c in cursor.fetchall()] or ["Nenhum"]

            # 2.2 Detalhes do departamento

            cursor.execute("""
                SELECT
                    CODIGO AS CODIGO_DEPARTAMENTO,
                    NOME AS NOME_DEPARTAMENTO
                FROM
                    DEPARTAMENTO
                WHERE
                    CODIGO = %s;
            """, (depto_id,))
            depto = cursor.fetchone()
            detalhes = f"Código: {depto['CODIGO_DEPARTAMENTO']}\nNome: {depto['NOME_DEPARTAMENTO']}" if depto else "Não encontrado."

            # Exibe os resultados na caixa de texto
            txt_resultado.config(state="normal")
            txt_resultado.delete("1.0", tk.END)
            txt_resultado.insert(tk.END, f"📘 Detalhes do Departamento:\n{detalhes}\n\n")
            txt_resultado.insert(tk.END, f"📗 Cursos Associados:\n" + "\n".join(cursos))
            txt_resultado.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ----- Interface da Janela -----
    janela = tk.Toplevel()
    janela.title("Consulta - Departamento")
    janela.geometry("600x400")

    tk.Label(janela, text="ID do Departamento:").pack(pady=5)
    entry_id = tk.Entry(janela)
    entry_id.pack()

    tk.Button(janela, text="Consultar", command=consultar).pack(pady=10)

    txt_resultado = tk.Text(janela, wrap="word", height=20, state="disabled")
    txt_resultado.pack(padx=10, pady=10, fill="both", expand=True)