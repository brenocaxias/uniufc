
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.simpledialog import askstring
from tkcalendar import DateEntry

def abrir_crud_professores(conexao):
    def listar_professores():
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT P.siape, P.nome_completo, P.data_nascimento, P.data_ingresso, D.nome 
                FROM PROFESSOR P
                LEFT JOIN DEPARTAMENTO D ON P.codigo_departamento = D.codigo
            """)
            for siape, nome, nascimento, ingresso, depto in cursor.fetchall():
                tree.insert("", "end", iid=siape, values=(siape, nome, nascimento, ingresso, depto or ""))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar professores:\n{e}")

    def adicionar_professor():
        janela_add = tk.Toplevel()
        janela_add.title("Novo Professor")

        tk.Label(janela_add, text="SIAPE:").grid(row=0, column=0)
        siape_entry = tk.Entry(janela_add)
        siape_entry.grid(row=0, column=1)

        tk.Label(janela_add, text="Nome Completo:").grid(row=1, column=0)
        nome_entry = tk.Entry(janela_add)
        nome_entry.grid(row=1, column=1)

        tk.Label(janela_add, text="Data de Nascimento:").grid(row=2, column=0)
        nascimento_entry = DateEntry(janela_add, date_pattern='yyyy-mm-dd')
        nascimento_entry.grid(row=2, column=1)

        tk.Label(janela_add, text="Data de Ingresso:").grid(row=3, column=0)
        ingresso_entry = DateEntry(janela_add, date_pattern='yyyy-mm-dd')
        ingresso_entry.grid(row=3, column=1)

        tk.Label(janela_add, text="Código do Departamento:").grid(row=4, column=0)
        departamento_entry = tk.Entry(janela_add)
        departamento_entry.grid(row=4, column=1)

        def salvar():
            try:
                cursor = conexao.cursor()
                cursor.execute("""
                    INSERT INTO PROFESSOR (siape, nome_completo, data_nascimento, data_ingresso, codigo_departamento)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    siape_entry.get(),
                    nome_entry.get(),
                    nascimento_entry.get_date(),
                    ingresso_entry.get_date(),
                    departamento_entry.get()
                ))
                conexao.commit()
                janela_add.destroy()
                listar_professores()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar professor:\n{e}")

        tk.Button(janela_add, text="Salvar", command=salvar).grid(row=5, columnspan=2, pady=10)

    def excluir_professor():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um professor para excluir.")
            return
        confirmar = messagebox.askyesno("Confirmar", "Deseja excluir este professor?")
        if confirmar:
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM PROFESSOR WHERE siape = %s", (item,))
                conexao.commit()
                listar_professores()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir professor:\n{e}")

    janela = tk.Toplevel()
    janela.title("CRUD - Professores")
    janela.geometry("700x400")

    tree = ttk.Treeview(janela, columns=("siape", "nome", "nascimento", "ingresso", "departamento"), show="headings")
    tree.heading("siape", text="SIAPE")
    tree.heading("nome", text="Nome")
    tree.heading("nascimento", text="Nascimento")
    tree.heading("ingresso", text="Ingresso")
    tree.heading("departamento", text="Departamento")
    tree.pack(fill="both", expand=True, pady=10)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=5)

    tk.Button(frame_botoes, text="Adicionar", width=15, command=adicionar_professor).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Excluir", width=15, command=excluir_professor).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)

    listar_professores()