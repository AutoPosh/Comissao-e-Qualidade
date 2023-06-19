import os, traceback
import mysql.connector
from dotenv import load_dotenv
from functools import wraps
from datetime import datetime, timedelta, timezone, date
import json
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
cursor.execute(f"SELECT tempo_pausa FROM servicos WHERE id_servico = '1'")
resultado = cursor.fetchone()

print(resultado)

'''cursor.execute(f"SELECT id_servico, numero_os, etapa_servico, servico, id_colaborador_1, id_colaborador_2, id_colaborador_3, status_servico FROM servicos WHERE id_colaborador_1 = 'Ed Campos' and status_servico = 'Inicializado'")
servicos = cursor.fetchall()


lista_servicos = {}

for i in servicos:
    print(i[0])

for tupla in servicos:
    servico = {
        'numero_os': tupla[1],
        'etapa': tupla[2],
        'descricao': tupla[3],
        'colaborador_1': tupla[4],
        'colaborador_2': tupla[5],
        'colaborador_3': tupla[6],
        'situacao': tupla[7],
        # ... adicione os demais campos aqui
    }

    lista_servicos['id ' + str(tupla[0])] = servico

# Converter o dicionário em formato JSON
json_servicos = json.dumps(lista_servicos, indent=4, ensure_ascii=False)'''

# Imprimir o JSON resultante
#print(json_servicos)



'''cursor.execute(f"SELECT nome FROM colaboradores where id_colaborador = '1' or id_colaborador = '2' or id_colaborador = '3'")
response = cursor.fetchall()

cursor.execute(f"SELECT id_servico from servicos where numero_os = 4523 AND etapa_servico = 1234")
resposta = cursor.fetchone()
print(resposta)
id_servico = resposta[0]
id_servico = resposta[0][0]

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

print(id_servico)'''

