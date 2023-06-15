import os, traceback
import mysql.connector
from dotenv import load_dotenv
from functools import wraps
from datetime import datetime, timedelta, timezone, date
load_dotenv()

#Configuração do banco de dados MySQL
db_config = {
    'host': f'{os.getenv("WORK_IP")}',
    'user': f'{os.getenv("USER_WORK")}',
    'password': f'{os.getenv("PASS_DB_WORK")}',
    'database': f'{os.getenv("DB_NAME")}'
}


#Obtem a conexão com o DB
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

#estabelece a conexão
conn = get_db_connection()

cursor = conn.cursor()

cursor.execute(f"SELECT nome FROM colaboradores where id_colaborador = '1' or id_colaborador = '2' or id_colaborador = '3'")

response = cursor.fetchall()


lista = []
for i in response:
    lista.append(i[0])

responsaveis = ' | '.join(lista)

print(responsaveis)

if len(lista) > 0:
    print(f'Colaborador 1: {lista[0]}')

if len(lista) > 1:
    colab_2 = lista[1]
    print(f'Colaborador 2: {colab_2}')

if len(lista) > 2:
    colab_3 = lista[2]
    print(f'Colaborador 3: {colab_3}')


print(lista[0])
print(colab_2)
print(colab_3)



