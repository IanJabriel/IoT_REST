# API IoT - Sistemas Embarcados

API REST desenvolvida com **FastAPI** para receber e consultar dados de sensores IoT (corrente elétrica), integrada com **Firebase Realtime Database** e dispositivos ESP32.

---

## Endpoints

### `POST /dados`

Recebe dados do sensor IoT e armazena no Firebase Realtime Database.

**Body (JSON):**

```json
{
  "endereco": "sensor_01",
  "corrente": 12.5,
  "id": 1
}
```

- O campo `data` é gerado automaticamente pela API com o timestamp atual no fuso horário de São Paulo (`America/Sao_Paulo`), no formato `YYYY-MM-DD HH:MM:SS`.
- O registro é salvo no caminho `/registro` do Firebase com uma chave automática.

**Resposta:**

```json
{
  "message": "Dados recebidos com sucesso",
  "registro": {
    "endereco": "sensor_01",
    "data": "2026-03-07 14:30:00",
    "corrente": 12.5,
    "dispositivo_id": 1
  },
  "chave": "-NxAbC123def"
}
```

### `GET /dados`

Retorna todos os registros armazenados no Firebase.

**Resposta:**

```json
{
  "message": "Dados do Firebase",
  "database": [
    {
      "_key": "-NxAbC123def",
      "endereco": "sensor_01",
      "data": "2026-03-07 14:30:00",
      "corrente": 12.5,
      "dispositivo_id": 1
    }
  ]
}
```

---

## Como rodar

### 1. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar o Firebase

Coloque o arquivo `serviceAccountKey.json` (chave de conta de serviço do Firebase) na raiz do projeto.

### 4. Iniciar o servidor

```bash
uvicorn api:app --reload
```

A API estará disponível em `http://localhost:8000` ou, no Codespace, em:

`https://jubilant-space-goggles-jprq9xq56wjhqv9q-4500.app.github.dev/`

A documentação interativa (Swagger) pode ser acessada em `http://localhost:8000/docs` ou:

`https://jubilant-space-goggles-jprq9xq56wjhqv9q-4500.app.github.dev/docs`

---

## Tecnologias

- **Python**
- **FastAPI**
- **Uvicorn**
- **Firebase Admin SDK** (Realtime Database)
- **pytz**

---

## Estrutura do Projeto

```
IoT_REST/
├── api.py                  # Código principal da API (rotas)
├── firebase_connector.py   # Conector do Firebase Realtime Database
├── serviceAccountKey.json  # Credenciais do Firebase (não versionar)
├── requirements.txt        # Dependências do projeto
└── README.md
```
