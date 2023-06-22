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

#cursor.execute(f"SELECT DISTINCT c.id_comissao, c.numero_os, c.etapa_servico, s.servico, c.status_avaliacao, c.id_colaborador_1, c.id_colaborador_2, c.id_colaborador_3 FROM comissao c JOIN servicos s ON c.etapa_servico = s.etapa_servico WHERE c.status_avaliacao = 'Aguardando Avaliacao';")
cursor.execute("SELECT etapa_servico FROM comissao WHERE id_comissao = 1")
services_comissao = cursor.fetchone()

#print(services_comissao[0])

with open('comissionamento/static/json/comissao.json', 'r', encoding="utf-8") as f:
    comissao = json.load(f)

print(comissao[f'{services_comissao[0]}']['comissao'])

#print(comissao)

'''cursor.execute(f"SELECT tempo_inicio FROM servicos WHERE id_servico = '1'")
tempo_inicio = cursor.fetchone()

cursor.execute(f"SELECT tempo_pausa FROM servicos WHERE id_servico = '1'")
tempo_pausa = cursor.fetchone()

inicio = tempo_inicio[0]
fim = tempo_pausa[0]

#valor_pausa = valor_pausa[0].strftime(%H:%M:%S)
diferenca = (fim - inicio)

# Extrair horas, minutos e segundos da diferença
horas = diferenca.total_seconds() // 3600
minutos = (diferenca.total_seconds() % 3600) // 60
segundos = diferenca.total_seconds() % 60

# Formatar a string no formato "HH:MM:SS"
valor_pausa = "{:02}:{:02}:{:02}".format(int(horas), int(minutos), int(segundos))

print(valor_pausa)  # Saída: 03:15:30'''

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

