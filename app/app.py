import datetime
from pathlib import Path

import psycopg

DSN = "dbname=pgdb user=admin password=admin host=pgdb port=5432"


def init_db() -> None:
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS categories(
                        id_category uuid DEFAULT gen_random_uuid() PRIMARY KEY,
                        name_category VARCHAR(255) NOT NULL UNIQUE,
                        description_category TEXT
                    );
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS products(
                        id_product uuid DEFAULT gen_random_uuid() PRIMARY KEY,
                        name_product VARCHAR(255) NOT NULL,
                        price DECIMAL(10,2),
                        CONSTRAINT price_strictly_positive CHECK (price > 0),
                        stock INT,
                        CONSTRAINT stock_positive CHECK (stock >= 0),
                        id_category uuid NOT NULL,
                        CONSTRAINT fk_id_category FOREIGN KEY(id_category) REFERENCES categories(id_category)
                    );
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS customers(
                        id_customer uuid DEFAULT gen_random_uuid() PRIMARY KEY,
                        first_name VARCHAR(255) NOT NULL,
                        last_name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) NOT NULL UNIQUE,
                        registration_ts TIMESTAMP NOT NULL
                    );
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS orders(
                        id_order uuid DEFAULT gen_random_uuid() PRIMARY KEY,
                        order_ts TIMESTAMP NOT NULL,
                        status_order VARCHAR(255) NOT NULL,
                        CONSTRAINT status_order_enum CHECK (status_order in ('PENDING', 'PAID', 'SHIPPED', 'CANCELLED')),
                        id_customer uuid NOT NULL,
                        CONSTRAINT fk_id_customer FOREIGN KEY(id_customer) REFERENCES customers(id_customer)
                    );
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS order_items(
                        id_order_item uuid DEFAULT gen_random_uuid() PRIMARY KEY,
                        id_product uuid,
                        CONSTRAINT kf_id_product FOREIGN KEY(id_product) REFERENCES products(id_product),
                        id_order uuid,
                        CONSTRAINT kf_id_order FOREIGN KEY(id_order) REFERENCES orders(id_order),
                        quantity INT NOT NULL,
                        CONSTRAINT quantity_strictly_positive CHECK (quantity > 0),
                        price DECIMAL(10,2),
                        CONSTRAINT price_strictly_positive CHECK (price > 0)
                    );
                    """
                )
    except Exception as e:
        print(e)


def insert_data() -> None:
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO categories(name_category, description_category) VALUES
                    ('Électronique','Produits high-tech et accessoires'),
                    ('Maison & Cuisine','Électroménager et ustensiles'),
                    ('Sport & Loisirs','Articles de sport et plein air'),
                    ('Beauté & Santé','Produits de beauté, hygiène, bien-être'),
                    ('Jeux & Jouets','Jouets pour enfants et adultes');
                    """
                )
                cursor.execute(
                    """
                    INSERT INTO products(name_product, price, stock, id_category) VALUES
                    ('Casque Bluetooth X1000',79.99,50,(SELECT id_category FROM categories WHERE name_category='Électronique')),
                    ('Souris Gamer Pro RGB',49.90,120,(SELECT id_category FROM categories WHERE name_category='Électronique')),
                    ('Bouilloire Inox 1.7L',29.99,80,(SELECT id_category FROM categories WHERE name_category='Maison & Cuisine')),
                    ('Aspirateur Cyclonix 3000',129.00,40,(SELECT id_category FROM categories WHERE name_category='Maison & Cuisine')),
                    ('Tapis de Yoga Comfort+',19.99,150,(SELECT id_category FROM categories WHERE name_category='Sport & Loisirs')),
                    ('Haltères 5kg (paire)',24.99,70,(SELECT id_category FROM categories WHERE name_category='Sport & Loisirs')),
                    ('Crème hydratante BioSkin',15.90,200,(SELECT id_category FROM categories WHERE name_category='Beauté & Santé')),
                    ('Gel douche FreshEnergy',4.99,300,(SELECT id_category FROM categories WHERE name_category='Beauté & Santé')),
                    ('Puzzle 1000 pièces "Montagne"',12.99,95,(SELECT id_category FROM categories WHERE name_category='Jeux & Jouets')),
                    ('Jeu de société "Galaxy Quest"',29.90,60,(SELECT id_category FROM categories WHERE name_category='Jeux & Jouets'));
                    """
                )
                cursor.execute(
                    """
                    INSERT INTO customers(first_name, last_name, email, registration_ts) VALUES
                    ('Alice','Martin','alice.martin@mail.com','2024-01-10 14:32'),
                    ('Bob','Dupont','bob.dupont@mail.com','2024-02-05 09:10'),
                    ('Chloé','Bernard','chloe.bernard@mail.com','2024-03-12 17:22'),
                    ('David','Robert','david.robert@mail.com','2024-01-29 11:45'),
                    ('Emma','Leroy','emma.leroy@mail.com','2024-03-02 08:55'),
                    ('Félix','Petit','felix.petit@mail.com','2024-02-18 16:40'),
                    ('Hugo','Roussel','hugo.roussel@mail.com','2024-03-20 19:05'),
                    ('Inès','Moreau','ines.moreau@mail.com','2024-01-17 10:15'),
                    ('Julien','Fontaine','julien.fontaine@mail.com','2024-01-23 13:55'),
                    ('Katia','Garnier','katia.garnier@mail.com','2024-03-15 12:00');
                    """
                )
                cursor.execute(
                    """
                    INSERT INTO orders(id_customer, order_ts, status_order) VALUES
                    ((SELECT id_customer FROM customers WHERE email='alice.martin@mail.com'),'2024-03-01 10:20','PAID'),
                    ((SELECT id_customer FROM customers WHERE email='bob.dupont@mail.com'),'2024-03-04 09:12','SHIPPED'),
                    ((SELECT id_customer FROM customers WHERE email='chloe.bernard@mail.com'),'2024-03-08 15:02','PAID'),
                    ((SELECT id_customer FROM customers WHERE email='david.robert@mail.com'),'2024-03-09 11:45','CANCELLED'),
                    ((SELECT id_customer FROM customers WHERE email='emma.leroy@mail.com'),'2024-03-10 08:10','PAID'),
                    ((SELECT id_customer FROM customers WHERE email='felix.petit@mail.com'),'2024-03-11 13:50','PENDING'),
                    ((SELECT id_customer FROM customers WHERE email='hugo.roussel@mail.com'),'2024-03-15 19:30','SHIPPED'),
                    ((SELECT id_customer FROM customers WHERE email='ines.moreau@mail.com'),'2024-03-16 10:00','PAID'),
                    ((SELECT id_customer FROM customers WHERE email='julien.fontaine@mail.com'),'2024-03-18 14:22','PAID'),
                    ((SELECT id_customer FROM customers WHERE email='katia.garnier@mail.com'),'2024-03-20 18:00','PENDING');
                    """
                )
                cursor.execute(
                    """
                    INSERT INTO order_items(id_order, id_product, quantity, price) VALUES
                    ((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='alice.martin@mail.com') AND order_ts='2024-03-01 10:20'),(SELECT id_product FROM products WHERE name_product='Casque Bluetooth X1000' LIMIT 1),1,79.99),
                    ((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='alice.martin@mail.com') AND order_ts='2024-03-01 10:20'),(SELECT id_product FROM products WHERE name_product='Puzzle 1000 pièces "Montagne"' LIMIT 1),2,12.99),
                    ((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='bob.dupont@mail.com') AND order_ts='2024-03-04 09:12'),(SELECT id_product FROM products WHERE name_product='Tapis de Yoga Comfort+' LIMIT 1),1,19.99),
                    ((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='chloe.bernard@mail.com') AND order_ts='2024-03-08 15:02'),(SELECT id_product FROM products WHERE name_product='Bouilloire Inox 1.7L' LIMIT 1),1,29.99),
                    ((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='chloe.bernard@mail.com') AND order_ts='2024-03-08 15:02'),(SELECT id_product FROM products WHERE name_product='Gel douche FreshEnergy' LIMIT 1),3,4.99),
                    ((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='david.robert@mail.com') AND order_ts='2024-03-09 11:45'),(SELECT id_product FROM products WHERE name_product='Haltères 5kg (paire)' LIMIT 1),1,24.99),
                    ((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='emma.leroy@mail.com') AND order_ts='2024-03-10 08:10'),(SELECT id_product FROM products WHERE name_product='Crème hydratante BioSkin' LIMIT 1),2,15.90),
                    ((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='julien.fontaine@mail.com') AND order_ts='2024-03-18 14:22'),(SELECT id_product FROM products WHERE name_product='Jeu de société "Galaxy Quest"' LIMIT 1),1,29.90),
                    ((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='katia.garnier@mail.com') AND order_ts='2024-03-20 18:00'),(SELECT id_product FROM products WHERE name_product='Souris Gamer Pro RGB' LIMIT 1),1,49.90),
                    ((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='katia.garnier@mail.com') AND order_ts='2024-03-20 18:00'),(SELECT id_product FROM products WHERE name_product='Gel douche FreshEnergy' LIMIT 1),2,4.99);
                    """
                )
    except Exception as e:
        print(e)


