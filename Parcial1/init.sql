CREATE DATABASE IF NOT EXISTS myflaskapp;
USE myflaskapp;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255),
  username VARCHAR(255) UNIQUE,
  password VARCHAR(255)
);

INSERT INTO users (name,email,username,password) VALUES
('juan','juan@gmail.com','juan','123'),
('maria','maria@gmail.com','maria','456');

CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  price DECIMAL(10,2),
  quantity INT
);

INSERT INTO products (name, price, quantity) VALUES
('pc',150,10),
('phone',100,20),
('teclado',60,20);

CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  userName VARCHAR(255),
  userEmail VARCHAR(255),
  saleTotal DECIMAL(10,2),
  date DATETIME DEFAULT CURRENT_TIMESTAMP
);
