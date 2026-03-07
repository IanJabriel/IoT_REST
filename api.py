from fastapi import FastAPI
from typing import List
from datetime import datetime
from firebase_connector import FirebaseConnector
import pytz # LIB para teste de timezone, pode ser removida depois de usar o microcontrolador real, já que ele deve enviar a data formatada corretamente.

app = FastAPI(redirect_slashes=False)

db = FirebaseConnector(
    database_url="https://navarro-iot-default-rtdb.firebaseio.com/",
    credentials_path="serviceAccountKey.json",
)

@app.post("/dados")
async def receber_dados(dados: dict):
    # Esse código deve ser descomentado caso seja utilizado um microcontrolador verdadeiro
    # data_str = dados.get("data")

    # for fmt in ("%Y/%m/%d", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"):
    #    try:
    #        data_obj = datetime.strptime(data_str, fmt)
    #        break
    #    except ValueError:
    #        continue
    # else:
    #    return {"error": f"Formato de data inválido: {data_str}"}

    # Data formatada para pegar o timestamp atual, já que estamos simulando um microcontrolador
    fuso = pytz.timezone("America/Sao_Paulo")
    data_formatada = datetime.now(fuso).strftime("%Y-%m-%d %H:%M:%S")

    registro = {
        "endereco": dados.get("endereco"),
        "data": data_formatada,
        "corrente": dados.get("corrente"),
        "dispositivo_id": dados.get("id")
    }

    chave = db.push("/registro", registro)

    return {"message": "Dados recebidos com sucesso", "registro": registro, "chave": chave}

@app.get("/dados")
async def obter_dados():
    todos = db.get_all("/registro")
    return {"message": "Dados do Firebase", "database": todos}