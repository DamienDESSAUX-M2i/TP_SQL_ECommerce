import datetime
import os
from pathlib import Path

import psycopg

dbname = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = "pgdb"
port = "5432"

DSN = f"postgres://{user}:{password}@{host}:{port}/{dbname}"


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
    texts.append("Liste des 5 clients les plus actifs :")
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
    texts.append("Liste des 5 clients les plus dépensiers :")
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
    texts.append("Liste des 3 catégories les plus rentables :")
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
    texts.append("Liste des produits ayant générés moins de 20€ :")
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
    texts.append("Liste des clients n'ayant passé qu'une commande :")
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
    texts.append("\n")
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
    file_path = Path(
        f"/app/reports/report_{datetime.datetime.today().__format__('%Y%M%d_%H%m%S')}.txt"
    )
    compute_report(file_path=file_path)


if __name__ == "__main__":
    main()
