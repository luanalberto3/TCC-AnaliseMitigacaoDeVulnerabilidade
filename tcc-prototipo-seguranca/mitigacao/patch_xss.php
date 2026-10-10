<?php
// Escape na saída HTML: use sempre o valor escapado, nunca $_GET diretamente.
function escapeHtml(string $value): string {
    return htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

$nome = escapeHtml($_GET['name'] ?? '');
echo '<p>Olá, ' . $nome . '</p>';