def select_most_active_customers() -> list[dict]:
    try:
        with psycopg.connect(DSN, row_factory=psycopg.rows.dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        CONCAT_WS(' ', c.first_name, c.last_name) As full_name
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
                    """
                )
                return cursor.fetchall()
    except Exception as e:
        print(e)


def metric_most_active_customers(file_path: Path) -> None:
    texts: list[str] = []
    query_results: list[dict] = select_most_active_customers()
    texts.append("List des 5 clients les plus actifs :")
    if query_results:
        for k, query_result in enumerate(query_results, start=1):
            texts.append(f"{k}. {query_result['full_name']}")
    texts.append("\n")

    write_report(file_path=file_path, text="\n".join(texts))


def select_biggest_spenders() -> dict:
    try:
        with psycopg.connect(DSN, row_factory=psycopg.rows.dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
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
                    """
                )
                return cursor.fetchall()
    except Exception as e:
        print(e)


def metric_biggest_spenders(file_path: Path) -> None:
    texts: list[str] = []
    query_results: list[dict] = select_biggest_spenders()
    texts.append("List des 5 clients les plus dépensiers :")
    if query_results:
        for k, query_result in enumerate(query_results, start=1):
            texts.append(
                f"{k}. {query_result['full_name']} - {query_result['total_per_customer']}€"
            )
    texts.append("\n")

    write_report(file_path=file_path, text="\n".join(texts))


