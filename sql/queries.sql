-- 3.1
SELECT first_name, last_name, email, registration_ts FROM customers ORDER BY registration_ts ASC;

-- 3.2
SELECT name_product, price FROM products ORDER BY price DESC;

-- 3.3
SELECT status_order, order_ts FROM orders WHERE order_ts BETWEEN '2024-03-01 00:00:00' AND '2024-03-15 00:00:00';

-- 3.4
SELECT name_product, price, stock FROM products WHERE price > 50;

-- 3.5
SELECT p.name_product, p.price, p.stock, c.name_category
FROM products AS p
INNER JOIN categories AS c
ON p.id_category = c.id_category
WHERE c.name_category ILIKE '_lectronique';

-- 4.1
SELECT p.name_product, p.price, p.stock, c.name_category
FROM products as p
INNER JOIN categories AS c
ON p.id_category = c.id_category;

-- 4.2
SELECT o.order_ts, o.status_order, CONCAT_WS(' ', c.first_name, c.last_name) AS full_name
FROM orders AS o
INNER JOIN customers AS c
ON o.id_customer = c.id_customer;

-- 4.3
SELECT
    CONCAT_WS(' ', c.first_name, c.last_name) AS full_name,
    p.name_product,
    oi.quantity,
    oi.price
FROM order_items as oi
INNER JOIN orders as o
ON oi.id_order = o.id_order
INNER JOIN products AS p
ON oi.id_product = p.id_product
INNER JOIN customers as c
ON o.id_customer = c.id_customer;

-- 4.4
SELECT status_order
FROM orders
WHERE status_order IN ('PAID', 'SHIPPED');