import tkinter as tk
from tkinter import messagebox, ttk

# Define uma função para abrir a janela de disciplinas atuais de um aluno.
# Recebe a 'conexao' com o banco de dados e a 'matricula_aluno' como parâmetros.
def abrir_disciplinas_atuais_aluno(conexao, matricula_aluno):
    # Cria uma nova janela de nível superior (Toplevel).
    # 'Toplevel' é usado para criar janelas secundárias que funcionam de forma independente da janela principal,
    # mas ainda são parte da mesma aplicação Tkinter.
    janela = tk.Toplevel()
    # Define o título da janela.
    janela.title("Minhas Disciplinas Atuais")
    # Define as dimensões iniciais da janela (largura x altura).
    janela.geometry("600x400")

    # Cria um widget Treeview da biblioteca ttk (Themed Tkinter).
    # 'ttk.Treeview' é ideal para exibir dados tabulares (como resultados de banco de dados)
    # de forma organizada, com cabeçalhos de coluna e linhas de dados.
    # 'columns' define os nomes das colunas lógicas que serão usadas para os dados.
    # 'show="headings"' garante que apenas os cabeçalhos das colunas sejam exibidos inicialmente,
    # ocultando a coluna de identificadores padrão do Treeview.
    tree = ttk.Treeview(janela, columns=("disciplina", "nota", "frequencia"), show="headings")
    # Define o texto que aparecerá como cabeçalho para cada coluna.
    tree.heading("disciplina", text="Disciplina")
    tree.heading("nota", text="Nota Final")
    tree.heading("frequencia", text="Frequência (%)")
    # Empacota o widget Treeview na janela.
    # 'fill="both"' faz com que o Treeview preencha tanto horizontal quanto verticalmente o espaço disponível.
    # 'expand=True' permite que o Treeview se expanda se a janela for redimensionada.
    # 'padx' e 'pady' adicionam um preenchimento (margem) horizontal e vertical, respectivamente, ao redor do widget.
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    try:
        # Cria um objeto cursor a partir da conexão com o banco de dados.
        # O cursor é usado para executar comandos SQL no banco de dados.
        cursor = conexao.cursor()
        # Executa uma consulta SQL para obter o nome da disciplina, a média final e a frequência
        # para um aluno específico.
        # - SELECT D.nome, AD.media_final, AD.frequencia: Seleciona as colunas desejadas.
        # - FROM ALUNO_DISCIPLINA AD: Começa da tabela ALUNO_DISCIPLINA (AD é um alias).
        # - JOIN DISCIPLINA D ON AD.codigo_disciplina = D.codigo: Une a tabela ALUNO_DISCIPLINA
        #   com a tabela DISCIPLINA (D é um alias) onde o código da disciplina corresponde.
        #   Isso é necessário para obter o nome da disciplina, que está na tabela DISCIPLINA.
        # - WHERE AD.matricula_aluno = %s: Filtra os resultados para uma matrícula de aluno específica.
        #   '%s' é um placeholder (substituto) para evitar SQL Injection, uma prática de segurança essencial.
        #   O valor real (matricula_aluno) é passado como uma tupla no segundo argumento de execute().
        cursor.execute("""
            SELECT D.nome, AD.media_final, AD.frequencia
            FROM ALUNO_DISCIPLINA AD
            JOIN DISCIPLINA D ON AD.codigo_disciplina = D.codigo
            WHERE AD.matricula_aluno = %s
        """, (matricula_aluno,))

        # Itera sobre cada linha retornada pela consulta SQL (cursor.fetchall()).
        # 'fetchall()' recupera todas as linhas restantes do conjunto de resultados de uma consulta.
        for nome_disciplina, nota, frequencia in cursor.fetchall():
            # Insere cada linha de dados no Treeview.
            # O primeiro argumento "" indica que o item é um item raiz (não tem pai).
            # O segundo argumento "end" adiciona o item no final da lista.
            # 'values' é uma tupla contendo os dados para as colunas definidas no Treeview.
            tree.insert("", "end", values=(nome_disciplina, nota, frequencia))

    except Exception as e:
        # Bloco para tratamento de exceções (erros).
        # Se ocorrer qualquer erro durante a conexão ou execução da consulta SQL,
        # ele será capturado aqui.
        # 'messagebox.showerror()' exibe uma caixa de diálogo de erro para o usuário,
        # informando sobre o problema e exibindo a mensagem de erro detalhada ('e').
        messagebox.showerror("Erro", f"Erro ao buscar suas disciplinas:\n{e}")