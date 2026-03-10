from fastapi import FastAPI, BackgroundTasks
from datetime import datetime
from firebase_connector import FirebaseConnector
from tagoio_connector import send_to_tago
from dotenv import load_dotenv
import pytz
import os

load_dotenv()

app = FastAPI(redirect_slashes=False)

# Conexão com o Firebase Realtime Database
db = FirebaseConnector(
    database_url=os.environ["FIREBASE_DATABASE_URL"],
    credentials_path=os.environ["FIREBASE_CREDENTIALS_PATH"],
)

@app.post("/data")
async def save_data(data: dict, background_tasks: BackgroundTasks):
    # Código para microcontrolador real — descomente quando não estiver simulando
    # date_str = data.get("data")
    # for fmt in ("%Y/%m/%d", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"):
    #     try:
    #         date_obj = datetime.strptime(date_str, fmt)
    #         break
    #     except ValueError:
    #         continue
    # else:
    #     return {"error": f"Formato de data inválido: {date_str}"}

    # Usa o timestamp atual no fuso de São Paulo, pois estamos simulando o microcontrolador
    timezone = pytz.timezone("America/Sao_Paulo")
    formatted_date = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")

    payload = {
        "endereco": data.get("endereco"),
        "data": formatted_date,
        "corrente": data.get("corrente"),
        "dispositivo_id": data.get("id")
    }

    # Salva no Firebase e retorna a chave gerada
    key = db.push("/register", payload)

    background_tasks.add_task(send_to_tago, payload)

    return {"message": "Dados recebidos com sucesso", "payload": payload, "chave": key}

@app.get("/data")
async def get_data():
    # Busca todos os registros no Firebase
    records = db.get_all("/register")
    return {"message": "Dados do Firebase", "database": records}