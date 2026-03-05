from fastapi import FastAPI
from typing import List
from datetime import datetime
from firebase_connector import FirebaseConnector

app = FastAPI(redirect_slashes=False)

db = FirebaseConnector(
    database_url="https://navarro-iot-default-rtdb.firebaseio.com/",
    credentials_path="serviceAccountKey.json",
)

@app.post("/dados")
async def receber_dados(dados: dict):
    data_str = dados.get("data")

    for fmt in ("%Y/%m/%d", "%Y-%m-%d"):
        try:
            data_obj = datetime.strptime(data_str, fmt)
            break
        except ValueError:
            continue
    else:
        return {"error": f"Formato de data inválido: {data_str}"}

    data_formatada = data_obj.strftime("%d/%m/%Y")

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