import os, traceback, json, calendar, requests
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_caching import Cache
from functools import wraps
from datetime import datetime, timedelta, timezone, date
load_dotenv()
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

SECRET_KEY = os.getenv("SECRET_KEY")

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=960)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=960)

    # Check if the session has expired
    if 'login_time' in session and \
            datetime.now(timezone.utc) - session['login_time'] > app.permanent_session_lifetime:
        session.clear()  # Clear the session data
        return redirect(url_for('index'))

    # Update the last activity time
    session['last_activity'] = datetime.now(timezone.utc)


#Decorator para proteger as rotas
def proteger_rota(cargos_permitidos):
    def decorator_proteger_rota(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('cargo') in cargos_permitidos or session.get('cargo') == 'admin':
                return f(*args, **kwargs)
            else:
                return redirect(url_for('rota_homepage'))
        return decorated_function
    return decorator_proteger_rota


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


app.secret_key = SECRET_KEY


#Rota principal <- Tela de Login
@app.route('/')
def index():
    return render_template('index.html')


#Rota para validação do formulario
@app.route('/login', methods=['POST', 'GET'])
def login():
    #obtem a senha enviada pelo form
    password = request.form['password']

    #estabelece a conexão
    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM colaboradores WHERE senha = %s", (password,))
        user = cursor.fetchone()

        if user:
            id_user = user[0]
            usuario = user[1]
            cargo = user[3]
            grade = user[4]
            nivel = user[5]
            data_cadastro = user[6]
            
            session['id_user'] = id_user
            session['usuario'] = usuario
            session['cargo'] = cargo
            session['login_time'] = datetime.now(timezone.utc)

            #Crie sessions para as variaveis que quer passar como conteúdo em outras páginas

            # ------- Definir a expiração da sessão para 1 minutos a partir do momento atual -------- #

            # Define o tempo máximo de sessão para 1 minutos a partir do momento atual
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=960)
            return redirect(url_for('rota_homepage'))
        else:
            return render_template('index.html', error='Senha incorreta')
    except Exception as error:
        #buscar como tratar erros de conexão ou consulta
        return f'Erro de banco de dados: {error}'

    finally:
        #fecha a conexão com o db já que pegamos as creds que precisavamos
        conn.close()

@app.route('/homepage')
@proteger_rota(['Administrador', 'Operacional', 'Qualidade'])
def rota_homepage():
    usuario = session.get('usuario')
    if usuario != None:

        return render_template('home.html', usuario = usuario)
    else:
        return redirect(url_for('index'))


# ----------- Rotas Protegidas ----------- #
@app.route('/operacional', methods=['POST', 'GET'])
@proteger_rota(['Operacional', 'Administrador'])
def rota_operacao():
    usuario = session.get('usuario')
    id_user = session.get('id_user')
    cargo = session.get('cargo')

    if usuario != None:
        #Carregamento dos serviços
        usuario = session.get('usuario')
        #estabelece a conexão
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT id_servico, numero_os, etapa_servico, servico, id_colaborador_1, id_colaborador_2, id_colaborador_3, status_servico FROM servicos WHERE id_colaborador_1 = '{usuario}' AND status_servico != 'Finalizado'")
        carregar_servicos = cursor.fetchall()

        #Cadastrar funcionarios da operação
        cursor.execute(f"SELECT nome FROM colaboradores WHERE id_colaborador != '{id_user}' AND cargo = 'Operacional'")
        funcionarios = cursor.fetchall()
        pessoas = []
        for k in funcionarios:
            #print(str(k[0]))
            pessoas.append(k[0])
        conn.commit()
        conn.close()
        return render_template('operacao.html', usuario = usuario, id_user = id_user, lista_svc = carregar_servicos, pessoas = pessoas)
    else:
        return redirect(url_for('index'))


# ------------ Rota Inicialização de serviços ------------- #
@app.route('/operacional/inicializar-servico', methods=['POST', 'GET'])
@proteger_rota(['Operacional', 'Administrador'])
def inicializar():
    responsavel = session.get('usuario')
    colab_id_1 = session.get('id_user')
    colab_id_1 = str(colab_id_1)
    dados_cadastro = request.get_json()
    dados_cadastro['Resposavel'] = responsavel
    dados_cadastro['dtCadastro'] = date.today()
    dados_cadastro['id_colaborador_1'] = responsavel

    data = datetime.now()

    mes_atual = datetime.now().month
    mes_atual = calendar.month_name[mes_atual]

    ano_atual = datetime.now().year
    ano_atual = str(ano_atual)

    data_formatada = data.strftime("%Y-%m-%d %H:%M:%S")
    
    #estabelece a conexão
    conn = get_db_connection()

    init_response = {}

    try:
        cursor = conn.cursor()

        cursor.execute(
            f"SELECT numero_os, etapa_servico, servico, id_colaborador_1, status_servico, tempo_inicio FROM servicos WHERE numero_os = '{dados_cadastro['os']}' AND etapa_servico = '{dados_cadastro['etapa']}';")
        
        verificar = cursor.fetchone()

        if verificar:
            if verificar[1] == 322 or verificar[1] == 323 or verificar[1] == 324:
                print('Passo Extra')
                cursor.nextset()
            else:
                print(verificar)
                conn.close()
                return jsonify({'exists': True, 'dados': verificar})

        with open('static/json/base_servicos.json', 'r', encoding="utf-8") as f:
            #printar o conteudo do json
            svc_json = json.load(f)
            etapa_descricao = svc_json[f"{dados_cadastro['etapa']}"]

        cursor.execute(
            f"INSERT INTO servicos (numero_os, etapa_servico, servico, id_colaborador_1, id_colaborador_2, id_colaborador_3, status_servico, tempo_inicio, valor_pausa, mes, ano) VALUES ({dados_cadastro['os']}, {dados_cadastro['etapa']}, '{etapa_descricao}', '{dados_cadastro['id_colaborador_1']}', '{dados_cadastro['colab2']}', '{dados_cadastro['colab3']}', 'Inicializado', '{data_formatada}', '0', '{mes_atual}', '{ano_atual}');"
            )

        cursor.execute(
           f"INSERT INTO comissao (numero_os, etapa_servico, status_avaliacao, id_colaborador_1, id_colaborador_2, id_colaborador_3, porc_colab1, porc_colab2, porc_colab3, mes, ano) VALUES ('{dados_cadastro['os']}', '{dados_cadastro['etapa']}', 'Aguardando Operação', '{dados_cadastro['id_colaborador_1']}', '{dados_cadastro['colab2']}', '{dados_cadastro['colab3']}', {dados_cadastro['porc_colab1']}, {dados_cadastro['porc_colab2']}, {dados_cadastro['porc_colab3']}, '{mes_atual}', '{ano_atual}');"
        )

        cursor.execute(f"SELECT id_servico FROM servicos WHERE numero_os = '{dados_cadastro['os']}' AND etapa_servico = '{dados_cadastro['etapa']}';")
        resposta_id = cursor.fetchall()

        id_servico = resposta_id[0]


        conn.commit()

        init_response = {
        "id_servico": id_servico,
        "os": dados_cadastro['os'],
        "etapa": dados_cadastro['etapa'],
        "descricao": etapa_descricao,
        "colab_1": dados_cadastro['id_colaborador_1'],
        "colab_2": dados_cadastro['colab2'],
        "colab_3": dados_cadastro['colab3'],
        "status": "Inicializado"
        }
        conn.close()
        return jsonify({'sucess': True, 'dados': init_response})

    except Exception as e:
        print('Ocorreu um erro:', str(e))
        traceback.print_exc()
    
    return jsonify({'sucess': True, 'dados': init_response})


