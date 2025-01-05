import psycopg2
from dotenv import load_dotenv
import os

def select_all():

    load_dotenv()

    try:
        # Conexão com o banco de dados
        conn = psycopg2.connect(
            dbname=os.getenv("DATABASE_NAME"),
            user=os.getenv("USER_NAME"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST_IP"),
            port=os.getenv("PORT")
        )
        cursor = conn.cursor()  

        # Consultar os dados
        cursor.execute("SELECT * FROM " + os.getenv("TABLE_NAME") + ";")
        resultados = cursor.fetchall()

        # Transformar o resultado em uma lista de dicionários
        colunas = [desc[0] for desc in cursor.description]
        lista_resultados = [dict(zip(colunas, linha)) for linha in resultados]

        cursor.close()
        conn.close()

        return lista_resultados

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

