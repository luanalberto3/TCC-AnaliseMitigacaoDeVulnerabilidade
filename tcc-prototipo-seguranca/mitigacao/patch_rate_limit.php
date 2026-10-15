<?php
declare(strict_types=1);

// Persistente por conta + IP: uma nova sessão não reinicia o contador.
const MAX_TENTATIVAS_LOGIN = 5;
const JANELA_LOGIN_SEGUNDOS = 60;

/** @return array{permitido: bool, aguarde: int} */
function registrarTentativaLogin(PDO $pdo, string $usuario, string $ip): array
{
    $pdo->exec(
        'DELETE FROM login_attempts
         WHERE attempted_at < DATE_SUB(NOW(), INTERVAL ' . JANELA_LOGIN_SEGUNDOS . ' SECOND)'
    );

    $contagem = $pdo->prepare(
        'SELECT COUNT(*) FROM login_attempts
         WHERE username = :username AND client_ip = :ip
           AND attempted_at >= DATE_SUB(NOW(), INTERVAL ' . JANELA_LOGIN_SEGUNDOS . ' SECOND)'
    );
    $contagem->execute(['username' => $usuario, 'ip' => $ip]);

    if ((int) $contagem->fetchColumn() >= MAX_TENTATIVAS_LOGIN) {
        return ['permitido' => false, 'aguarde' => JANELA_LOGIN_SEGUNDOS];
    }

    $inserir = $pdo->prepare(
        'INSERT INTO login_attempts (username, client_ip) VALUES (:username, :ip)'
    );
    $inserir->execute(['username' => $usuario, 'ip' => $ip]);
    return ['permitido' => true, 'aguarde' => 0];
}

function limparTentativasLogin(PDO $pdo, string $usuario, string $ip): void
{
    $stmt = $pdo->prepare(
        'DELETE FROM login_attempts WHERE username = :username AND client_ip = :ip'
    );
    $stmt->execute(['username' => $usuario, 'ip' => $ip]);
}