@app.route('/operacional/alterar_status', methods=['POST'])
@proteger_rota(['Operacional', 'Administrador'])
def alterar_status():
    div_id = request.args.get('id')
    acao = request.args.get('acao')
    etapaData = request.args.get('etapa')
    servicoData = request.args.get('servico')
    
    conn = get_db_connection()

    print(div_id, acao, etapaData, servicoData)

    try:
        cursor = conn.cursor()
        # Obtem a data e hora atual
        agora = datetime.now()

        #Formatada
        data_hora_formatada = agora.strftime('%Y-%m-%d %H:%M:%S')

        if acao == 'pausar':
            status = 'Em Pausa'

            #Formatada
            data_hora_formatada = agora.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(f"UPDATE servicos SET status_servico = '{status}', tempo_pausa = '{data_hora_formatada}' WHERE id_servico = '{div_id}'")
            conn.commit()
            return jsonify({"sucesso": True, "status": status})

        elif acao == 'reiniciar':
            status = 'Inicializado'

            cursor.execute(f"SELECT tempo_pausa FROM servicos WHERE id_servico = '{div_id}'")
            tempo_pausa = cursor.fetchone()
            mark_pausa = tempo_pausa[0]

            cursor.execute(f"SELECT valor_pausa FROM servicos WHERE id_servico = '{div_id}'")
            valor_pausa = cursor.fetchone()
            value_pausa = valor_pausa[0]

            diferenca = (agora - mark_pausa) + value_pausa

            # Extrair horas, minutos e segundos da diferença
            horas = diferenca.total_seconds() // 3600
            minutos = (diferenca.total_seconds() % 3600) // 60
            segundos = diferenca.total_seconds() % 60

            value = "{:02}:{:02}:{:02}".format(int(horas), int(minutos), int(segundos))

            cursor.execute(f"UPDATE servicos SET status_servico = '{status}', tempo_reinicio = '{data_hora_formatada}', valor_pausa = '{value}' WHERE id_servico = '{div_id}'")

            conn.commit()

        elif acao == 'finalizar':
            status = 'Finalizado'

            with open('static/json/comissao.json', 'r', encoding="utf-8") as f:
                comissao = json.load(f)
                
            cursor.execute(f"SELECT etapa_servico, id_colaborador_1, id_colaborador_2, id_colaborador_3 FROM comissao WHERE id_comissao = {div_id}")
            services_comissao = cursor.fetchall()

            etapa_svc = services_comissao[0][0]

            colaborador_1 = services_comissao[0][1]
            colaborador_2 = services_comissao[0][2]
            colaborador_3 = services_comissao[0][3]

            comissionamento = comissao[f'{etapa_svc}']['comissao']

            if colaborador_2 == '' and colaborador_3 == '':
                cursor.execute(f"UPDATE comissao SET comissao_colab_1 = '{comissionamento}', comissao_colab_2 = 0, comissao_colab_3 = 0 WHERE id_comissao='{div_id}'")

            elif colaborador_2 !=  '' and colaborador_3 == '':
                cursor.execute(f"UPDATE comissao SET comissao_colab_1 = '{comissionamento/2}', comissao_colab_2 = '{comissionamento/2}', comissao_colab_3 = 0 WHERE id_comissao='{div_id}'")

            elif colaborador_3 != '':
                cursor.execute(f"UPDATE comissao SET comissao_colab_1 = '{comissionamento/3}', comissao_colab_2 = '{comissionamento/3}', comissao_colab_3 = '{comissionamento/3}' WHERE id_comissao='{div_id}'")

            #Formatada
            data_hora_formatada = agora.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(f"UPDATE servicos SET status_servico = '{status}', tempo_fim = '{data_hora_formatada}' WHERE id_servico = '{div_id}'")
            cursor.execute(f"UPDATE comissao SET status_avaliacao = 'Aguardando Avaliação' WHERE id_comissao = '{div_id}'")

            conn.commit()

    except Exception as e:
        print(f'Erro no banco: {e}')
        conn.rollback()
        traceback.print_exc()

    conn.close()
    return acao


