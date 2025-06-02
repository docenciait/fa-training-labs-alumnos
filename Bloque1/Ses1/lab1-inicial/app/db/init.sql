CREATE DATABASE IF NOT EXISTS microservice_db;

USE microservice_db;

CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255)
);

-- Datos Dummy 🚀
INSERT INTO items (name, description) VALUES 
('Item 1', 'Description for item 1'),
('Item 2', 'Description for item 2'),
('Item 3', 'Description for item 3');
