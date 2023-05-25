import uvicorn
import socket
import dotenv

#Pega o IP da máquina
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

#Inicia o servidor no host e porta especificados
if __name__ == "__main__":
    uvicorn.run("api_cq:app", host=f'{IPAddr}', port=5000, reload=True)