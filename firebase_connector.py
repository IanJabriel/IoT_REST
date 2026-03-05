"""
Firebase Realtime Database Connector para APIs Python
Requer: pip install firebase-admin
"""

import firebase_admin
from firebase_admin import credentials, db
from typing import Any, Optional
import logging
import os
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FirebaseConnector:

    def __init__(
        self,
        database_url: str,
        credentials_path: Optional[str] = None,
        credentials_env: Optional[str] = None,
    ):
        self.database_url = database_url
        self._initialize_app(credentials_path, credentials_env)

    def _initialize_app(self, credentials_path: Optional[str], credentials_env: Optional[str]):
        if firebase_admin._apps:
            existing_url = firebase_admin.get_app().options.get("databaseURL")
            if existing_url == self.database_url:
                return
            else:
                firebase_admin.delete_app(firebase_admin.get_app())

        if credentials_env:
            cred_json = json.loads(os.environ[credentials_env])
            cred = credentials.Certificate(cred_json)
        elif credentials_path:
            cred = credentials.Certificate(credentials_path)
        else:
            raise ValueError("Informe credentials_path ou credentials_env.")

        firebase_admin.initialize_app(cred, {"databaseURL": self.database_url})
        logger.info("Firebase conectado com sucesso.")

    def push(self, path: str, data: Any) -> str:
        """Insere novo registro com chave automática."""
        ref = db.reference(path).push(data)
        logger.info(f"PUSH: {path}/{ref.key}")
        return ref.key

    def get_all(self, path: str) -> list[dict]:
        """Retorna todos os registros de um caminho."""
        data = db.reference(path).get()
        if not data:
            return []
        return [{"_key": key, **value} for key, value in data.items()]