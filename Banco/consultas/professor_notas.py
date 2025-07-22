import tkinter as tk
from tkinter import messagebox, ttk


def abrir_notas_professor(conexao, siape_professor):
    janela = tk.Toplevel()
    janela.title("Notas e Frequências dos Alunos")
    janela.geometry("800x600")

    # Define a função que lista os alunos.
    def listar_alunos_por_disciplina(disciplina_id):
        # Limpar a tabela antes de carregar novos dados
        for row in tree.get_children():
            tree.delete(row)

        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT
                    A.nome, AD.media_final, AD.frequencia
                FROM
                    ALUNO_DISCIPLINA AD
                JOIN
                    ALUNO A ON AD.matricula_aluno = A.matricula
                WHERE
                    AD.codigo_disciplina = %s
            """, (disciplina_id,))

            for nome_aluno, nota, frequencia in cursor.fetchall():
                tree.insert("", "end", values=(nome_aluno, nota, frequencia))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar dados dos alunos:\n{e}")

    try:
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT D.codigo, D.nome FROM DISCIPLINA D
            JOIN MINISTRA_DISCIPLINA MD ON D.codigo = MD.codigo_disciplina
            WHERE MD.siape_professor = %s
        """, (siape_professor,))
        disciplinas = cursor.fetchall()

        if disciplinas:
            disciplina_map = {f"{d[1]} ({d[0]})": d[0] for d in disciplinas}
            combo_disciplinas = ttk.Combobox(janela, state="readonly")
            combo_disciplinas['values'] = list(disciplina_map.keys())
            combo_disciplinas.set(list(disciplina_map.keys())[0])  # Seleciona a primeira disciplina por padrão
            combo_disciplinas.bind("<<ComboboxSelected>>",
                                   lambda event: listar_alunos_por_disciplina(disciplina_map[combo_disciplinas.get()]))
            combo_disciplinas.pack(pady=10)
        else:
            tk.Label(janela, text="Você não ministra nenhuma disciplina.", font=("Arial", 12)).pack(pady=20)
            return  # Retorna para não criar a Treeview se não houver disciplinas

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar lista de disciplinas: {e}")
        return  # Retorna em caso de erro


    tree = ttk.Treeview(janela, columns=("nome", "nota", "frequencia"), show="headings")
    tree.heading("nome", text="Nome do Aluno")
    tree.heading("nota", text="Nota Final")
    tree.heading("frequencia", text="Frequência (%)")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Chama a função de listagem para a disciplina inicial
    if 'disciplina_map' in locals():
        primeira_disciplina_id = list(disciplina_map.values())[0]
        listar_alunos_por_disciplina(primeira_disciplina_id)