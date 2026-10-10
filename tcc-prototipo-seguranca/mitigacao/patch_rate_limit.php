<?php
// Inserir antes da validação de login. Requer sessão iniciada (session_start()).
const MAX_TENTATIVAS_LOGIN = 5;
const JANELA_LOGIN_SEGUNDOS = 60;

function permitirTentativaLogin(): bool {
    $agora = time();
    $tentativas = $_SESSION['login_tentativas'] ?? [];
    $tentativas = array_values(array_filter(
        $tentativas,
        fn ($timestamp) => $timestamp > $agora - JANELA_LOGIN_SEGUNDOS
    ));
    if (count($tentativas) >= MAX_TENTATIVAS_LOGIN) {
        $_SESSION['login_tentativas'] = $tentativas;
        return false;
    }
    $tentativas[] = $agora;
    $_SESSION['login_tentativas'] = $tentativas;
    return true;
}

if (!permitirTentativaLogin()) {
    http_response_code(429);
    exit('Muitas tentativas. Aguarde um minuto e tente novamente.');
}
