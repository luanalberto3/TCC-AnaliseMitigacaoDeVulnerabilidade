# Ambiente protegido

O serviço `protegido` é a contraparte defensiva do DVWA e fica disponível em
`http://localhost:8082`.

Ele aplica, de fato, os patches mantidos em `mitigacao/`:

- `login.php`: limite de cinco tentativas por usuário e IP em 60 segundos;
- `sqli.php`: validação de inteiro e prepared statement PDO;
- `xss.php`: codificação de toda entrada refletida com `htmlspecialchars`.

A credencial `admin` / `password` existe apenas para verificar o fluxo de
autenticação do laboratório. Não a utilize fora deste ambiente.
