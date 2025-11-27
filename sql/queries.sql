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

-- 5.1
SELECT
    o.order_ts,
    CONCAT_WS(' ', c.first_name, c.last_name) AS full_name,
    p.name_product,
    oi.quantity,
    oi.price,
    oi.quantity * oi.price AS total
FROM order_items as oi
INNER JOIN orders as o
ON oi.id_order = o.id_order
INNER JOIN products AS p
ON oi.id_product = p.id_product
INNER JOIN customers as c
ON o.id_customer = c.id_customer
ORDER BY o.order_ts;

-- 5.2
SELECT
    o.order_ts,
    o.status_order,
    SUM(oi.quantity * oi.price) AS total
FROM order_items as oi
INNER JOIN orders as o
ON oi.id_order = o.id_order
GROUP BY o.id_order
ORDER BY o.order_ts;

-- 5.3
SELECT
    o.order_ts,
    o.status_order,
    SUM(oi.quantity * oi.price) AS total
FROM order_items as oi
INNER JOIN orders as o
ON oi.id_order = o.id_order
GROUP BY o.id_order
HAVING SUM(oi.quantity * oi.price) > 100
ORDER BY o.order_ts;

-- 5.4
SELECT
    p.name_product,
    SUM(oi.price * oi.quantity) AS total_revenue
FROM order_items as oi
INNER JOIN products as p
ON oi.id_product = p.id_product
GROUP BY p.id_product;

-- 6.1
SELECT
    p.name_product,
    SUM(oi.quantity) AS total_quantity
FROM order_items AS oi
INNER JOIN products AS p
ON oi.id_product = p.id_product
GROUP BY p.name_product, oi.quantity
HAVING SUM(oi.quantity) >= 1;

-- 6.2
SELECT name_product AS name_product_never_sold
FROM products
WHERE id_product NOT IN (
    SELECT id_product
    FROM order_items
    WHERE quantity >=1
);

-- 6.3
SELECT
    CONCAT_WS(' ', c.first_name, c.last_name) AS full_name,
    SUM(agg2.total) AS total
FROM customers as c
INNER JOIN (
    SELECT
        o.id_customer,
        agg1.total
    FROM orders AS o
    INNER JOIN (
        SELECT
            id_order,
            SUM(quantity * price) AS total
        FROM order_items
        GROUP BY id_order
        ) AS agg1
    ON o.id_order = agg1.id_order
    ) AS agg2
ON c.id_customer = agg2.id_customer
GROUP BY CONCAT_WS(' ', c.first_name, c.last_name), agg2.id_customer
ORDER BY SUM(agg2.total) DESC
LIMIT 1;

-- 6.4
SELECT
    p.name_product,
    SUM(oi.quantity) AS total_quantity
FROM products AS p
INNER JOIN order_items AS oi
ON p.id_product = oi.id_product
GROUP BY p.name_product, oi.id_product
ORDER BY SUM(oi.quantity) DESC
LIMIT 3;

-- 6.5
SELECT
    o.order_ts,
    o.status_order,
    agg.total_per_order
FROM orders AS o
INNER JOIN (
    SELECT
        id_order,
        SUM(quantity * price) AS total_per_order
    FROM order_items
    GROUP BY id_order
    HAVING SUM(quantity * price) > (
        SELECT AVG(total_per_order)
        FROM (
            SELECT SUM(quantity * price) AS total_per_order
            FROM order_items
            GROUP BY id_order
            )
        )
    ) AS agg
ON o.id_order = agg.id_order;

-- 7.1
SELECT SUM(quantity * price) AS total_revenue
FROM order_items
WHERE id_order NOT IN (
    SELECT id_order
    FROM orders
    WHERE status_order = 'CANCELLED'
);

-- 7.2
SELECT ROUND(AVG(total_per_order))
FROM (
    SELECT SUM(quantity * price) AS total_per_order
    FROM order_items
    GROUP BY id_order
);

-- 7.3
SELECT
    c.name_category,
    SUM(oi.quantity)
FROM categories AS c
INNER JOIN products AS p
ON c.id_category = p.id_category
INNER JOIN order_items AS oi
ON p.id_product = oi.id_product
GROUP BY c.id_category;

-- 7.4
SELECT
    EXTRACT(YEAR FROM o.order_ts) AS year,
    EXTRACT(MONTH FROM o.order_ts) AS month,
    SUM(agg.total_per_order) AS total_revenu_per_month
