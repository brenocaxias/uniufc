# Ponto de entrada da aplicação "UniUFC-BD"

import os
import sys
import tkinter as tk
import mysql.connector
# Importa a função de login do banco de dados
from login_mysql import login_bd
from login_sistema import login_sistema # Importa a proxima tela

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def iniciar_sistema():
    """
    Função principal que inicia o fluxo do sistema.
    Gerencia a sequência de janelas de login.
    """
    try:
        # Chama a função de login do MySQL e espera a conexão
        conexao = login_bd()

        # Se a conexão for bem-sucedida, prossegue para a tela de login do sistema
        if conexao:
            login_sistema(conexao)

    except Exception as e:
        print("Erro ao iniciar o sistema:", e)
        sys.exit(1)

if __name__ == "__main__":
    iniciar_sistema()