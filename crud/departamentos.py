
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def abrir_crud_departamentos(conexao):
    def listar_departamentos():
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT codigo, nome FROM DEPARTAMENTO")
            for codigo, nome in cursor.fetchall():
                tree.insert("", "end", iid=codigo, values=(codigo, nome))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar departamentos:\n{e}")

    def adicionar_departamento():
        codigo = simpledialog.askstring("Novo Código", "Digite o código do departamento:")
        nome = simpledialog.askstring("Novo Nome", "Digite o nome do departamento:")
        if codigo and nome:
            try:
                cursor = conexao.cursor()
                cursor.execute("INSERT INTO DEPARTAMENTO (codigo, nome) VALUES (%s, %s)", (codigo, nome))
                conexao.commit()
                listar_departamentos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar departamento:\n{e}")

    def excluir_departamento():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um departamento para excluir.")
            return
        confirmar = messagebox.askyesno("Confirmar", "Deseja excluir este departamento?")
        if confirmar:
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM DEPARTAMENTO WHERE codigo = %s", (item,))
                conexao.commit()
                listar_departamentos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir departamento:\n{e}")

    janela = tk.Toplevel()
    janela.title("CRUD - Departamentos")
    janela.geometry("600x350")

    tree = ttk.Treeview(janela, columns=("codigo", "nome"), show="headings")
    tree.heading("codigo", text="Código")
    tree.heading("nome", text="Nome")
    tree.pack(fill="both", expand=True, pady=10)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=5)

    tk.Button(frame_botoes, text="Adicionar", width=15, command=adicionar_departamento).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Excluir", width=15, command=excluir_departamento).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)

    listar_departamentos()