@app.route('/consulta', methods=['POST', 'GET'])
@proteger_rota(['Operacional', 'Administrador'])
def rota_consulta():
    usuario = session.get('usuario')
    if usuario != None:
        conn = get_db_connection()
        cursor = conn.cursor()

        mes_atual = datetime.now().month
        mes_atual = calendar.month_name[mes_atual]

        print(mes_atual)

        ano_atual = datetime.now().year
        ano_atual = str(ano_atual)


        cursor.execute(f"SELECT c.numero_os, c.etapa_servico, c.id_colaborador_1, c.comissao_colab_1, s.tempo_inicio, s.tempo_fim, s.valor_pausa, c.total_possivel_1, c.premio_1_colab_1 FROM comissao c JOIN servicos s ON c.numero_os = s.numero_os WHERE c.id_colaborador_1 = '{usuario}' AND s.mes = '{mes_atual}' AND s.ano = '{ano_atual}' AND (c.status_avaliacao = 'Aguardando Avaliação' or c.status_avaliacao = 'Avaliado')")
        resposta = cursor.fetchall()

        cursor.execute(f"SELECT c.numero_os, c.etapa_servico, c.id_colaborador_2, c.comissao_colab_2, s.tempo_inicio, s.tempo_fim, s.valor_pausa, c.total_possivel_2, c.premio_1_colab_2 FROM comissao c JOIN servicos s ON c.numero_os = s.numero_os WHERE c.id_colaborador_2 = '{usuario}' AND s.mes = '{mes_atual}' AND s.ano = '{ano_atual}' AND (c.status_avaliacao = 'Aguardando Avaliação' or c.status_avaliacao = 'Avaliado')")
        resposta_2 = cursor.fetchall()

        cursor.execute(f"SELECT c.numero_os, c.etapa_servico, c.id_colaborador_3, c.comissao_colab_3, s.tempo_inicio, s.tempo_fim, s.valor_pausa, c.total_possivel_3, c.premio_1_colab_3 FROM comissao c JOIN servicos s ON c.numero_os = s.numero_os WHERE c.id_colaborador_3 = '{usuario}' AND s.mes = '{mes_atual}' AND s.ano = '{ano_atual}' AND (c.status_avaliacao = 'Aguardando Avaliação' or c.status_avaliacao = 'Avaliado')")
        resposta_3 = cursor.fetchall()

        comissao_fixa = []
        ordens = []
        lista_tuplas = []
        total_possivel = []
        premio_1 = []

        for i in resposta:
            lista_tuplas.append(i)
            comissao_fixa.append(i[3])
            ordens.append(i[0])
            if i[7] is not None and i[8] is not None:
                total_possivel.append(i[7])
                premio_1.append(i[8])

        for j in resposta_2:
            lista_tuplas.append(j)
            comissao_fixa.append(j[3])
            ordens.append(j[0])
            if j[7] is not None and j[8] is not None:
                total_possivel.append(j[7])
                premio_1.append(j[8])

        for k in resposta_3:
            lista_tuplas.append(k)
            comissao_fixa.append(k[3])
            ordens.append(k[0])
            if k[7] is not None and k[8] is not None:
                total_possivel.append(k[7])
                premio_1.append(k[8])

        soma_comissao = sum(comissao_fixa)
        total_distintos = len(set(ordens))
        #print('prêmio 1:', premio_1)
        #print('Max Premio:', total_possivel)
        max_premio_1 = sum(total_possivel)
        real_premio_1 = sum(premio_1)
        #print('Máximo: ', max_premio_1)
        #print('Real: ', real_premio_1)

        cursor.execute(f"SELECT nota_avaliacao FROM comissao WHERE (id_colaborador_1 = '{usuario}' or id_colaborador_2 = '{usuario}' or id_colaborador_3 = '{usuario}') AND mes = '{mes_atual}' AND ano = '{ano_atual}' AND status_avaliacao = 'Avaliado'")
        notas_resposta = cursor.fetchall()
        #print('RESPOSTA CURSOR: ', notas_resposta)

        notas_avaliacao = []
        for l in notas_resposta:
            if l[0] is not None:
                notas_avaliacao.append(l[0])
        #print(notas_avaliacao)
        if len(notas_avaliacao) > 0:
            nota_avaliacao = (sum(notas_avaliacao)/len(notas_avaliacao))*100
        else:
            nota_avaliacao = 0

        avaliacao = str(nota_avaliacao)+'%'
        #print(avaliacao)


        match mes_atual:
            case 'January':
                mes_atual = 'Janeiro'
            case 'February':
                mes_atual = 'Fevereiro'
            case 'March':
                mes_atual = 'Março'
            case 'April':
                mes_atual = 'Abril'
            case 'May':
                mes_atual = 'Maio'
            case 'June':
                mes_atual = 'Junho'
            case 'July':
                mes_atual = 'Julho'
            case 'August':
                mes_atual = 'Agosto'
            case 'September':
                mes_atual = 'Setembro'
            case 'November':
                mes_atual = 'Novembro'
            case 'December':
                mes_atual = 'Dezembro'
        
        cursor.execute(f'SELECT nome, grade, nivel FROM colaboradores WHERE nome = "{usuario}"')
        resposta_grade = cursor.fetchall()
        resposta_grade = f'Grade {resposta_grade[0][1]} - {resposta_grade[0][2]}'
        conn.commit()

        cursor.execute(f"SELECT valor_premio_2, valor_total FROM premio_2 WHERE nome_colaborador = '{usuario}' AND mes = '{mes_atual}' and ano = '{ano_atual}'")
        resposta_premio_2 = cursor.fetchall()
        #print("Prêmio 2", resposta_premio_2)

        if resposta_premio_2:
            valor_premio_2 = resposta_premio_2[0][0]
            soma_total = resposta_premio_2[0][1]

        else:
            valor_premio_2 = 0
            soma_total = soma_comissao + real_premio_1

        conn.close()

        return render_template('consulta.html', usuario = usuario, soma_comissao = soma_comissao, ordens = total_distintos, mes = mes_atual, ano=ano_atual, total_possivel_1 = max_premio_1, real_premio_1 = real_premio_1, grade = resposta_grade, nota_avaliacao = avaliacao, premio_2 = valor_premio_2)
    else:
        return redirect(url_for('index'))


