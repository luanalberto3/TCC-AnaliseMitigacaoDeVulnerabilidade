<?php
declare(strict_types=1);
require __DIR__ . '/bootstrap.php';
require __DIR__ . '/includes/patch_sqli.php';

$id = (string) ($_GET['id'] ?? '');
$people = buscarUsuarioPorId(db(), $id);
pageStart('Consulta protegida contra SQL Injection');
?>
<p class="lead compact">A busca aceita somente identificadores inteiros e usa uma consulta parametrizada.</p>
<form method="get" action="/sqli.php">
  <label>ID <input name="id" value="<?= htmlspecialchars($id, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') ?>" required></label>
  <button type="submit">Consultar registro <span>→</span></button>
</form>
<?php if ($id !== '' && !$people): ?>
  <p class="feedback neutral">Nenhum registro encontrado ou identificador inválido.</p>
<?php endif; ?>
<?php foreach ($people as $person): ?>
  <p class="record"><span>REGISTRO ENCONTRADO</span><?= htmlspecialchars($person['first_name'] . ' ' . $person['last_name'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') ?></p>
<?php endforeach; ?>
<?php pageEnd(); ?>
