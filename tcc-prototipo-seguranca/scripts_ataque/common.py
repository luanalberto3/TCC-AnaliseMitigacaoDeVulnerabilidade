"""Utilitários compartilhados para os testes do laboratório local."""
from __future__ import annotations

import argparse
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}
PROFILES = ("vulneravel", "protegido")


def profile_args(description: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--perfil", choices=(*PROFILES, "ambos"), default="ambos")
    return parser.parse_args()


def selected_profiles(profile: str) -> tuple[str, ...]:
    return PROFILES if profile == "ambos" else (profile,)


def local_url(url: str) -> str:
    if urlparse(url).hostname not in LOCAL_HOSTS:
        raise ValueError("Os testes aceitam somente URLs locais do laboratório.")
    return url


def dvwa_cookies() -> dict[str, str]:
    session_id = os.getenv("DVWA_PHPSESSID", "")
    if not session_id:
        raise ValueError("Defina DVWA_PHPSESSID após autenticar-se no DVWA para testar o perfil vulnerável.")
    return {"PHPSESSID": session_id, "security": os.getenv("DVWA_SECURITY", "low")}


def protected_base_url() -> str:
    return local_url(os.getenv("PROTEGIDO_BASE_URL", "http://localhost:8082").rstrip("/"))


def dvwa_url(name: str, default_path: str) -> str:
    return local_url(os.getenv(name, f"http://localhost:8080{default_path}"))


def result_path() -> Path:
    configured = os.getenv("TCC_RESULTS_PATH")
    return Path(configured) if configured else Path(__file__).parents[1] / "resultados" / "relatorio_testes.json"


def save_result(result: dict) -> None:
    report = result_path()
    report.parent.mkdir(parents=True, exist_ok=True)
    try:
        content = report.read_text(encoding="utf-8").strip()
        entries = json.loads(content) if content else []
        if not isinstance(entries, list):
            raise ValueError("O relatório deve conter uma lista JSON.")
    except FileNotFoundError:
        entries = []
    entries.append(result)
    temporary = report.with_suffix(".tmp")
    temporary.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(report)


def new_result(*, profile: str, attack: str, success: bool, attempts: int, elapsed: float,
               status_code: int | None, outcome: str, **extra: object) -> dict:
    return {
        "id_execucao": str(uuid.uuid4()),
        "data_hora_utc": datetime.now(timezone.utc).isoformat(),
        "perfil": profile,
        "ataque": attack,
        "sucesso": success,
        "tentativas": attempts,
        "tempo_segundos": round(elapsed, 3),
        "taxa_tentativas_por_segundo": round(attempts / elapsed, 3) if elapsed else None,
        "status_http": status_code,
        "resultado": outcome,
        **extra,
    }


def print_and_save(result: dict) -> None:
    save_result(result)
    print(json.dumps(result, ensure_ascii=False))
