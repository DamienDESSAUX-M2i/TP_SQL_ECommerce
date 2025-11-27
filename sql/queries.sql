-- 3.1
SELECT
    first_name,
    last_name,
    email, registration_ts
FROM customers
ORDER BY registration_ts ASC;

-- 3.2
SELECT
    name_product,
    price
FROM products
ORDER BY price DESC;

-- 3.3
SELECT
    status_order,
    order_ts
FROM orders
WHERE order_ts BETWEEN '2024-03-01 00:00:00' AND '2024-03-15 23:59:59'
ORDER BY order_ts ASC;

-- 3.4
SELECT
    name_product,
    price, stock
FROM products
WHERE price > 50
ORDER BY price DESC;

-- 3.5
SELECT
    p.name_product,
    p.price, p.stock,
    c.name_category
FROM products AS p
INNER JOIN categories AS c ON p.id_category = c.id_category
WHERE c.name_category = 'Électronique';

-- 4.1
SELECT
    p.name_product,
    p.price, p.stock,
    c.name_category
FROM products as p
INNER JOIN categories AS c ON p.id_category = c.id_category;

-- 4.2
SELECT
    o.order_ts,
    o.status_order,
    CONCAT_WS(' ', c.first_name, c.last_name) AS full_name
FROM orders AS o
INNER JOIN customers AS c ON o.id_customer = c.id_customer;

-- 4.3
SELECT
    CONCAT_WS(' ', c.first_name, c.last_name) AS full_name,
    p.name_product,
    oi.quantity,
    oi.price
FROM order_items as oi
INNER JOIN orders as o ON oi.id_order = o.id_order
INNER JOIN products AS p ON oi.id_product = p.id_product
INNER JOIN customers as c ON o.id_customer = c.id_customer;

-- 4.4
SELECT status_order
FROM orders
WHERE status_order IN ('PAID', 'SHIPPED');

-- 5.1
SELECT
    o.order_ts,
    CONCAT_WS(' ', c.first_name, c.last_name) AS full_name,
    p.name_product,
    oi.quantity,
    oi.price,
    (oi.quantity * oi.price) AS total
FROM order_items as oi
INNER JOIN orders as o ON oi.id_order = o.id_order
INNER JOIN products AS p ON oi.id_product = p.id_product
INNER JOIN customers as c ON o.id_customer = c.id_customer
ORDER BY o.order_ts ASC;

-- 5.2
SELECT
    o.id_order,
    CONCAT_WS(' ', c.first_name, c.last_name) AS full_name,
    SUM(oi.quantity * oi.price) AS total
FROM orders as o
INNER JOIN order_items as oi ON o.id_order = oi.id_order
INNER JOIN customers as c ON o.id_customer = c.id_customer
GROUP BY o.id_order
ORDER BY o.order_ts ASC;

-- 5.3
SELECT
    o.id_order,
    SUM(oi.quantity * oi.price) AS total_per_order
FROM order_items as oi
INNER JOIN orders as o ON oi.id_order = o.id_order
GROUP BY o.id_order
HAVING SUM(oi.quantity * oi.price) > 100
ORDER BY total_per_order DESC;

-- 5.4
SELECT
    c.name_category,
    SUM(oi.price * oi.quantity) AS total_per_category
FROM order_items AS oi
INNER JOIN orders AS o ON oi.id_order = oi.id_order
INNER JOIN products AS p ON oi.id_product = p.id_product
INNER JOIN categories AS c ON p.id_product = c.id_product
WHERE o.status_order <> 'CANCELLED'
GROUP BY c.name_category
ORDER BY total_per_category DESC;

-- 6.1
SELECT
    p.name_product,
    SUM(oi.quantity) AS total_quantity
FROM order_items AS oi
INNER JOIN products AS p ON oi.id_product = p.id_product
GROUP BY p.name_product
HAVING SUM(oi.quantity) >= 1
ORDER BY total_quantity DESC;

-- 6.2
SELECT name_product AS name_product_never_sold
FROM products AS p
LEFT JOIN order_items AS oi ON p.id_product = oi.id_product
WHERE oi.id_product IS NULL;

-- 6.3
SELECT
    CONCAT_WS(' ', c.first_name, c.last_name) AS full_name,
    SUM(oi.quantity * oi.price) AS total_spent
FROM customers AS c
INNER JOIN orders AS o ON c.id_customer = o.id_customer
INNER JOIN order_items AS oi ON o.id_order = oi.id_order
INNER JOIN customers AS c ON o.id_customer = c.id_customer
WHERE o.status_order <> 'CANCELLED'
GROUP BY CONCAT_WS(' ', c.first_name, c.last_name)
ORDER BY total_spent DESC
LIMIT 1;


-- 6.4
SELECT
    p.name_product,
    SUM(oi.quantity) AS total_quantity
FROM products AS p
INNER JOIN order_items AS oi ON p.id_product = oi.id_product
GROUP BY p.name_product
ORDER BY SUM(oi.quantity) DESC
LIMIT 3;

-- 6.5
WITH order_totals AS (
    SELECT
        o.id_order,
        SUM(oi.quantity * oi.price) AS total_per_order
    FROM orders AS o
    INNER JOIN order_items AS oi ON oi.id_order = o.id_order
    GROUP BY o.id_order
),

average_total AS (
    SELECT AVG(total_per_order) AS avg_total FROM order_total_per_order
)

SELECT
    ot.id_order,
    ot.total_per_order
FROM order_totals ot, average_total a
WHERE ot.total_per_order > (SELECT avg_total FROM average_total)
ORDER BY ot.total DESC;

