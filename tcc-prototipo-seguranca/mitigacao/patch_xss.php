<?php
declare(strict_types=1);

// Escape na saída HTML: use sempre o valor escapado, nunca $_GET diretamente.
function escapeHtml(string $value): string {
    return htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}