@app.route('/comissionamento', methods=['POST', 'GET'])
@proteger_rota(['Qualidade', 'Administrador', 'Operacional'])
def comissionamento():
    usuario = session.get('usuario')
    mes = request.args.get('month')
    month = request.args.get('month')

    match month:
        case 'janeiro':
            month = 'January'
        case 'fevereiro':
            month = 'February'
        case 'março':
            month = 'March'
        case 'abril':
            month = 'April'
        case 'maio':
            month = 'May'
        case 'junho':
            month = 'June'
        case 'julho':
            month = 'July'
        case 'agosto':
            month = 'August'
        case 'setembro':
            month = 'September'
        case 'outubro':
            month = 'October'
        case 'novembro':
            month = 'November'
        case 'dezembro':
            month = 'December'


    mes = mes.capitalize()
    comissao = obter_comissao(month, mes)

    #Adicionar depois: Nível de grade, tabela da premiação 2, valores de todos os indicadores e média.

    # Retorna a resposta em formato JSON para o AJAX
    return jsonify({'comissao': comissao[0], 'mes':mes, 'total_distintos': comissao[1], 'max_premio_1': comissao[2], 'real_premio_1': comissao[3], 'nota_avaliacao': comissao[4], 'valor_premio_2': comissao[5], 'soma_total': comissao[6]})


def obter_comissao(month, mes):
    usuario = session.get('usuario')
    year = '2023'

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT c.numero_os, c.etapa_servico, c.id_colaborador_1, c.comissao_colab_1, s.tempo_inicio, s.tempo_fim, s.valor_pausa, c.total_possivel_1, c.premio_1_colab_1 FROM comissao c JOIN servicos s ON c.numero_os= s.numero_os WHERE c.id_colaborador_1 = '{usuario}' AND s.mes = '{month}' AND s.ano = '{year}' AND (c.status_avaliacao = 'Aguardando Avaliação' or c.status_avaliacao = 'Avaliado')")
    resposta = cursor.fetchall()

    cursor.execute(f"SELECT c.numero_os, c.etapa_servico, c.id_colaborador_2, c.comissao_colab_2, s.tempo_inicio, s.tempo_fim, s.valor_pausa, c.total_possivel_2, c.premio_1_colab_2 FROM comissao c JOIN servicos s ON c.numero_os= s.numero_os WHERE c.id_colaborador_2 = '{usuario}' AND s.mes = '{month}' AND s.ano = '{year}' AND (c.status_avaliacao = 'Aguardando Avaliação' or c.status_avaliacao = 'Avaliado')")
    resposta_2 = cursor.fetchall()

    cursor.execute(f"SELECT c.numero_os, c.etapa_servico, c.id_colaborador_3, c.comissao_colab_3, s.tempo_inicio, s.tempo_fim, s.valor_pausa, c.total_possivel_3, c.premio_1_colab_3 FROM comissao c JOIN servicos s ON c.numero_os= s.numero_os WHERE c.id_colaborador_3 = '{usuario}' AND s.mes = '{month}' AND s.ano = '{year}' AND (c.status_avaliacao = 'Aguardando Avaliação' or c.status_avaliacao = 'Avaliado')")
    resposta_3 = cursor.fetchall()

    comissao_fixa = []
    ordens = []
    lista_tuplas = []
    total_possivel = []
    premio_1 = []

    for i in resposta:
        lista_tuplas.append(i)
        comissao_fixa.append(i[3])
        ordens.append(i[0])
        if i[7] is not None and i[8] is not None:
            total_possivel.append(i[7])
            premio_1.append(i[8])

    for j in resposta_2:
        lista_tuplas.append(j)
        comissao_fixa.append(j[3])
        ordens.append(j[0])
        if j[7] is not None and j[8] is not None:
            total_possivel.append(j[7])
            premio_1.append(j[8])

    for k in resposta_3:
        lista_tuplas.append(k)
        comissao_fixa.append(k[3])
        ordens.append(k[0])
        if k[7] is not None and k[8] is not None:
            total_possivel.append(k[7])
            premio_1.append(k[8])

        
    soma_comissao = sum(comissao_fixa)
    total_distintos = len(set(ordens))
    max_premio_1 = sum(total_possivel)
    real_premio_1 = sum(premio_1)
    print(soma_comissao, total_distintos, max_premio_1, real_premio_1)

    cursor.execute(f"SELECT nota_avaliacao FROM comissao WHERE (id_colaborador_1 = '{usuario}' or id_colaborador_2 = '{usuario}' or id_colaborador_3 = '{usuario}') AND mes = '{month}' AND ano = '{year}' AND status_avaliacao = 'Avaliado'")
    notas_resposta = cursor.fetchall()
    #print('RESPOSTA CURSOR: ', notas_resposta)

    notas_avaliacao = []
    for l in notas_resposta:
        if l[0] is not None:
            notas_avaliacao.append(l[0])
    #print(notas_avaliacao)
    if len(notas_avaliacao) > 0:
        nota_avaliacao = (sum(notas_avaliacao)/len(notas_avaliacao))*100
    else:
        nota_avaliacao = 0

    avaliacao = str(nota_avaliacao)+'%'
    #print(avaliacao)
    cursor.execute(f"SELECT valor_premio_2, valor_total FROM premio_2 WHERE nome_colaborador = '{usuario}' AND mes = '{month}' and ano = '{year}'")
    resposta_premio_2 = cursor.fetchall()
    #print("Prêmio 2", resposta_premio_2)

    if resposta_premio_2:
        valor_premio_2 = resposta_premio_2[0][0]
        soma_total = resposta_premio_2[0][1]
    else:
        valor_premio_2 = 0
        soma_total = soma_comissao + real_premio_1
    conn.close()

    return soma_comissao, total_distintos, max_premio_1, real_premio_1, avaliacao, valor_premio_2, soma_total