-- 7.1
SELECT SUM(oi.quantity * oi.price) AS total_revenue
FROM order_items AS oi
INNER JOIN orders AS o ON oi.id_order = o.id_order
WHERE o.id_order <> 'CANCELLED';

-- 7.2
WITH order_totals AS (
    SELECT SUM(oi.quantity * oi.price) AS total_per_order
    FROM order_items AS oi
    INNER JOIN orders AS o ON oi.id_order = o.id_order
    WHERE o.status_order <> 'CANCELLED'
    GROUP BY oi.id_order
)

SELECT ROUND(AVG(total_per_order), 2) AS avg_total_per_order
FROM order_totals;

-- 7.3
SELECT
    c.name_category,
    SUM(oi.quantity) AS total_quantity
FROM categories AS c
INNER JOIN products AS p ON c.id_category = p.id_category
INNER JOIN order_items AS oi ON p.id_product = oi.id_product
INNER JOIN orders AS o ON oi.id_order = o.id_order
WHERE o.status_order <> 'CANCELLED'
GROUP BY c.id_category
ORDER BY total_quantity DESC;

-- 7.4
SELECT
    EXTRACT(YEAR FROM o.order_ts) AS year,
    EXTRACT(MONTH FROM o.order_ts) AS month,
    SUM(oi.quantity * oi.price) AS total_revenu_per_month
FROM orders AS o
INNER JOIN order_items AS oi ON o.id_order = oi.id_order
WHERE o.status_order <> 'CANCELLED'
GROUP BY EXTRACT(YEAR FROM o.order_ts), EXTRACT(MONTH FROM o.order_ts);

-- 8.1
SELECT
    o.id_order,
    CONCAT_WS(' ', c.first_name, c.last_name) AS full_name,
    o.order_ts,
    CASE
        WHEN o.status_order = 'PAID' THEN 'Payée'
        WHEN o.status_order = 'SHIPPED' THEN 'Expédiée'
        WHEN o.status_order = 'PENDING' THEN 'En attente'
        WHEN o.status_order = 'CANCELLED' THEN 'Annulée'
    END AS status_label
FROM orders AS o
INNER JOIN customers AS c ON o.id_customer = c.id_customer
ORDER BY o.order_ts ASC;

-- 8.2
WITH customer_totals AS (
    SELECT
        c.id_customer,
        CONCAT_WS(' ', c.first_name, c.last_name) AS full_name,
        SUM(oi.quantity * oi.price) AS total_spent
    FROM customers AS c
    JOIN orders AS o ON o.id_customer = c.id_customer
    JOIN order_items oi ON oi.id_order = o.id_order
    WHERE o.status_order <> 'CANCELLED'
    GROUP BY c.id_customer, full_name
)

SELECT
    id_customer,
    full_name,
    total_spent,
    CASE
        WHEN total_spent > 300 THEN 'OR'
        WHEN total_spent >= 100 THEN 'ARGENT'
        ELSE 'BRONZE'
    END AS segment
FROM customer_totals
ORDER BY total_spent DESC;

-- 9.1
SELECT
    c.id_customer,
    CONCAT_WS(' ', c.first_name, c.last_name) As full_name,
    COUNT(o.id_order) AS nb_orders
FROM customers AS c
INNER JOIN orders AS o ON c.id_customer = o.id_customer
GROUP BY c.id_customer, full_name
ORDER BY nb_orders DESC
LIMIT 5;

-- 9.2
SELECT
    c.id_customer,
    CONCAT_WS(' ', c.first_name, c.last_name) As full_name,
    SUM(oi.quantity * oi.price) AS total_spent
FROM customers AS c
JOIN orders AS o ON o.id_customer = c.id_customer
JOIN order_items AS oi ON oi.id_order = o.id_order
WHERE o.status_order <> 'CANCELLED'
GROUP BY c.id_customer, full_name
ORDER BY total_spent DESC
LIMIT 5;

-- 9.3
SELECT
    c.name_category,
    SUM(oi.quantity * oi.price) AS category_revenue
FROM order_items oi
JOIN orders AS o ON o.id_order = oi.id_order
JOIN products AS p ON p.id_product = oi.id_product
JOIN categories AS c ON c.id_category = p.id_category
WHERE o.status_order <> 'CANCELLED'
GROUP BY c.name_category
ORDER BY category_revenue DESC
LIMIT 3;

-- 9.4
SELECT
    p.id_product,
    p.name_product,
    SUM(oi.quantity * oi.price) AS total_revenue
FROM products AS p
LEFT JOIN order_items AS oi ON oi.id_product = p.id_product
LEFT JOIN orders AS o ON o.id_order = oi.id_order
WHERE o.status_order <> 'CANCELLED'
GROUP BY p.id_product, p.name_product
HAVING SUM(oi.quantity * oi.price) < 20
ORDER BY total_revenue ASC;

-- 9.5
SELECT
    c.id_customer,
    CONCAT_WS(' ', c.first_name, c.last_name) As full_name,
    COUNT(o.id_order) AS nb_orders
FROM customers AS c
JOIN orders AS o ON o.id_customer = c.id_customer
GROUP BY c.id_customer, full_name
HAVING COUNT(o.id_order) = 1
ORDER BY full_name;

-- 9.6
SELECT
    p.name_product,
    SUM(oi.quantity * oi.price) AS total_lost
FROM order_items AS oi
INNER JOIN products AS p ON oi.id_product = p.id_product
INNER JOIN orders AS o ON oi.id_order = o.id_order
WHERE status_order = 'CANCELLED'
GROUP BY p.name_product
ORDER BY total_lost DESC;