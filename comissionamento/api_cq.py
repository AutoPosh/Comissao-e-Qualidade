from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse('/login.html', {"request": request})

#Cria a conexão com o banco de dados
engine = create_engine('mysql://root:root@192.168.1.147:3306/autoposh_teste')
Session = sessionmaker(bind=engine)

#Cria a sessão
db = Session()

@app.post("/authenticate")
def authenticate(password: str = Form(...)):

    # Consulta o banco de dados para buscar o usuário a partir da senha
    password = str(password)
    query = text(f"SELECT * FROM colaboradores WHERE codigo = '{password}'")
    result = db.execute(query, {"password": password}).fetchone()

    if result:
        usuario = {
            "ID": result[0],  # Corrigir para acessar a coluna "id"
            "nome": result[1],  # Corrigir para acessar a coluna "nome"
            "codigo": result[2],  # Corrigir para acessar a coluna "codigo
            "cargo": result[3]  # Corrigir para acessar a coluna "cargo
        }

        # Definir a expiração da sessão para 10 minutos a partir do momento atual
        expiracao_sessao = datetime.now() + timedelta(minutes=10)

        # Você pode realizar ações adicionais aqui, como gerar um token de autenticação, armazenar informações da sessão, etc.

        # Retornar uma resposta de sucesso com o usuário e a expiração da sessão
        return {
            "message": "Autenticação bem-sucedida",
            "usuario": usuario,
            "expiracao_sessao": expiracao_sessao,
        }
    else:
        # Retornar uma resposta de erro se a senha não for encontrada no banco de dados
        return JSONResponse(status_code=401, content={"message": "Senha inválida"})

@app.get("/index")
async def read_root(request: Request):
    return templates.TemplateResponse('/index.html', {"request": request})

@app.get("/service")
async def about_page(request: Request):
    return templates.TemplateResponse("service.html", {"request": request})

@app.get("/qualidade")
async def about_page(request: Request):
    return templates.TemplateResponse("qualidade.html", {"request": request})

@app.get("/consulta")
async def about_page(request: Request):
    return templates.TemplateResponse("consulta.html", {"request": request})

@app.get("/adm")
async def about_page(request: Request):
    return templates.TemplateResponse("adm.html", {"request": request})