import datetime
import os
from pathlib import Path
from zoneinfo import ZoneInfo

import psycopg

dbname = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = "pgdb"
port = "5432"

DSN = f"postgres://{user}:{password}@{host}:{port}/{dbname}"


def run_query(query: str) -> list[dict]:
    try:
        with psycopg.connect(DSN, row_factory=psycopg.rows.dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
    except Exception as e:
        print(e)


def metric_most_active_customers(file_path: Path) -> None:
    texts: list[str] = []
    query = """
        SELECT
            CONCAT_WS(' ', c.first_name, c.last_name) As full_name,
            COUNT(o.id_order) AS nb_orders
        FROM customers AS c
        INNER JOIN orders AS o ON c.id_customer = o.id_customer
        GROUP BY c.id_customer, full_name
        ORDER BY nb_orders DESC
        LIMIT 5;
        """
    query_results: list[dict] = run_query(query=query)
    texts.append("Liste des 5 clients les plus actifs :")
    if query_results:
        for k, query_result in enumerate(query_results, start=1):
            texts.append(
                f"{k}. {query_result['full_name']} - {query_result['nb_orders']} commandes"
            )
    texts.append("\n")

    write_report(file_path=file_path, text="\n".join(texts))


def metric_biggest_spenders(file_path: Path) -> None:
    texts: list[str] = []
    query = """
        SELECT
            CONCAT_WS(' ', c.first_name, c.last_name) As full_name,
            SUM(oi.quantity * oi.price) AS total_spent
        FROM customers AS c
        JOIN orders AS o ON o.id_customer = c.id_customer
        JOIN order_items AS oi ON oi.id_order = o.id_order
        WHERE o.status_order <> 'CANCELLED'
        GROUP BY c.id_customer, full_name
        ORDER BY total_spent DESC
        LIMIT 5;
        """
    query_results: list[dict] = run_query(query=query)
    texts.append("Liste des 5 clients les plus dépensiers :")
    if query_results:
        for k, query_result in enumerate(query_results, start=1):
            texts.append(
                f"{k}. {query_result['full_name']} - {query_result['total_spent']}€"
            )
    texts.append("\n")

    write_report(file_path=file_path, text="\n".join(texts))


def metric_most_profitable_categories(file_path: Path) -> None:
    texts: list[str] = []
    query = """
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
        """
    query_results: list[dict] = run_query(query=query)
    texts.append("Liste des 3 catégories les plus rentables :")
    if query_results:
        for k, query_result in enumerate(query_results, start=1):
            texts.append(
                f"{k}. {query_result['name_category']} - {query_result['category_revenue']}€"
            )
    texts.append("\n")

    write_report(file_path=file_path, text="\n".join(texts))


def metric_CA_products_minus_20(file_path: Path) -> None:
    texts: list[str] = []
    query = """
        SELECT
            p.name_product,
            SUM(oi.quantity * oi.price) AS total_revenue
        FROM products AS p
        LEFT JOIN order_items AS oi ON oi.id_product = p.id_product
        LEFT JOIN orders AS o ON o.id_order = oi.id_order
        WHERE o.status_order <> 'CANCELLED'
        GROUP BY p.id_product, p.name_product
        HAVING SUM(oi.quantity * oi.price) < 20
        ORDER BY total_revenue ASC;
        """
    query_results: list[dict] = run_query(query=query)
    texts.append("Liste des produits ayant générés moins de 20€ :")
    if query_results:
        for k, query_result in enumerate(query_results, start=1):
            texts.append(
                f"{k}. {query_result['name_product']} - {query_result['total_revenue']}€"
            )
    texts.append("\n")

    write_report(file_path=file_path, text="\n".join(texts))


def metric_customers_one_order(file_path: Path) -> None:
    texts: list[str] = []
    query = """
        SELECT
            CONCAT_WS(' ', c.first_name, c.last_name) As full_name
        FROM customers AS c
        JOIN orders AS o ON o.id_customer = c.id_customer
        GROUP BY c.id_customer, full_name
        HAVING COUNT(o.id_order) = 1
        ORDER BY full_name;
        """
    query_results: list[dict] = run_query(query=query)
    texts.append("Liste des clients n'ayant passé qu'une commande :")
    if query_results:
        for k, query_result in enumerate(query_results, start=1):
            texts.append(f"{k}. {query_result['full_name']}")
    texts.append("\n")

    write_report(file_path=file_path, text="\n".join(texts))


def metric_amount_lost_cancelled_orders_per_product(file_path: Path) -> None:
    texts: list[str] = []
    query = """
        SELECT
            p.name_product,
            SUM(oi.quantity * oi.price) AS total_lost
        FROM order_items AS oi
        INNER JOIN products AS p ON oi.id_product = p.id_product
        INNER JOIN orders AS o ON oi.id_order = o.id_order
        WHERE status_order = 'CANCELLED'
        GROUP BY p.name_product
        ORDER BY total_lost DESC;
        """
    query_results: list[dict] = run_query(query=query)
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


def compute_top_report(file_path: Path, ts: datetime.datetime) -> None:
    texts: list[str] = []
    texts.append("Rapport Supershop - Analyse des ventes")
    texts.append(f"Généré le : {ts.__format__('%Y-%m-%d %H-%M%S')}")
    texts.append("\n")
    write_report(file_path=file_path, text="\n".join(texts))


def compute_report(file_path: Path, ts: datetime.datetime) -> None:
    compute_top_report(file_path=file_path, ts=ts)

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
    ts = datetime.datetime.now(ZoneInfo("Europe/Paris"))
    reports_dir = Path("/app/reports")
    if not reports_dir.exists():
        os.mkdir(reports_dir)
    file_path = reports_dir.joinpath(f"report_{ts.__format__('%Y%m%d_%H%M%S')}.txt")
    compute_report(file_path=file_path, ts=ts)


if __name__ == "__main__":
    main()