@app.route('/qualidade', methods=['POST', 'GET'])
@proteger_rota(['Qualidade', 'Administrador'])
def rota_qualidade():
    usuario = session.get('usuario')
    if usuario != None:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT DISTINCT c.id_comissao, c.numero_os, c.etapa_servico, s.servico, c.status_avaliacao, c.id_colaborador_1, c.id_colaborador_2, c.id_colaborador_3, c.mes FROM comissao c JOIN servicos s ON c.etapa_servico = s.etapa_servico WHERE c.status_avaliacao = 'Aguardando Avaliacao';")
        services_comissao = cursor.fetchall()
        for i in range (0, len(services_comissao)):
            mes = services_comissao[i][8]
            match mes:
                case 'January':
                    mes = 'Janeiro'
                case 'February':
                    mes = 'Fevereiro'
                case 'March':
                    mes = 'Março'
                case 'April':
                    mes = 'Abril'
                case 'May':
                    mes = 'Maio'
                case 'June':
                    mes = 'Junho'
                case 'July':
                    mes = 'Julho'
                case 'August':
                    mes = 'Agosto'
                case 'September':
                    mes = 'Setembro'
                case 'November':
                    mes = 'Novembro'
                case 'December':
                    mes = 'Dezembro'

        conn.close()
        return render_template('qualidade.html', usuario = usuario, lista_comissao = services_comissao)
    else:
        return redirect(url_for('index'))


@proteger_rota(['Qualidade', 'Administrador'])
@app.route('/avaliacao', methods=['POST', 'GET'])
def avaliacao():
    data = request.get_json()
    id = data['id']
    osData = data['osData']
    etapaData = data['etapaData']
    servicoData = data['servicoData']
    mes = data['statusServico']


    # Salvar os dados em sessão
    session['dados_avaliacao'] = [id, osData, etapaData, servicoData, mes]

    data = datetime.now()
    data_inicio = data.strftime("%Y-%m-%d %H:%M:%S")
    session['inicio_avaliacao'] = data_inicio

    #print(session.get('dados_avaliacao'))
    return redirect(url_for('avaliar'))

@proteger_rota(['Qualidade', 'Administrador'])
@app.route('/avaliar', methods=['POST', 'GET'])
def avaliar():
    dados_avaliacao = session.get('dados_avaliacao')
    #print('Se printar então deu certo', dados_avaliacao)
    id = dados_avaliacao[0]
    ordem_servico = dados_avaliacao[1]
    etapa = dados_avaliacao[2]
    etapa = etapa.strip()
    servico_nome = dados_avaliacao[3]
    mes = dados_avaliacao[4]

    try:
        with open(r'static/json/perguntas.json', 'r', encoding='utf-8') as f:
            perguntas = json.load(f)
        #print(etapa)
        questoes = perguntas.get(etapa)
        #print(questoes)
    except Exception as e:
        print('Ocorreu um erro:', str(e))  # Exibe a mensagem de erro
        raise  # Levanta o mesmo erro novamente

    return render_template('avaliacao.html', id=id, ordem_servico=ordem_servico, etapa=etapa, servico_nome=servico_nome, mes=mes, questoes = questoes)

