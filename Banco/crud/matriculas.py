import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def abrir_matriculas(conexao):
    ## Função para listar as matrículas de um aluno específico
    def listar_matriculas():
        for row in tree.get_children():
            tree.delete(row)
        matricula_aluno = entry_aluno_id.get()
        # Verifica se o campo da matrícula do aluno não está vazio.
        if not matricula_aluno:
            # Exibe um aviso se a matrícula não for fornecida.
            messagebox.showwarning("Atenção", "Digite a matrícula do aluno.")
            return
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT D.nome, M.media_final, M.frequencia
                FROM ALUNO_DISCIPLINA M
                JOIN DISCIPLINA D ON M.codigo_disciplina = D.codigo
                WHERE M.matricula_aluno = %s
            """, (matricula_aluno,))
            # Itera sobre todas as linhas de resultado da consulta.
            for nome, nota, freq in cursor.fetchall():
                tree.insert("", "end", values=(nome, nota, f"{freq}%"))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar matrículas:\n{e}")

    # Função para adicionar uma nova matrícula
    def adicionar_matricula():
        # Obtém a matrícula do aluno do campo de entrada.
        matricula_aluno = entry_aluno_id.get()
        # Verifica se o usuário não cancelou nenhum dos diálogos (retorna None)
        if not matricula_aluno:
            messagebox.showwarning("Atenção", "Digite a matrícula do aluno.")
            return
        codigo_disciplina = simpledialog.askstring("Código da Disciplina", "Digite o código da disciplina:")
        nota = simpledialog.askfloat("Nota Final", "Digite a nota (ex: 8.5):")
        freq = simpledialog.askfloat("Frequência (%)", "Digite a frequência (ex: 90):")
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO ALUNO_DISCIPLINA (matricula_aluno, codigo_disciplina, media_final, frequencia)
                VALUES (%s, %s, %s, %s)
            """, (matricula_aluno, codigo_disciplina, nota, freq))
            conexao.commit()
            listar_matriculas()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar matrícula:\n{e}")

    # Função para editar uma matrícula existente.
    def editar_matricula():
        matricula_aluno = entry_aluno_id.get()
        if not matricula_aluno:
            messagebox.showwarning("Atenção", "Digite a matrícula do aluno.")
            return
        codigo_disciplina = simpledialog.askstring("Código da Disciplina", "Digite o código da disciplina a editar:")
        nova_nota = simpledialog.askfloat("Nova Nota", "Digite a nova nota:")
        nova_freq = simpledialog.askfloat("Nova Frequência", "Digite a nova frequência:")
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                UPDATE ALUNO_DISCIPLINA
                SET media_final = %s, frequencia = %s
                WHERE matricula_aluno = %s AND codigo_disciplina = %s
            """, (nova_nota, nova_freq, matricula_aluno, codigo_disciplina))
            conexao.commit()
            listar_matriculas()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao editar matrícula:\n{e}")

    # Função para excluir uma matrícula.
    def excluir_matricula():
        matricula_aluno = entry_aluno_id.get()
        if not matricula_aluno:
            messagebox.showwarning("Atenção", "Digite a matrícula do aluno.")
            return
        codigo_disciplina = simpledialog.askstring("Código da Disciplina", "Digite o código da disciplina a remover:")
        confirmar = messagebox.askyesno("Confirmar", "Deseja excluir esta matrícula?")
        if confirmar:
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM ALUNO_DISCIPLINA WHERE matricula_aluno = %s AND codigo_disciplina = %s", (matricula_aluno, codigo_disciplina))
                conexao.commit()
                listar_matriculas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir matrícula:\n{e}")

    janela = tk.Toplevel()
    janela.title("Matrículas de Aluno em Disciplinas")
    janela.geometry("700x400")

    tk.Label(janela, text="Matrícula do Aluno:").pack(pady=(10, 0))
    entry_aluno_id = tk.Entry(janela)
    entry_aluno_id.pack()

    tk.Button(janela, text="Listar Matrículas", command=listar_matriculas).pack(pady=5)

    tree = ttk.Treeview(janela, columns=("disciplina", "nota", "frequencia"), show="headings")
    tree.heading("disciplina", text="Disciplina")
    tree.heading("nota", text="Nota Final")
    tree.heading("frequencia", text="Frequência")
    tree.pack(fill="both", expand=True, pady=10)

    frame = tk.Frame(janela)
    frame.pack(pady=5)
    tk.Button(frame, text="Adicionar", width=15, command=adicionar_matricula).pack(side="left", padx=5)
    tk.Button(frame, text="Editar", width=15, command=editar_matricula).pack(side="left", padx=5)
    tk.Button(frame, text="Excluir", width=15, command=excluir_matricula).pack(side="left", padx=5)
    tk.Button(frame, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)