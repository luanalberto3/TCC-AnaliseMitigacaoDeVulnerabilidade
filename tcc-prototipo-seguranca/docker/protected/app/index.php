<?php
require __DIR__ . '/bootstrap.php';
pageStart('Ambiente protegido — TCC');
?>
<p class="lead">Uma contraparte segura para medir, em ambiente local, como controles bem aplicados reduzem a exploração de vulnerabilidades web.</p>

<div class="feature-grid">
  <a class="feature" href="/login.php">
    <span class="feature-icon">01</span>
    <strong>Autenticação</strong>
    <span>Limite de tentativas por conta e endereço IP.</span>
  </a>
  <a class="feature" href="/sqli.php?id=1">
    <span class="feature-icon">02</span>
    <strong>SQL Injection</strong>
    <span>Consultas parametrizadas com PDO.</span>
  </a>
  <a class="feature" href="/xss.php?name=Visitante">
    <span class="feature-icon">03</span>
    <strong>Cross-Site Scripting</strong>
    <span>Codificação segura da saída HTML.</span>
  </a>
</div>

<aside class="notice"><span>●</span> Serviço disponível apenas na rede local do laboratório.</aside>
<?php pageEnd(); ?>
