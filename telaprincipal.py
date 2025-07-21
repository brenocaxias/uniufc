import tkinter as tk
from tkinter import messagebox
from crud.alunos import abrir_crud_alunos
from crud.professores import abrir_crud_professores
from crud.disciplinas import abrir_crud_disciplinas
from crud.cursos import abrir_crud_cursos
from crud.departamentos import abrir_crud_departamentos
from crud.usuarios import abrir_crud_usuarios
from crud.alunos_graduacao import abrir_crud_alunos_graduacao
from crud.alunos_posgraduacao import abrir_crud_alunos_posgraduacao
from crud.matriculas import abrir_matriculas
from crud.contatos import abrir_gerenciador_contatos
from consultas.aluno import abrir_consulta_aluno
from consultas.disciplinas import abrir_consulta_disciplina
from consultas.orientador import abrir_consulta_orientador
from consultas.departamento import abrir_consulta_departamento
from consultas.disciplinas import abrir_lista_disciplinas_professor
from consultas.aluno_historico import abrir_historico_aluno
from consultas.professor_notas import abrir_notas_professor
from consultas.aluno_disciplinas_atuais import abrir_disciplinas_atuais_aluno


def menu_principal(tipo_usuario, nome_usuario, conexao, id_usuario=None):
    """
    Cria e exibe a janela do menu principal.

    :param tipo_usuario: Nível de acesso do usuário (DBA, professor, etc.).
    :param nome_usuario: Nome do usuário.
    :param conexao: Objeto de conexão com o banco de dados.
    :param id_usuario: O SIAPE do professor ou a matrícula do aluno.
    """
    tipo_usuario = tipo_usuario.strip().lower()
    root = tk.Tk()
    root.title(f"UniUFC-BD - Menu Principal ({tipo_usuario})")
    root.geometry("500x400")
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.focus_force()

    tk.Label(root, text=f"Bem-vindo(a), {nome_usuario}!", font=("Arial", 14)).pack(pady=20)

    if tipo_usuario == "dba":
        tk.Button(root, text="Gerenciar Alunos", width=30, command=lambda: abrir_crud_alunos(conexao)).pack(pady=5)
        tk.Button(root, text="Gerenciar Professores", width=30, command=lambda: abrir_crud_professores(conexao)).pack(
            pady=5)
        tk.Button(root, text="Gerenciar Disciplinas", width=30, command=lambda: abrir_crud_disciplinas(conexao)).pack(
            pady=5)
        tk.Button(root, text="Gerenciar Cursos", width=30, command=lambda: abrir_crud_cursos(conexao)).pack(pady=5)
        tk.Button(root, text="Gerenciar Departamentos", width=30,
                  command=lambda: abrir_crud_departamentos(conexao)).pack(pady=5)
        tk.Button(root, text="Gerenciar Usuários", width=30, command=lambda: abrir_crud_usuarios(conexao)).pack(pady=5)
        tk.Button(root, text="Alunos de Graduação", width=30,
                  command=lambda: abrir_crud_alunos_graduacao(conexao)).pack(pady=5)
        tk.Button(root, text="Alunos de Pós-Graduação", width=30,
                  command=lambda: abrir_crud_alunos_posgraduacao(conexao)).pack(pady=5)
        tk.Button(root, text="Matrícula de Aluno", width=30, command=lambda: abrir_matriculas(conexao)).pack(pady=5)
        tk.Button(root, text="Gerenciar Contatos", width=30, command=lambda: abrir_gerenciador_contatos(conexao)).pack(
            pady=5)
        tk.Button(root, text="Consultar Dados do Aluno", width=30, command=lambda: abrir_consulta_aluno(conexao)).pack(
            pady=5)
        tk.Button(root, text="Consultar Disciplina", width=30, command=lambda: abrir_consulta_disciplina(conexao)).pack(
            pady=5)
        tk.Button(root, text="Consultar Orientador", width=30, command=lambda: abrir_consulta_orientador(conexao)).pack(
            pady=5)
        tk.Button(root, text="Consultar Departamento", width=30,
                  command=lambda: abrir_consulta_departamento(conexao)).pack(pady=5)

    elif tipo_usuario == "funcionario":
        tk.Button(root, text="Consultar Departamento", command=lambda: abrir_consulta_departamento(conexao)).pack(
            pady=5)

    elif tipo_usuario == "professor":
        tk.Button(root, text="Minhas Disciplinas", width=30,
                  command=lambda: abrir_lista_disciplinas_professor(conexao, id_usuario)).pack(pady=5)
        tk.Button(root, text="Alunos e Notas", width=30,
                  command=lambda: abrir_notas_professor(conexao, id_usuario)).pack(pady=5)
        tk.Button(root, text="Consultar Dados do Aluno", width=30, command=lambda: abrir_consulta_aluno(conexao)).pack(
            pady=5)
        tk.Button(root, text="Consultar Disciplina", width=30, command=lambda: abrir_consulta_disciplina(conexao)).pack(
            pady=5)
        tk.Button(root, text="Consultar Orientador", width=30, command=lambda: abrir_consulta_orientador(conexao)).pack(
            pady=5)

    elif tipo_usuario == "aluno":
        # Correção aqui: passar o id_usuario para a consulta de dados pessoais
        tk.Button(root, text="Minhas Disciplinas", width=30,
                  command=lambda: abrir_disciplinas_atuais_aluno(conexao, id_usuario)).pack(pady=5)
        tk.Button(root, text="Histórico Escolar", width=30,
                  command=lambda: abrir_historico_aluno(conexao, id_usuario)).pack(pady=5)
        tk.Button(root, text="Dados Pessoais", width=30,
                  command=lambda: abrir_consulta_aluno(conexao, id_usuario)).pack(pady=5)

    tk.Button(root, text="Sair", width=30, command=root.destroy).pack(pady=20)

    root.mainloop()