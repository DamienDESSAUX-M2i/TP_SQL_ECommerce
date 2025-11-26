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