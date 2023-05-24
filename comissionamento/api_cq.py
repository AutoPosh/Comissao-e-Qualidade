import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from functools import wraps
from datetime import timedelta, time, datetime
load_dotenv()
app = Flask(__name__)

SECRET_KEY = os.getenv("SECRET_KEY")


#Decorator para proteger as rotas
def proteger_rota(cargos_permitidos):
    def decorator_proteger_rota(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('cargo') in cargos_permitidos or session.get('cargo') == 'admin':
                return f(*args, **kwargs)
            else:
                return 'Acesso negado!' #Aqui vou colocar um retorno de erro para fazer popup de um modal informando proibição para o acesso;
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
            usuario = user[1]
            cargo = user[3]
            grade = user[4]
            patente = user[5]

            session['usuario'] = usuario
            #se der erro, crie sessions pros outros itens

            # ------- Definir a expiração da sessão para 10 minutos a partir do momento atual -------- #
            expireSession = datetime.now() + timedelta(minutes=2)
            expiraSession_str = (datetime.now() + timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S")

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
@proteger_rota(['Administrador', 'Operacao', 'Qualidade'])
def rota_homepage():
    return render_template('home.html')

# ----------- Rotas Protegidas ----------- #
@app.route('/operacional', methods=['POST', 'GET'])
@proteger_rota(['Operacao', 'Administrador'])
def rota_operacao():
    return render_template('operacao.html')


@app.route('/consulta', methods=['POST', 'GET'])
@proteger_rota(['Operacao', 'Administrador'])
def rota_consulta():
    return render_template('consulta.html')


@app.route('/qualidade', methods=['POST', 'GET'])
@proteger_rota(['Qualidade', 'Administrador'])
def rota_qualidade():
    return render_template('qualidade.html')

@app.route('/painel', methods=['POST', 'GET'])
@proteger_rota(['Qualidade', 'Administrador'])
def rota_qualidade():
    return render_template('painel-adm.html')

@app.route('/logout')
def logout():
    session.pp('usuario', None)             #Remove a sessão do usuário
    return 'Logout realizado com sucesso!'  #Criar tela de logout com redirect automatico a tela de login.


if __name__ == '__main__':
    app.run(host = os.getenv("WORK_IP"), port=5000)

