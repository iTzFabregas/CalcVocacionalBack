import psycopg2
from psycopg2.extras import execute_values
from psycopg2 import sql
from dotenv import load_dotenv
import os

from defines import areas

def select_all():

    load_dotenv()

    try:
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
        print(f"Erro ao manipular o banco de dados na hora de selecionar: {e}")


def save_results(user_email, scores):

    load_dotenv()

    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DATABASE_NAME"),
            user=os.getenv("USER_NAME"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST_IP"),
            port=os.getenv("PORT")
        )
        cursor = conn.cursor()
        

        delete_query = sql.SQL("DELETE FROM resultado WHERE email = %s;")
        cursor.execute(delete_query, (user_email, ))

        query = "INSERT INTO resultado (email, profissao, pontuacao) VALUES %s"
        values = [(user_email, profissao, score) for profissao, score in zip(areas, scores)]
        execute_values(cursor, query, values)
        
        conn.commit()


        cursor.close()
        conn.close()


    except Exception as e:
        print(f"Erro ao manipular o banco de dados na hora de salvar: {e}")