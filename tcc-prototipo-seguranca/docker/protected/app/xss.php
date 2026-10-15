<?php
declare(strict_types=1);
require __DIR__ . '/bootstrap.php';
require __DIR__ . '/includes/patch_xss.php';

$name = (string) ($_GET['name'] ?? 'Visitante');
pageStart('Saudação protegida contra XSS');
?>
<p class="lead compact">A entrada é tratada como texto antes de ser refletida na página.</p>
<form method="get" action="/xss.php">
  <label>Nome <input name="name" value="<?= escapeHtml($name) ?>"></label>
  <button type="submit">Exibir saudação <span>→</span></button>
</form>
<p class="greeting"><span>Olá,</span> <?= escapeHtml($name) ?></p>
<?php pageEnd(); ?>
