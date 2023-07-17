'''import os, traceback
import mysql.connector
from dotenv import load_dotenv
from functools import wraps
from datetime import datetime, timedelta, timezone, date
import json, calendar

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

cursor.execute(f"SELECT c.numero_os, c.etapa_servico, c.id_colaborador_1, c.comissao_colab_1, s.tempo_inicio, s.tempo_fim, s.valor_pausa, s.mes FROM comissao c JOIN servicos s ON c.numero_os = s.numero_os WHERE c.id_colaborador_1 = 'Antonio Carlos' AND c.status_avaliacao = 'Aguardando Avaliação'")
resposta_completa_1 = cursor.fetchall()

cursor.execute(f"SELECT c.numero_os, c.etapa_servico, c.id_colaborador_2, c.comissao_colab_2, s.tempo_inicio, s.tempo_fim, s.valor_pausa, s.mes FROM comissao c JOIN servicos s ON c.numero_os = s.numero_os WHERE c.id_colaborador_2 = 'Antonio Carlos' AND c.status_avaliacao = 'Aguardando Avaliação'")
resposta_completa_2 = cursor.fetchall()

cursor.execute(f"SELECT c.numero_os, c.etapa_servico, c.id_colaborador_3, c.comissao_colab_3, s.tempo_inicio, s.tempo_fim, s.valor_pausa, s.mes FROM comissao c JOIN servicos s ON c.numero_os = s.numero_os WHERE c.id_colaborador_3 = 'Antonio Carlos' AND c.status_avaliacao = 'Aguardando Avaliação'")
resposta_completa_3 = cursor.fetchall()


comissao_fixa = []
ordens = []
lista_tuplas = []

for i in resposta_completa_1:
    lista_tuplas.append(i)
    comissao_fixa.append(i[3])
    ordens.append(i[0])

for j in resposta_completa_2:
    lista_tuplas.append(j)
    comissao_fixa.append(j[3])
    ordens.append(j[0])

for k in resposta_completa_3:
    lista_tuplas.append(k)
    ordens.append(k[0])
    comissao_fixa.append(k[3])

soma_comissao = sum(comissao_fixa)

print('Valor Final:', soma_comissao)

total_distintos = len(set(ordens))
print('Quantidade', total_distintos)

mes_atual = datetime.now().month
mes_atual = calendar.month_name[mes_atual]


for i in lista_tuplas:
    print(i)'''

#cursor.execute(f"SELECT DISTINCT c.id_comissao, c.numero_os, c.etapa_servico, s.servico, c.status_avaliacao, c.id_colaborador_1, c.id_colaborador_2, c.id_colaborador_3 FROM comissao c JOIN servicos s ON c.etapa_servico = s.etapa_servico WHERE c.status_avaliacao = 'Aguardando Avaliacao';")
'''cursor.execute(f"SELECT etapa_servico, id_colaborador_1, id_colaborador_2, id_colaborador_3 FROM comissao WHERE id_comissao = 1")
services_comissao = cursor.fetchall()

etapa_svc = services_comissao[0][0]
colaborador_1 = services_comissao[0][1]
colaborador_2 = services_comissao[0][2]
colaborador_3 = services_comissao[0][3]

print(etapa_svc)
print(colaborador_1)
print(colaborador_2)
print(colaborador_3)

with open('comissionamento/static/json/comissao.json', 'r', encoding="utf-8") as f:
    comissao = json.load(f)

comissionamento = comissao[f'{etapa_svc}']['comissao']

if colaborador_2 == '' and colaborador_3 == '':
    print(f'{comissionamento} query de inserção para o colaborador_1')

elif colaborador_2 !=  '' and colaborador_3 == '':
    print(f'{comissionamento/2} para colaborador_1 e colaborador_2')

elif colaborador_3 != '':
    print(f'{comissionamento/3} para colaborador_1, colaborador_2, colaborador_3')

print('Comissão:', comissionamento)

#print(comissao)'''

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


'''import json

with open('comissionamento\static\json\perguntas.json', 'r', encoding='utf-8') as f:
    perguntas = json.load(f)
qst = perguntas.get('176')
print(*(f'{i}\n' for i in qst))'''


from flask import Flask
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/avaliacao', methods=['POST', 'GET'])
def avaliacao(parametro):
    # Faça o processamento necessário com o parâmetro
    # Armazene o valor em cache
    cache.set('parametro', parametro)
    return 'Valor armazenado em cache'

@app.route('/rota2')
def rota2():
    # Recupere o valor do cache
    parametro = cache.get('parametro')
    return f'O valor recebido foi: {parametro}'

if __name__ == '__main__':
    app.run()