@proteger_rota(['Qualidade', 'Administrador'])
@app.route('/premiacao', methods=['POST', 'GET'])
def premiacao():
    inicio_avaliacao = session.get('inicio_avaliacao')
    data_fim = datetime.now()
    fim_avaliacao = data_fim.strftime("%Y-%m-%d %H:%M:%S")

    data = request.get_json()
    id = data.get('id')
    nota = data.get('nota')
    print(float(nota)*100)
    etapa = data.get('etapa')
    #print(f'ID: {id}\nNota:{nota}\nEtapa:{etapa}')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE comissao SET tempo_inicio ='{inicio_avaliacao}', tempo_fim = '{fim_avaliacao}' WHERE id_comissao = '{id}'")
    conn.close()
    if 'inicio_avaliacao' in session:
        del session['inicio_avaliacao']
        print('Hora excluída da sessão')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(f'SELECT id_colaborador_1, id_colaborador_2, id_colaborador_3, porc_colab1, porc_colab2, porc_colab3 FROM comissao WHERE id_comissao = "{id}"')

    resposta = cursor.fetchall()
    colaborador_1 = resposta[0][0]
    colaborador_2 = resposta[0][1]
    colaborador_3 = resposta[0][2]
    
    lista = [colaborador_1, colaborador_2, colaborador_3]
    tamanho = 0
    for i in lista:
        if i != '':
            tamanho += 1

    # Dicionário para armazenar as premiações dos colaboradores
    premiacao_colaboradores = {}

    # Executar o SELECT para obter os cargos dos colaboradores
    for colaborador in lista:
        if colaborador != "":
            query = f"SELECT grade, nivel FROM colaboradores WHERE nome = '{colaborador}'"
            cursor.execute(query)
            resultado_pesquisa = cursor.fetchone()

            #Tomada de decisão para escolher o item da Nova Grade quando o colaborador for o Lailson Ramon
            if colaborador == 'Lailson Ramon':
                cargo_colaborador = f'Nova Grade {resultado_pesquisa[0]} - {resultado_pesquisa[1]}'
                print(f'{cargo_colaborador}')
            else:
                cargo_colaborador = f'Grade {resultado_pesquisa[0]} - {resultado_pesquisa[1]}'
                print(f'Grade {resultado_pesquisa[0]} - {resultado_pesquisa[1]}')

            if resultado_pesquisa:
                cargo = cargo_colaborador
                premiacao_colaboradores[colaborador] = {
                    "total_possivel": "tudo",
                    "cargo": cargo
                }

            else:
                premiacao_colaboradores[colaborador] = {
                    "total_possivel": "tudo",
                    "cargo": None
                }

    # Fechar a conexão com o banco de dados
    conn.close()

    #print(premiacao_colaboradores[colaborador_1])
    with open(r'static\json\premios.json', 'r', encoding='utf-8') as f:
        premios = json.load(f)

    # Lista para armazenar os cargos
    lista_cargos = []

    for chave in premiacao_colaboradores:
        # Acessa o valor do cargo para cada chave
        cargo = premiacao_colaboradores[chave]['cargo']
        # Adiciona o cargo à lista
        lista_cargos.append(cargo)
        etapa_values = premios.get(f'{etapa}')

        #print('VALORES DA ETAPA', etapa_values[cargo])
        lista_cargos.append(etapa_values[cargo])

    if len(lista_cargos) == 2:
        valor_colab_1 = lista_cargos[1]
        print(f'valor colaborador 1: {valor_colab_1}')
        print(f'Valor real colaborador 1: {valor_colab_1*float(nota)}')
        max_colaborador_1 = valor_colab_1
        real_colaborador_1 = valor_colab_1*float(nota)

        max_colaborador_2 = 0
        real_colaborador_2 = 0

        max_colaborador_3 = 0
        real_colaborador_3 = 0
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f"UPDATE comissao SET status_avaliacao = 'Avaliado', nota_avaliacao = '{nota}', total_possivel_1 = '{max_colaborador_1}', premio_1_colab_1 = '{real_colaborador_1}', total_possivel_2 = '{max_colaborador_2}', premio_1_colab_2 = '{real_colaborador_2}', total_possivel_3 = '{max_colaborador_3}', premio_1_colab_3 = '{real_colaborador_3}' WHERE id_comissao = '{id}'")
            conn.commit()
            conn.close()

        except Exception as e:
            print('Ocorreu um erro:', str(e))
        

    elif len(lista_cargos) == 4:
        valor_colab_1 = lista_cargos[1]
        #---------------------------------------------------------- CRIAR LIGAÇÕES NO BANCO DE DADOS ----------------------------------------------------------
        print(f'valor colaborador 1: {valor_colab_1/2}')
        print(f'Valor real colaborador 1: {(valor_colab_1*float(nota))/2}')
        max_colaborador_1 = valor_colab_1/2
        real_colaborador_1 = ((valor_colab_1*float(nota))/2)
        
        valor_colab_2 = lista_cargos[3]
        print(f'valor colaborador 2: {valor_colab_2/2}')
        print(f'Valor real colaborador 2: {(valor_colab_2*float(nota))/2}')
        max_colaborador_2 = valor_colab_2/2
        real_colaborador_2 = (valor_colab_2*float(nota))/2

        max_colaborador_3 = 0
        real_colaborador_3 = 0

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f"UPDATE comissao SET status_avaliacao = 'Avaliado', nota_avaliacao = '{nota}', total_possivel_1 = '{max_colaborador_1}', premio_1_colab_1 = '{real_colaborador_1}', total_possivel_2 = '{max_colaborador_2}', premio_1_colab_2 = '{real_colaborador_2}', total_possivel_3 = '{max_colaborador_3}', premio_1_colab_3 = '{real_colaborador_3}' WHERE id_comissao = '{id}'")
            conn.commit()
            conn.close()
            
        except Exception as e:
            print('Ocorreu um erro:', str(e))

    elif len(lista_cargos) == 6:
        valor_colab_1 = lista_cargos[1]
        print(f'valor colaborador 1: {valor_colab_1/3}')
        print(f'Valor real colaborador 1: {(valor_colab_1*float(nota))/3}')

        max_colaborador_1 = valor_colab_1/3
        real_colaborador_1 = (valor_colab_1*float(nota))/3

        valor_colab_2 = lista_cargos[3]
        print(f'valor colaborador 2: {valor_colab_2/3}')
        print(f'Valor real colaborador 2: {(valor_colab_2*float(nota))/3}')
        max_colaborador_2 = valor_colab_2/3
        real_colaborador_2 = (valor_colab_2*float(nota))/3

        valor_colab_3 = lista_cargos[5]
        print(f'valor colaborador 3: {valor_colab_3/3}')
        print(f'Valor real colaborador 3: {(valor_colab_3*float(nota))/3}')
        max_colaborador_3 = valor_colab_3/3
        real_colaborador_3 = (valor_colab_3*float(nota))/3

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f"UPDATE comissao SET status_avaliacao = 'Avaliado', nota_avaliacao = '{nota}', total_possivel_1 = '{max_colaborador_1}', premio_1_colab_1 = '{real_colaborador_1}', total_possivel_2 = '{max_colaborador_2}', premio_1_colab_2 = '{real_colaborador_2}', total_possivel_3 = '{max_colaborador_3}', premio_1_colab_3 = '{real_colaborador_3}' WHERE id_comissao = '{id}'")
            conn.commit()
            conn.close()
            
        except Exception as e:
            print('Ocorreu um erro:', str(e))

    else:
        resposta = {'message': 'Erro no tamanho da lista, linha 729'}
        return jsonify(resposta), 200

    response = {'message': 'Dados recebidos com sucesso'}
    return jsonify(response), 200


@app.route('/painel', methods=['POST', 'GET'])
@proteger_rota(['Administrador'])
def rota_painel():
    usuario = session.get('usuario')
    if usuario != None:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT nome, cargo, grade, nivel FROM colaboradores WHERE cargo = 'Operacional'")
        colaboradores = cursor.fetchall()
        conn.close()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM comissao WHERE status_avaliacao = "Avaliado"')
        conn.close()

        return render_template('painel-adm.html', usuario = usuario, funcionarios = colaboradores)
    else:
        return redirect(url_for('index'))


