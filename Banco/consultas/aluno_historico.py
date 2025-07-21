
import tkinter as tk
from tkinter import messagebox, ttk

def abrir_historico_aluno(conexao, matricula_aluno):
    janela = tk.Toplevel()
    janela.title("Histórico Escolar")
    janela.geometry("600x400")

    tree = ttk.Treeview(janela, columns=("disciplina", "nota", "frequencia"), show="headings")
    tree.heading("disciplina", text="Disciplina")
    tree.heading("nota", text="Nota Final")
    tree.heading("frequencia", text="Frequência (%)")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    try:
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT D.nome, AD.media_final, AD.frequencia
            FROM ALUNO_DISCIPLINA AD
            JOIN DISCIPLINA D ON AD.codigo_disciplina = D.codigo
            WHERE AD.matricula_aluno = %s AND AD.media_final >= 7.0
        """, (matricula_aluno,))

        for nome_disciplina, nota, frequencia in cursor.fetchall():
            tree.insert("", "end", values=(nome_disciplina, nota, frequencia))

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar seu histórico:\n{e}")