FROM orders AS o
INNER JOIN (
    SELECT id_order, SUM(quantity * price) AS total_per_order
    FROM order_items
    GROUP BY id_order
    ) AS agg
ON o.id_order = agg.id_order
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
    END AS status
FROM orders AS o
INNER JOIN customers AS c
ON o.id_customer = c.id_customer;

-- 8.2
SELECT
    CONCAT_WS(' ', c.first_name, c.last_name) AS full_name,
    agg2.total_per_customer,
    CASE
        WHEN agg2.total_per_customer > 300 THEN 'OR'
        WHEN agg2.total_per_customer >= 100 THEN 'ARGENT'
        ELSE 'BRONZE'
    END AS segment
FROM customers AS c
INNER JOIN (
    SELECT
        o.id_customer,
        SUM(agg1.total_per_order) AS total_per_customer
    FROM orders AS o
    INNER JOIN (
        SELECT id_order, SUM(quantity * price) AS total_per_order
        FROM order_items
        GROUP BY id_order
        ) AS agg1
    ON o.id_order = agg1.id_order
    GROUP BY o.id_customer
    ) AS agg2
ON c.id_customer = agg2.id_customer;

-- 9.1
SELECT
    CONCAT_WS(' ', c.first_name, c.last_name) As full_name,
    agg.nb_orders
FROM customers AS c
INNER JOIN (
    SELECT
        id_customer,
        COUNT(id_order) AS nb_orders
    FROM orders
    GROUP BY id_order
    ORDER BY nb_orders DESC
    LIMIT 5
    ) AS agg
ON c.id_customer = agg.id_customer;

-- 9.2
SELECT
    CONCAT_WS(' ', c.first_name, c.last_name) As full_name,
    agg2.total_per_customer
FROM customers AS c
INNER JOIN (
    SELECT
        o.id_customer,
        SUM(total_per_order) AS total_per_customer
    FROM orders AS o
    INNER JOIN (
        SELECT
            id_order,
            SUM(quantity * price) AS total_per_order
        FROM order_items
        GROUP BY id_order
        ) AS agg1
    ON o.id_order = agg1.id_order
    GROUP BY o.id_customer
    ORDER BY total_per_customer DESC
    LIMIT 5
    ) AS agg2
ON c.id_customer = agg2.id_customer;

-- 9.3
SELECT
    c.name_category,
    agg2.total_per_category
FROM categories AS c
INNER JOIN (
    SELECT
        p.id_category,
        SUM(agg1.total_per_product) AS total_per_category
    FROM products AS p
    INNER JOIN (
        SELECT
            id_product,
            SUM(quantity * price) AS total_per_product
        FROM order_items
        GROUP BY id_product
        ) AS agg1
    ON p.id_product = agg1.id_product
    GROUP BY p.id_category
    ORDER BY total_per_category DESC
    LIMIT 3
    ) AS agg2
ON c.id_category = agg2.id_category;

-- 9.4
SELECT
    p.name_product,
    agg.total_per_product
FROM products AS p
INNER JOIN (
    SELECT
        id_product,
        SUM(quantity * price) AS total_per_product
    FROM order_items
    GROUP BY id_product
    HAVING SUM(quantity * price) < 20
    ) AS agg
ON p.id_product = agg.id_product;

-- 9.5
SELECT
    CONCAT_WS(' ', c.first_name, c.last_name) AS full_name,
    agg.nb_orders
FROM customers AS c
INNER JOIN (
    SELECT
        id_customer,
        COUNT(id_order) AS nb_orders
    FROM orders
    GROUP BY id_customer
    ) AS agg
ON c.id_customer = agg.id_customer
WHERE nb_orders = 1;

-- 9.6
SELECT
    p.name_product,
    agg2.status_order,
    agg2.total_lost
FROM products AS p
INNER JOIN (
    SELECT
        oi.id_product,
        agg1.status_order,
        oi.quantity * oi.price AS total_lost
    FROM order_items AS oi
    INNER JOIN (
        SELECT id_order, status_order
        FROM orders
        WHERE status_order = 'CANCELLED'
        ) AS agg1
    ON oi.id_order = agg1.id_order
    ) AS agg2
ON p.id_product = agg2.id_product;