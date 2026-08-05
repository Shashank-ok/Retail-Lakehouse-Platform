import pandas as pd

from config import SILVER_DIR, GOLD_DIR


def main() -> None:
    orders = pd.read_parquet(
        SILVER_DIR / "orders.parquet"
    )

    order_items = pd.read_parquet(
        SILVER_DIR / "order_items.parquet"
    )

    dim_customer = pd.read_parquet(
        GOLD_DIR / "dim_customer.parquet"
    )

    dim_product = pd.read_parquet(
        GOLD_DIR / "dim_product.parquet"
    )

    dim_seller = pd.read_parquet(
        GOLD_DIR / "dim_seller.parquet"
    )

    fact_sales = order_items.merge(
        orders[
            [
                "order_id",
                "customer_id",
                "order_status",
                "order_purchase_timestamp",
                "delivery_days",
                "is_late_delivery",
            ]
        ],
        on="order_id",
        how="inner",
        validate="many_to_one",
    )

    fact_sales = fact_sales.merge(
        dim_customer[["customer_id", "customer_key"]],
        on="customer_id",
        how="left",
        validate="many_to_one",
    )

    fact_sales = fact_sales.merge(
        dim_product[["product_id", "product_key"]],
        on="product_id",
        how="left",
        validate="many_to_one",
    )

    fact_sales = fact_sales.merge(
        dim_seller[["seller_id", "seller_key"]],
        on="seller_id",
        how="left",
        validate="many_to_one",
    )

    fact_sales["date_key"] = (
        fact_sales["order_purchase_timestamp"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    fact_sales = fact_sales.reset_index(drop=True)
    fact_sales.insert(0, "sales_key", fact_sales.index + 1)

    fact_sales = fact_sales[
        [
            "sales_key",
            "order_id",
            "order_item_id",
            "customer_key",
            "product_key",
            "seller_key",
            "date_key",
            "order_status",
            "price",
            "freight_value",
            "total_item_value",
            "delivery_days",
            "is_late_delivery",
        ]
    ]

    null_keys = fact_sales[
        ["customer_key", "product_key", "seller_key", "date_key"]
    ].isnull().sum()

    print("Null foreign keys:")
    print(null_keys)

    fact_sales.to_parquet(
        GOLD_DIR / "fact_sales.parquet",
        index=False,
    )

    print(f"fact_sales created: {len(fact_sales):,} records")


if __name__ == "__main__":
    main()