
# Gerencia as operações de CRUD para a entidade DEPARTAMENTO.

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


def abrir_crud_departamentos(conexao):
    """
    Cria a janela do CRUD de departamentos.

    :param conexao: Objeto de conexão com o banco de dados.
    """

    def listar_departamentos():
        """
        Lista todos os departamentos do banco de dados.
        """
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
        """
        Adiciona um novo departamento.
        """
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

    def editar_departamento():
        """
        Abre uma nova janela para editar um departamento selecionado.
        """
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um departamento para editar.")
            return

        valores_atuais = tree.item(item, "values")
        codigo_antigo = valores_atuais[0]

        janela_edit = tk.Toplevel()
        janela_edit.title(f"Editar Departamento (Código: {codigo_antigo})")

        tk.Label(janela_edit, text="Nome:").grid(row=0, column=0)
        nome_entry = tk.Entry(janela_edit)
        nome_entry.insert(0, valores_atuais[1])  # Preenche com valor atual
        nome_entry.grid(row=0, column=1)

        def salvar_edicao():
            """
            Salva as alterações do departamento no banco de dados.
            """
            try:
                novo_nome = nome_entry.get()

                cursor = conexao.cursor()
                cursor.execute("""
                    UPDATE DEPARTAMENTO SET 
                    nome = %s 
                    WHERE codigo = %s
                """, (novo_nome, codigo_antigo))
                conexao.commit()
                janela_edit.destroy()
                listar_departamentos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao editar departamento:\n{e}")

        tk.Button(janela_edit, text="Salvar Alterações", command=salvar_edicao).grid(row=1, columnspan=2, pady=10)

    def excluir_departamento():
        """
        Exclui um departamento selecionado.
        """
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

    # ----- Interface da Janela -----
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
    tk.Button(frame_botoes, text="Editar", width=15, command=editar_departamento).pack(side="left",
                                                                                       padx=5)  # Botão de Editar
    tk.Button(frame_botoes, text="Excluir", width=15, command=excluir_departamento).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)

    listar_departamentos()