CREATE DATABASE IF NOT EXISTS monolito_db;

USE monolito_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_products (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Dummy data
INSERT INTO users (username, email, password_hash) VALUES
('john_doe', 'john@example.com', 'dummy_hash'),
('jane_doe', 'jane@example.com', 'dummy_hash');

INSERT INTO products (name, description, price) VALUES
('Laptop', 'Powerful laptop', 1200.99),
('Mouse', 'Wireless mouse', 25.50),
('Keyboard', 'Mechanical keyboard', 85.00);