@app.route('/painel/premiacao_2', methods=['POST', 'GET'])
@proteger_rota(['Administrador'])
def acao_premio2():
    data = request.get_json()
    action = data.get('action', None)
    
    # Dados enviados na requisição AJAX
    colaborador_name = data.get('colaborador', None)
    mes = data.get('mes', None)
    agenda = data.get('agenda', None)
    ponto = data.get('ponto', None)
    print(colaborador_name, mes, agenda, ponto)

    ano_atual = datetime.now().year
    ano_atual = str(ano_atual)

    # Aqui você pode adicionar a lógica para processar a ação recebida e retornar a resposta apropriada
    if action == 'simular':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT nota_avaliacao FROM comissao WHERE status_avaliacao = "Avaliado" AND (id_colaborador_1 = "{colaborador_name}" OR id_colaborador_2 = "{colaborador_name}" or id_colaborador_3 = "{colaborador_name}") AND mes = "{mes}" AND ano = "2023"')
        retorno = cursor.fetchall()

        items = []
        print("Retorno: ", retorno)
        for i in retorno:
            items.append(i[0])
        
        nota_media = sum(items)/len(items)
        print('media: ', nota_media)
    

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT comissao_colab_1, total_possivel_1, premio_1_colab_1 FROM comissao WHERE id_colaborador_1 = '{colaborador_name}' AND mes = '{mes}' AND ano = '{ano_atual}' AND status_avaliacao = 'Avaliado'")
        resposta = cursor.fetchall()

        cursor.execute(f"SELECT comissao_colab_2, total_possivel_2, premio_1_colab_2 FROM comissao WHERE id_colaborador_2 = '{colaborador_name}' AND mes = '{mes}' AND ano = '{ano_atual}' AND status_avaliacao = 'Avaliado'")
        resposta_2 = cursor.fetchall()

        cursor.execute(f"SELECT comissao_colab_3, total_possivel_3, premio_1_colab_3 FROM comissao WHERE id_colaborador_3 = '{colaborador_name}' AND mes = '{mes}' AND ano = '{ano_atual}' AND status_avaliacao = 'Avaliado'")
        resposta_3 = cursor.fetchall()

        print(f"Resposta 1: ", resposta)
        print(f"Resposta 2: ", resposta_2)
        print(f"Resposta 3: ", resposta_3)

        comissao_fixa = []
        total_possivel = []
        premio_1 = []

        for i in resposta:
            comissao_fixa.append(i[0])
            if i[1] is not None and i[2] is not None:
                total_possivel.append(i[1])
                premio_1.append(i[2])

        for j in resposta_2:
            comissao_fixa.append(j[0])
            if j[1] is not None and j[2] is not None:
                total_possivel.append(j[1])
                premio_1.append(j[2])

        for k in resposta_3:
            comissao_fixa.append(k[0])
            if k[1] is not None and k[2] is not None:
                total_possivel.append(k[1])
                premio_1.append(k[2])

        print("Nota Média: ", nota_media)
        print("Comissão Fixa:", sum(comissao_fixa))
        print("Total Possível: ", sum(total_possivel))
        print("premio_1: ", sum(premio_1))
        agenda = float(agenda)/100
        ponto = float(ponto)/100
        media_total = (agenda + ponto + nota_media)/3
        print(agenda, ponto, nota_media)
        media_total = media_total*100
        media_total = f'{media_total:.4f}'
        print('Média Total: ', media_total)
        media_total = float(media_total)
        print(type(media_total))
        valor_comissao_fixa = sum(comissao_fixa)
        max_premio_1 = sum(total_possivel)
        real_premio_1 = sum(premio_1)


        if media_total >= 98:
            porc_paga = 0.35
        elif media_total <= 97.99 and media_total >= 95:
            porc_paga = 0.30
        elif media_total <= 94.99 and media_total >= 90:
            porc_paga = 0.25
        elif media_total <= 89.99 and media_total >= 85:
            porc_paga = 0.20
        elif media_total <= 84.99 and media_total >= 80:
            porc_paga = 0.15
        elif media_total <= 79.99 and media_total >= 70:
            porc_paga = 0.15
        else:
            porc_paga = 0

        if porc_paga != 0:
            real_premio_1 = float(real_premio_1)
            premio_2 = real_premio_1*porc_paga
        else:
            premio_2 = 0
        print(f'Comissão Fixa: {valor_comissao_fixa}')
        print(f'Prêmio 1 Pago: {real_premio_1}')
        print(f'Porcentagem paga: {porc_paga}')
        print(f'Prêmio 2: {premio_2}')

        porc_tabela = porc_paga*100

        total_valores = float(valor_comissao_fixa) + real_premio_1 + premio_2
        print(f'Total a ser Pago: {total_valores}')
        total_valores = f'{total_valores:.2f}'
        nota_media = nota_media*100
        print('Mês: ', mes)
        premio_2 = f'{premio_2:.2f}'


        resultado = {'resultado': 'Simulação realizada com sucesso', 'comissao': valor_comissao_fixa, 'max_premio1': max_premio_1, 'real_premio_1': real_premio_1, 'colaborador': colaborador_name, 'media_avaliacao': nota_media, 'porc_tabela': porc_tabela, 'premio_2': premio_2, 'valor_total': total_valores}

    elif action == 'salvar':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT nota_avaliacao FROM comissao WHERE status_avaliacao = "Avaliado" AND (id_colaborador_1 = "{colaborador_name}" OR id_colaborador_2 = "{colaborador_name}" or id_colaborador_3 = "{colaborador_name}") AND mes = "{mes}" AND ano = "2023"')
        retorno = cursor.fetchall()

        items = []
        print("Retorno: ", retorno)
        for i in retorno:
            items.append(i[0])
        
        nota_media = sum(items)/len(items)
        print('media: ', nota_media)
    

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT comissao_colab_1, total_possivel_1, premio_1_colab_1 FROM comissao WHERE id_colaborador_1 = '{colaborador_name}' AND mes = '{mes}' AND ano = '{ano_atual}' AND status_avaliacao = 'Avaliado'")
        resposta = cursor.fetchall()

        cursor.execute(f"SELECT comissao_colab_2, total_possivel_2, premio_1_colab_2 FROM comissao WHERE id_colaborador_2 = '{colaborador_name}' AND mes = '{mes}' AND ano = '{ano_atual}' AND status_avaliacao = 'Avaliado'")
        resposta_2 = cursor.fetchall()

        cursor.execute(f"SELECT comissao_colab_3, total_possivel_3, premio_1_colab_3 FROM comissao WHERE id_colaborador_3 = '{colaborador_name}' AND mes = '{mes}' AND ano = '{ano_atual}' AND status_avaliacao = 'Avaliado'")
        resposta_3 = cursor.fetchall()

        print(f"Resposta 1: ", resposta)
        print(f"Resposta 2: ", resposta_2)
        print(f"Resposta 3: ", resposta_3)

        comissao_fixa = []
        total_possivel = []
        premio_1 = []

        for i in resposta:
            comissao_fixa.append(i[0])
            if i[1] is not None and i[2] is not None:
                total_possivel.append(i[1])
                premio_1.append(i[2])

        for j in resposta_2:
            comissao_fixa.append(j[0])
            if j[1] is not None and j[2] is not None:
                total_possivel.append(j[1])
                premio_1.append(j[2])

        for k in resposta_3:
            comissao_fixa.append(k[0])
            if k[1] is not None and k[2] is not None:
                total_possivel.append(k[1])
                premio_1.append(k[2])

        print("Nota Média: ", nota_media)
        print("Comissão Fixa:", sum(comissao_fixa))
        print("Total Possível: ", sum(total_possivel))
        print("premio_1: ", sum(premio_1))
        agenda = float(agenda)/100
        ponto = float(ponto)/100
        media_total = (agenda + ponto + nota_media)/3
        print(agenda, ponto, nota_media)
        media_total = media_total*100
        media_total = f'{media_total:.4f}'
        print('Média Total: ', media_total)
        media_total = float(media_total)
        print(type(media_total))
        valor_comissao_fixa = sum(comissao_fixa)
        max_premio_1 = sum(total_possivel)
        real_premio_1 = sum(premio_1)


        if media_total >= 98:
            porc_paga = 0.35
        elif media_total <= 97.99 and media_total >= 95:
            porc_paga = 0.30
        elif media_total <= 94.99 and media_total >= 90:
            porc_paga = 0.25
        elif media_total <= 89.99 and media_total >= 85:
            porc_paga = 0.20
        elif media_total <= 84.99 and media_total >= 80:
            porc_paga = 0.15
        elif media_total <= 79.99 and media_total >= 70:
            porc_paga = 0.15
        else:
            porc_paga = 0

        if porc_paga != 0:
            real_premio_1 = float(real_premio_1)
            premio_2 = real_premio_1*porc_paga
        else:
            premio_2 = 0
        print(f'Comissão Fixa: {valor_comissao_fixa}')
        print(f'Prêmio 1 Pago: {real_premio_1}')
        print(f'Porcentagem paga: {porc_paga}')
        print(f'Prêmio 2: {premio_2}')

        porc_tabela = porc_paga*100

        total_valores = float(valor_comissao_fixa) + real_premio_1 + premio_2
        print(f'Total a ser Pago: {total_valores}')
        total_valores = f'{total_valores:.2f}'
        nota_media = nota_media*100
        print('Mês: ', mes)
        premio_2 = f'{premio_2:.2f}'

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE premio_2 SET media_avaliacao = {nota_media}, agenda_rotina = {agenda*100}, controle_ponto = {ponto*100}, comissao_fixa = {valor_comissao_fixa}, premio_1 = {real_premio_1}, porc_paga = {porc_tabela} ,valor_premio_2 = {premio_2}, valor_total = {total_valores} WHERE nome_colaborador = '{colaborador_name}' AND mes = '{mes}' AND ano = '{2023}'")
        conn.commit()
        conn.close()

        resultado = {'resultado': 'Itens Salvos com Sucesso!', 'comissao': valor_comissao_fixa, 'max_premio1': max_premio_1, 'real_premio_1': real_premio_1, 'colaborador': colaborador_name, 'media_avaliacao': nota_media, 'porc_tabela': porc_tabela, 'premio_2': premio_2, 'valor_total': total_valores}

    else:
        resultado = {'resultado': 'Ação não reconhecida'}

    return jsonify(resultado)


