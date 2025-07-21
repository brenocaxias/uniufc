import mysql.connector
from mysql.connector import Error

def conectar_bd(usuario,senha, host='localhost',database='Equipe521461'):
    """
        Tenta estabelecer uma conexão com o banco de dados MySQL.

        :param usuario: O nome de usuário do MySQL.
        :param senha: A senha do MySQL.
        :param host: O host do servidor de banco de dados.
        :param database: O nome do banco de dados a ser conectado.
        :return: Um objeto de conexão se a conexão for bem-sucedida, caso contrário, None.
        """
    try:
        conexao= mysql.connector.connect(
            host="localhost",
            user= usuario,
            password= senha,
            database="Equipe521461"
        )
        if conexao.is_connected():
            return conexao
    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySql:",erro)
        return None