def select_most_profitable_categories() -> dict:
    try:
        with psycopg.connect(DSN, row_factory=psycopg.rows.dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
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
                    """
                )
                return cursor.fetchall()
    except Exception as e:
        print(e)


def metric_most_profitable_categories(file_path: Path) -> None:
    texts: list[str] = []
    query_results: list[dict] = select_most_profitable_categories()
    texts.append("List des 3 catégories les plus rentables :")
    if query_results:
        for k, query_result in enumerate(query_results, start=1):
            texts.append(
                f"{k}. {query_result['name_category']} - {query_result['total_per_category']}€"
            )
    texts.append("\n")

    write_report(file_path=file_path, text="\n".join(texts))


def select_CA_products_minus_20() -> dict:
    try:
        with psycopg.connect(DSN, row_factory=psycopg.rows.dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
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
                        ORDER BY total_per_product
                        ) AS agg
                    ON p.id_product = agg.id_product;
                    """
                )
                return cursor.fetchall()
    except Exception as e:
        print(e)


def metric_CA_products_minus_20(file_path: Path) -> None:
    texts: list[str] = []
    query_results: list[dict] = select_CA_products_minus_20()
    texts.append("List des produits ayant générés moins de 20€ :")
    if query_results:
        for k, query_result in enumerate(query_results, start=1):
            texts.append(
                f"{k}. {query_result['name_product']} - {query_result['total_per_product']}€"
            )
    texts.append("\n")

    write_report(file_path=file_path, text="\n".join(texts))


def select_customers_one_order() -> dict:
    try:
        with psycopg.connect(DSN, row_factory=psycopg.rows.dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        CONCAT_WS(' ', c.first_name, c.last_name) AS full_name
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
                    """
                )
                return cursor.fetchall()
    except Exception as e:
        print(e)


def metric_customers_one_order(file_path: Path) -> None:
    texts: list[str] = []
    query_results: list[dict] = select_customers_one_order()
    texts.append("List des clients n'ayant passé qu'une commande :")
    if query_results:
        for k, query_result in enumerate(query_results, start=1):
            texts.append(f"{k}. {query_result['full_name']}")
    texts.append("\n")

    write_report(file_path=file_path, text="\n".join(texts))


def select_amount_lost_cancelled_orders_per_product() -> dict:
    try:
        with psycopg.connect(DSN, row_factory=psycopg.rows.dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        p.name_product,
                        agg2.total_lost
                    FROM products AS p
                    INNER JOIN (
                        SELECT
                            oi.id_product,
                            oi.quantity * oi.price AS total_lost
                        FROM order_items AS oi
                        INNER JOIN (
                            SELECT id_order
                            FROM orders
                            WHERE status_order = 'CANCELLED'
                            ) AS agg1
                        ON oi.id_order = agg1.id_order
                        ORDER BY total_lost DESC
                        ) AS agg2
                    ON p.id_product = agg2.id_product;
                    """
                )
                return cursor.fetchall()
    except Exception as e:
        print(e)


def metric_amount_lost_cancelled_orders_per_product(file_path: Path) -> None:
    texts: list[str] = []
    query_results: list[dict] = select_amount_lost_cancelled_orders_per_product()
    texts.append('Montant perdu par produit présent dans les commandes "annulées" :')
    if query_results:
        for k, query_result in enumerate(query_results, start=1):
            texts.append(
                f"{k}. {query_result['total_lost']}€ - {query_result['name_product']}"
            )
    texts.append("\n")

    write_report(file_path=file_path, text="\n".join(texts))


def write_report(file_path: Path, text: str) -> None:
    with open(file_path, "at", encoding="utf-8") as f:
        f.write(text)


def compute_top_report(file_path: Path) -> None:
    texts: list[str] = []
    texts.append("Rapport Supershop - Analyse des ventes")
    texts.append(
        f"Généré le : {datetime.datetime.today().__format__('%Y-%M-%d %H-%m%S')}"
    )
    texts.append("")
    write_report(file_path=file_path, text="\n".join(texts))


def compute_report(file_path: Path) -> None:
    compute_top_report(file_path=file_path)

    metrics = [
        metric_most_active_customers,
        metric_biggest_spenders,
        metric_most_profitable_categories,
        metric_CA_products_minus_20,
        metric_customers_one_order,
        metric_amount_lost_cancelled_orders_per_product,
    ]

    for metric in metrics:
        metric(file_path=file_path)


def main():
    # init_db()
    # insert_data()
    file_path = Path(
        f"/app/reports/report_{datetime.datetime.today().__format__('%Y%M%d_%H%m%S')}.txt"
    )
    compute_report(file_path=file_path)


if __name__ == "__main__":
    main()
