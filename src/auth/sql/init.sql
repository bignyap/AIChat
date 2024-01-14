CREATE TABLE user (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  full_name VARCHAR(255) NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  disabled BOOLEAN NOT NULL DEFAULT TRUE
);

/*ALTER USER 'user'@'host' IDENTIFIED WITH 'mysql_native_password' BY 'password';*/

/*INSERT INTO user (username, email, full_name, hashed_password) VALUES 
('llm', 'llm@llm.com', 'LLM User', 'llm');*/