@app.route('/painel/cadastro-colaborador', methods=['POST', 'GET'])
@proteger_rota(['Administrador'])
def cadastro_colaborador():
    usuario = session.get('usuario')
    dados = request.get_json()
    dados['cadastrado_por'] = usuario
    print(dados)

    # Obter a data atual
    data_atual = datetime.now()

    # Formatar a data no formato desejado (YYYY-MM-DD)
    data_formatada = data_atual.strftime('%Y-%m-%d')

    #estabelece a conexão
    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO colaboradores (nome, senha, cargo, grade, nivel, data_cadastro) VALUES ('{dados['nomeCompleto']}', '{dados['senha']}', '{dados['selectCargo']}', '{dados['selectGrade']}', '{dados['selectNivel']}', '{data_formatada}')")

        conn.commit()
        
        return jsonify({'sucess': True, 'dados': 'Colaborador Cadastrado!'})

    except Exception as e:
        print('Ocorreu um erro:', str(e))
        traceback.print_exc()
        return jsonify({'sucess': True, 'dados': f'Erro de conexão com o banco + {str(e)}'})


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('usuario', None)            #Remove a sessão do usuário
    return 'Logout realizado com sucesso!'  #Criar tela de logout com redirect automatico a tela de login.


@app.route('/sem_permissao')
def rota_sem_permissao():
    usuario = session.get('usuario')
    error = 'Não possui permissões!'
    return render_template('home.html', usuario=usuario, error=error)


# --------------------- PESQUISA DE SATISFAÇÃO ---------------------#
@app.route('/pesquisa-nps', methods=['POST', 'GET'])
def rota_pesquisa():
    return render_template('pesquisa-nps/pesquisa.html')


@app.route('/send-pesquisa', methods=['POST', 'GET'])
def send_pesquisa():
    return jsonify({'resposta': 'Enviado com sucesso!'})


if __name__ == '__main__':
    app.run(host = os.getenv("WORK_IP"), port=5000, debug=True)

