<?php
declare(strict_types=1);
require __DIR__ . '/bootstrap.php';
require __DIR__ . '/includes/patch_rate_limit.php';

$message = null;
$class = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = substr(trim((string) ($_POST['username'] ?? '')), 0, 64);
    $password = (string) ($_POST['password'] ?? '');
    $ip = (string) ($_SERVER['REMOTE_ADDR'] ?? 'unknown');
    $pdo = db();
    $limit = registrarTentativaLogin($pdo, $username, $ip);

    if (!$limit['permitido']) {
        http_response_code(429);
        $message = 'Muitas tentativas. Aguarde antes de tentar novamente.';
        $class = 'error';
    } else {
        $stmt = $pdo->prepare('SELECT password_hash FROM users WHERE username = :username');
        $stmt->execute(['username' => $username]);
        $user = $stmt->fetch();
        if ($user && password_verify($password, $user['password_hash'])) {
            limparTentativasLogin($pdo, $username, $ip);
            $message = 'Autenticação realizada.';
            $class = 'ok';
        } else {
            http_response_code(401);
            $message = 'Credenciais inválidas.';
            $class = 'error';
        }
    }
}
pageStart('Login protegido');
if ($message) {
    echo '<p class="feedback ' . $class . '">' . htmlspecialchars($message, ENT_QUOTES, 'UTF-8') . '</p>';
}
?>
<p class="lead compact">Após cinco tentativas inválidas para a mesma conta e IP, novas requisições recebem resposta <code>429</code>.</p>
<form method="post" action="/login.php" autocomplete="off">
  <label>Usuário <input name="username" required maxlength="64"></label>
  <label>Senha <input name="password" type="password" required></label>
  <button type="submit">Verificar credenciais <span>→</span></button>
</form>
<?php pageEnd(); ?>
