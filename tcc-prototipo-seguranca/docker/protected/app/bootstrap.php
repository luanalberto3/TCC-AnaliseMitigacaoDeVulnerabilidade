<?php
declare(strict_types=1);

function db(): PDO
{
    static $pdo = null;
    if ($pdo instanceof PDO) {
        return $pdo;
    }

    $dsn = sprintf(
        'mysql:host=%s;dbname=%s;charset=utf8mb4',
        getenv('DB_HOST') ?: 'banco_protegido',
        getenv('DB_NAME') ?: 'secureapp'
    );
    $pdo = new PDO($dsn, getenv('DB_USER') ?: 'secureapp', getenv('DB_PASSWORD') ?: '', [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_EMULATE_PREPARES => false,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);

    // Credencial exclusivamente didática; o hash é gerado, nunca armazenado em texto puro.
    $seed = $pdo->prepare('SELECT id FROM users WHERE username = :username');
    $seed->execute(['username' => 'admin']);
    if (!$seed->fetch()) {
        $create = $pdo->prepare(
            'INSERT INTO users (username, password_hash) VALUES (:username, :password_hash)'
        );
        $create->execute([
            'username' => 'admin',
            'password_hash' => password_hash('password', PASSWORD_DEFAULT),
        ]);
    }
    return $pdo;
}

function pageStart(string $title): void
{
    header("Content-Security-Policy: default-src 'self'; base-uri 'self'; frame-ancestors 'none'");
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: no-referrer');
    echo '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">';
    echo '<meta name="viewport" content="width=device-width, initial-scale=1">';
    echo '<title>' . htmlspecialchars($title, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') . '</title>';
    echo '<link rel="stylesheet" href="/assets/style.css">';
    echo '</head><body><div class="ambient-glow glow-one"></div><div class="ambient-glow glow-two"></div>';
    echo '<main class="shell"><header class="site-header">';
    echo '<a class="brand" href="/" aria-label="Início do ambiente protegido"><span class="brand-mark">✓</span><span>SecureLab <small>TCC</small></span></a>';
    echo '<nav aria-label="Navegação principal"><a href="/login.php">Autenticação</a><a href="/sqli.php?id=1">SQLi</a><a href="/xss.php?name=Visitante">XSS</a></nav>';
    echo '</header><section class="page-card"><p class="eyebrow">AMBIENTE PROTEGIDO</p>';
    echo '<h1>' . htmlspecialchars($title, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') . '</h1>';
}

function pageEnd(): void
{
    echo '</section><footer>Laboratório local · comparação de medidas de mitigação</footer></main></body></html>';
}
