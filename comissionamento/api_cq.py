import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from functools import wraps
from datetime import datetime, timedelta, timezone, time
load_dotenv()
app = Flask(__name__)

SECRET_KEY = os.getenv("SECRET_KEY")

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)

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
            app.permanent_session_lifetime = timedelta(minutes=60)

            return redirect(url_for('rota_homepage'))
        else:
            return render_template('index.html', error='Senha incorreta')
    except mysql.connector.Error as error:
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
    if usuario != None:
        return render_template('operacao.html', usuario = usuario, id_user = id_user)
    else:
        return redirect(url_for('index'))
    
# ------------ Rota Inicialização de serviços ------------- #
@app.route('/inicializar', methods=['POST', 'GET'])
@proteger_rota(['Operacional', 'Administrador'])
def inicializar():
    '''id_user = session.get('id_user')

    #estabelece a conexão
    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO servicos (numero_os, id_colaborador_1, id_colaborador_2, id_colaborador_3, descricao, etapa_servico, servico, status_servico, tempo_inicio, tempo_fim, tempo_decorrido, roxo_qtd, roseo_qtd) VALUES (4312, 1, 2, 3, Uma descrição para este teste, 293, Etapa do teste de serviço, Inicializado, 2023-06-01 10:30:00, 2023-06-01 10:50:00, 20, , );")
        response = cursor.fetchone()
    except:
        print('É rapaz')'''
    
    


@app.route('/consulta', methods=['POST', 'GET'])
@proteger_rota(['Operacional', 'Administrador'])
def rota_consulta():
    usuario = session.get('usuario')
    if usuario != None:
        return render_template('consulta.html', usuario = usuario)
    else:
        return redirect(url_for('index'))


@app.route('/qualidade', methods=['POST', 'GET'])
@proteger_rota(['Qualidade', 'Administrador'])
def rota_qualidade():
    usuario = session.get('usuario')
    if usuario != None:
        return render_template('qualidade.html', usuario = usuario)
    else:
        return redirect(url_for('index'))


@app.route('/painel', methods=['POST', 'GET'])
@proteger_rota(['Administrador'])
def rota_painel():
    usuario = session.get('usuario')
    if usuario != None:
        return render_template('painel-adm.html', usuario = usuario)
    else:
        return redirect(url_for('index'))


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





