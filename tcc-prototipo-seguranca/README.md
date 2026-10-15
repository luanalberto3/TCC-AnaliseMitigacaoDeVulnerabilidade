 # Protótipo TCC — Análise e Mitigação de Vulnerabilidades Web

Laboratório local para comparar ataques simulados contra um ambiente vulnerável
(DVWA) e uma aplicação protegida. Os testes são bloqueados para alvos que não
sejam `localhost`.

## Serviços

| Perfil | Endereço | Finalidade |
|---|---|---|
| Vulnerável | `http://localhost:8080` | DVWA com nível de segurança `Low` |
| Protegido | `http://localhost:8082` | Aplicação com rate limiting, PDO e codificação HTML |

## 1. Subir o laboratório

No PowerShell, execute:

```powershell
cd C:\Users\windows\Desktop\TCC\tcc-prototipo-seguranca\docker
docker compose up -d --build
docker compose ps
```

Os serviços `tcc-dvwa`, `tcc-protegido` e `tcc-banco-protegido` devem aparecer
como ativos. Aguarde o banco protegido ficar `healthy` antes de realizar testes.

## 2. Preparar o ambiente vulnerável (DVWA)

1. Abra `http://localhost:8080/setup.php`.
2. Clique em **Create / Reset Database**.
3. Entre no DVWA com `admin` e `password`.
4. Abra **DVWA Security** e selecione o nível **Low**.
5. No navegador, pressione `F12` → **Application** → **Cookies** →
   `http://localhost:8080` e copie o valor de `PHPSESSID`himkas8413ll2adtn9fittjrd3.

Defina a sessão no mesmo PowerShell que executará os scripts:

```powershell
$env:DVWA_PHPSESSID = "COLE_AQUI_O_PHPSESSID" 
$env:DVWA_SECURITY = "low"
```

> Não publique o valor de `PHPSESSID`; ele é um cookie temporário de sessão.

## 3. Instalar dependências Python

Na raiz do projeto:

```powershell
cd C:\Users\windows\Desktop\TCC\tcc-prototipo-seguranca
pip install -r requirements.txt
```

## 4. Executar os ataques no ambiente vulnerável

Com o cookie configurado, execute:

```powershell
python .\scripts_ataque\01_brute_force.py --perfil vulneravel
python .\scripts_ataque\02_sql_injection.py --perfil vulneravel
python .\scripts_ataque\03_xss_injection.py --perfil vulneravel
```

Resultados esperados no DVWA com nível `Low`:

| Ataque | Resultado esperado |
|---|---|
| Força bruta | Credencial de laboratório aceita após várias tentativas |
| SQL Injection | Dados retornados após o payload de teste |
| XSS refletido | Payload presente na resposta sem codificação |

## 5. Executar os ataques no ambiente protegido

O ambiente protegido não exige cookie. Execute:

```powershell
python .\scripts_ataque\01_brute_force.py --perfil protegido
python .\scripts_ataque\02_sql_injection.py --perfil protegido
python .\scripts_ataque\03_xss_injection.py --perfil protegido
```

Resultados esperados:

| Ataque | Resultado esperado |
|---|---|
| Força bruta | Sexta tentativa bloqueada com HTTP `429` |
| SQL Injection | Identificador inválido rejeitado, sem exposição de registros |
| XSS refletido | Conteúdo refletido como texto codificado, sem script executável |

Após executar força bruta contra o perfil protegido, aguarde 60 segundos antes
de repeti-la. O rate limit é persistente por usuário e endereço IP.

## 6. Executar a comparação completa

O valor padrão de `--perfil` é `ambos`; com a sessão do DVWA configurada:

```powershell
python .\scripts_ataque\01_brute_force.py --perfil ambos
python .\scripts_ataque\02_sql_injection.py --perfil ambos
python .\scripts_ataque\03_xss_injection.py --perfil ambos
```

Cada execução adiciona uma entrada em `resultados/relatorio_testes.json`, com
perfil, ataque, sucesso, tentativas, tempo, taxa de requisições, status HTTP e
resultado observado.

## Encerrar o laboratório

```powershell
cd docker
docker compose down
```

Use este projeto exclusivamente nos serviços locais fornecidos pelo laboratório.
