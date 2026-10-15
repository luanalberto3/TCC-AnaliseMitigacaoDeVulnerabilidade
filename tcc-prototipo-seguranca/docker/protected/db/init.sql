CREATE TABLE IF NOT EXISTS users (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(64) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS login_attempts (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(64) NOT NULL,
  client_ip VARCHAR(45) NOT NULL,
  attempted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_login_attempts (username, client_ip, attempted_at)
);

CREATE TABLE IF NOT EXISTS people (
  id INT UNSIGNED PRIMARY KEY,
  first_name VARCHAR(80) NOT NULL,
  last_name VARCHAR(80) NOT NULL
);

INSERT INTO people (id, first_name, last_name) VALUES
  (1, 'Alice', 'Silva'),
  (2, 'Bruno', 'Souza')
ON DUPLICATE KEY UPDATE first_name = VALUES(first_name), last_name = VALUES(last_name);
