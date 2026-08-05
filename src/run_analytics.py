import duckdb

from config import GOLD_DIR


def main() -> None:
    fact_path = str(GOLD_DIR / "fact_sales.parquet")
    date_path = str(GOLD_DIR / "dim_date.parquet")
    product_path = str(GOLD_DIR / "dim_product.parquet")

    connection = duckdb.connect()

    monthly_sales_query = f"""
        SELECT
            d.year,
            d.month_number,
            d.month_name,
            COUNT(DISTINCT f.order_id) AS total_orders,
            ROUND(SUM(f.total_item_value), 2) AS total_revenue,
            ROUND(AVG(f.total_item_value), 2) AS average_item_value,
            ROUND(
                100.0 * AVG(f.is_late_delivery),
                2
            ) AS late_delivery_percentage
        FROM read_parquet('{fact_path}') AS f
        JOIN read_parquet('{date_path}') AS d
            ON f.date_key = d.date_key
        GROUP BY
            d.year,
            d.month_number,
            d.month_name
        ORDER BY
            d.year,
            d.month_number
    """

    result = connection.execute(monthly_sales_query).fetchdf()

    print(result.head(20))

    result.to_csv(
        GOLD_DIR / "monthly_sales_summary.csv",
        index=False,
    )


if __name__ == "__main__":
    main()