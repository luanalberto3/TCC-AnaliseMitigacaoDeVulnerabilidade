<?php
// Substitui concatenação de entrada do usuário em consultas SQL.
function buscarUsuarioPorId(PDO $pdo, string $id): array {
    if (filter_var($id, FILTER_VALIDATE_INT) === false) {
        return [];
    }
    $sql = 'SELECT first_name, last_name FROM users WHERE user_id = :id';
    $stmt = $pdo->prepare($sql);
    $stmt->execute([':id' => (int) $id]);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}
