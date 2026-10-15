"""Compara XSS refletido no DVWA vulnerável e no ambiente protegido local."""
import time

import requests

from common import (dvwa_cookies, dvwa_url, local_url, new_result, print_and_save,
                    profile_args, protected_base_url, selected_profiles)

PAYLOAD = "<script>alert('XSS_Vulnerability')</script>"


def run_vulnerable() -> dict:
    started = time.perf_counter()
    response = requests.get(dvwa_url("DVWA_XSS_URL", "/vulnerabilities/xss_r/"), params={"name": PAYLOAD}, cookies=dvwa_cookies(), timeout=10)
    injected = PAYLOAD in response.text
    return new_result(profile="vulneravel", attack="xss_refletido", success=injected, attempts=1, elapsed=time.perf_counter() - started, status_code=response.status_code, outcome="payload_refletido_sem_codificacao" if injected else "payload_sem_efeito")


def run_protected() -> dict:
    started = time.perf_counter()
    response = requests.get(local_url(f"{protected_base_url()}/xss.php"), params={"name": PAYLOAD}, timeout=10)
    injected = PAYLOAD in response.text
    return new_result(profile="protegido", attack="xss_refletido", success=injected, attempts=1, elapsed=time.perf_counter() - started, status_code=response.status_code, outcome="payload_refletido_sem_codificacao" if injected else "saida_codificada")


def main() -> None:
    args = profile_args(__doc__ or "Teste de XSS")
    for profile in selected_profiles(args.perfil):
        try:
            result = run_vulnerable() if profile == "vulneravel" else run_protected()
        except (requests.RequestException, ValueError) as error:
            result = new_result(profile=profile, attack="xss_refletido", success=False, attempts=0, elapsed=0, status_code=None, outcome="erro_de_execucao", erro=str(error))
        print_and_save(result)


if __name__ == "__main__":
    main()
