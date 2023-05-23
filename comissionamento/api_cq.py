from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker
import jwt, json, secrets
from jwt.exceptions import PyJWTError

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Cria a conexão com o banco de dados
engine = create_engine('mysql://root:root@192.168.0.34:3306/autoposh')
Session = sessionmaker(bind=engine)

# Cria a sessão
db = Session()

# Variável global para armazenar o cargo do usuário
user_cargo = None

# Função para buscar o cargo do usuário
async def get_user_cargo(request: Request):
    global user_cargo
    if user_cargo:
        return user_cargo
    else:
        raise HTTPException(status_code=401, detail="Não autorizado")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse('/login.html', {"request": request})

SECRET_KEY = secrets.token_hex(32)
device_id = secrets.token_hex(16)

@app.post("/authenticate")
def authenticate(password: str = Form(...)):
    
    global user_cargo
    # Consulta o banco de dados para buscar o usuário a partir da senha
    password = str(password)
    query = text(f"SELECT * FROM colaboradores WHERE codigo = '{password}'")
    result = db.execute(query, {"password": password}).fetchone()

    if result:
        user_cargo = result[3]

        usuario = {
            "ID": result[0],
            "nome": result[1],
            "codigo": result[2],
            "cargo": result[3],
            "data": f'{result[4]}'
        }

        # Definir a expiração da sessão para 10 minutos a partir do momento atual
        expiracao_sessao = datetime.now() + timedelta(minutes=1)
        
        expira = (datetime.now() + timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")

        try:
            # Gerar um token JWT exclusivo para a sessão
            token_payload = {
                "usuario": usuario,
                "expiracao_sessao": expiracao_sessao.strftime("%Y-%m-%d %H:%M:%S"),
                "device_id": device_id
            }

            token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

            # Retornar uma resposta de sucesso com o usuário e a expiração da sessão
            response = JSONResponse(content={
                "message": "Autenticado"
            })

            #Configurar o token no cookie da resposta
            response.set_cookie(key=f"token_{device_id}", value=token)
            
            return response
        except PyJWTError as e:
            # Lidar com erros de codificação do token JWT
            return JSONResponse(status_code=500, content={"message": "Erro ao gerar o token"}) 

    else:
        # Retornar uma resposta de erro se a senha não for encontrada no banco de dados
        return JSONResponse(status_code=401, content={"message": "Senha inválida"})


@app.get("/index")
async def read_root(request: Request):
    cargo = await get_user_cargo(request)
    if cargo in ["adm", "qualidade", "operacao"]:
        return templates.TemplateResponse('/index.html', {"request": request})
    else:
        raise HTTPException(status_code=403, detail="Acesso não permitido")


@app.get("/service")
async def about_page(request: Request):
    cargo = await get_user_cargo(request)
    if cargo in ["adm", "operacao"]:
        return templates.TemplateResponse("service.html", {"request": request})
    else:
        raise HTTPException(status_code=403, detail="Acesso não permitido")


@app.get("/qualidade")
async def about_page(request: Request):
    cargo = await get_user_cargo(request)
    if cargo in ["adm", "qualidade"]:
        return templates.TemplateResponse("qualidade.html", {"request": request})
    else:
        raise HTTPException(status_code=403, detail="Acesso não permitido")

@app.get("/consulta")
async def about_page(request: Request):
    cargo = await get_user_cargo(request)
    if cargo in ["adm", "operacao"]:
        return templates.TemplateResponse("consulta.html", {"request": request})
    else:
        raise HTTPException(status_code=403, detail="Acesso não permitido")
    
@app.get("/adm")
async def about_page(request: Request):
    cargo = await get_user_cargo(request)
    if cargo in ["adm"]:
        return templates.TemplateResponse("adm.html", {"request": request})
    else:
        raise HTTPException(status_code=403, detail="Acesso não permitido")
    
