CREATE DATABASE IF NOT EXISTS product_db;
USE product_db;

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL
);

INSERT INTO products (name, description, price) VALUES
('Laptop', 'High performance laptop', 1500.00),
('Smartphone', 'Latest model smartphone', 800.00);