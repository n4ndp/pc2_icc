CREATE DATABASE IF NOT EXISTS flaskapp;

USE flaskapp;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL
);

INSERT INTO users (nombre, username, password) VALUES
('Fernando Adriano Choqque Mejia', 'n4ndp', 'password123'),
('Carlos Alonso Flores Panduro', 'cflowers', 'clave456');
