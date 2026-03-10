import os
import logging
import requests
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

TAGO_ENDPOINT = os.environ.get("TAGO_ENDPOINT", "https://api.eu-w1.tago.io/data")

def _build_variables_from_payload(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    vars_list: List[Dict[str, Any]] = []
    for key in ["corrente", "endereco", "dispositivo_id"]:
        if payload.get(key) is not None:
            vars_list.append({"variable": key, "value": payload.get(key)})
    return vars_list

def send_to_tago(payload: Dict[str, Any], device_token: Optional[str] = None, timeout: int = 5) -> bool:
    token = device_token or os.environ.get("TAGO_DEVICE_TOKEN")
    if not token:
        logger.warning("TAGO_DEVICE_TOKEN não encontrado no .env!")
        return False

    token = token.strip()
    variables = _build_variables_from_payload(payload)
    if not variables: return False

    headers = {
        "Authorization": token, 
        "Content-Type": "application/json"
    }

    logger.info("Enviando para TagoIO | URL=%s | headers=%s", TAGO_ENDPOINT, headers)

    try:
        resp = requests.post(TAGO_ENDPOINT, json=variables, headers=headers, timeout=timeout)
        resp.raise_for_status()
        logger.info("SUCESSO ABSOLUTO! Dados chegaram no TagoIO. status=%s", resp.status_code)
        return True
        
    except requests.RequestException as exc:
        body = exc.response.text if hasattr(exc, "response") and exc.response is not None else None
        logger.error("Falha ao enviar para o TagoIO: %s | corpo: %s", exc, body)
        return False

def send_to_tago_async(payload: Dict[str, Any], device_token: Optional[str] = None, timeout: int = 5) -> None:
    import threading
    t = threading.Thread(target=lambda: send_to_tago(payload, device_token, timeout), daemon=True)
    t.start()