# Realiza consultas sobre os dados de uma disciplina.

import tkinter as tk
from tkinter import messagebox

def abrir_lista_disciplinas_professor(conexao, siape_professor):
    """
    Função que executa a consulta e exibe as disciplinas ministradas pelo professor.
    """
    janela_disciplinas = tk.Toplevel()
    janela_disciplinas.title("Minhas Disciplinas")
    janela_disciplinas.geometry("400x300")
    
    try:
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT D.nome FROM DISCIPLINA D
            JOIN MINISTRA_DISCIPLINA MD ON D.codigo = MD.codigo_disciplina
            WHERE MD.siape_professor = %s
        """, (siape_professor,))
        
        disciplinas = cursor.fetchall()
        
        if disciplinas:
            lista_text = "Disciplinas que você ministra:\n\n"
            for disc in disciplinas:
                lista_text += f"- {disc[0]}\n"
        else:
            lista_text = "Você não ministra nenhuma disciplina."
            
        tk.Label(janela_disciplinas, text=lista_text, justify=tk.LEFT).pack(padx=20, pady=20)
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar disciplinas: {e}")

def abrir_consulta_disciplina(conexao):
    """
    Cria a interface para consultar os dados de uma disciplina.
    
    :param conexao: O objeto de conexão com o banco de dados.
    """
    def consultar():
        """
        Executa as consultas no banco de dados com base no código da disciplina.
        """
        disc_id = entry_id.get()
        if not disc_id:
            messagebox.showwarning("Atenção", "Informe o ID da disciplina.")
            return

        try:
            cursor = conexao.cursor()

            # 4.1 Alunos matriculados na disciplina
            cursor.execute("""
                SELECT A.nome FROM ALUNO_DISCIPLINA AD
                JOIN ALUNO A ON AD.matricula_aluno = A.matricula
                WHERE AD.codigo_disciplina = %s
            """, (disc_id,))
            alunos = [r[0] for r in cursor.fetchall()] or ["Nenhum"]

            # 4.2 Pré-requisitos da disciplina
            cursor.execute("""
                SELECT D2.nome FROM PRE_REQUISITO_DISCIPLINA PR
                JOIN DISCIPLINA D2 ON D2.codigo = PR.codigo_pre_requisito
                WHERE PR.codigo_disciplina = %s
            """, (disc_id,))
            prereqs = [r[0] for r in cursor.fetchall()] or ["Nenhum"]

            # 4.3 Disciplinas para as quais a mesma é pré-requisito
            cursor.execute("""
                SELECT D.nome FROM PRE_REQUISITO_DISCIPLINA PR
                JOIN DISCIPLINA D ON D.codigo = PR.codigo_disciplina
                WHERE PR.codigo_pre_requisito = %s
            """, (disc_id,))
            dependentes = [r[0] for r in cursor.fetchall()] or ["Nenhuma"]

            # Exibe os resultados na caixa de texto
            txt_resultado.config(state="normal")
            txt_resultado.delete("1.0", tk.END)
            txt_resultado.insert(tk.END, f"📘 Alunos Matriculados:\n" + "\n".join(alunos) + "\n\n")
            txt_resultado.insert(tk.END, f"📗 Pré-requisitos desta disciplina:\n" + "\n".join(prereqs) + "\n\n")
            txt_resultado.insert(tk.END, f"📙 Disciplinas que dependem desta:\n" + "\n".join(dependentes))
            txt_resultado.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ----- Interface da Janela -----
    janela = tk.Toplevel()
    janela.title("Consulta - Disciplina")
    janela.geometry("650x500")

    tk.Label(janela, text="ID da Disciplina:").pack(pady=5)
    entry_id = tk.Entry(janela)
    entry_id.pack()

    tk.Button(janela, text="Consultar", command=consultar).pack(pady=10)

    txt_resultado = tk.Text(janela, wrap="word", height=25, state="disabled")
    txt_resultado.pack(padx=10, pady=10, fill="both", expand=True)