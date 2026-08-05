import pandas as pd

from config import BRONZE_DIR, SILVER_DIR
from data_quality import (
    remove_duplicates,
    save_rejected_records,
    validate_not_null,
)


DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


def main() -> None:
    input_path = BRONZE_DIR / "olist_orders.parquet"

    orders = pd.read_parquet(input_path)

    orders = remove_duplicates(orders, ["order_id"])

    orders, rejected_orders = validate_not_null(
        orders,
        ["order_id", "customer_id", "order_status"],
    )

    for column in DATE_COLUMNS:
        orders[column] = pd.to_datetime(
            orders[column],
            errors="coerce",
        )

    orders["order_status"] = (
        orders["order_status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    orders["delivery_days"] = (
        orders["order_delivered_customer_date"]
        - orders["order_purchase_timestamp"]
    ).dt.days

    orders["is_late_delivery"] = (
        orders["order_delivered_customer_date"]
        > orders["order_estimated_delivery_date"]
    ).astype("int8")

    orders.to_parquet(
        SILVER_DIR / "orders.parquet",
        index=False,
    )

    save_rejected_records(
        rejected_orders,
        SILVER_DIR / "rejected_orders.parquet",
    )

    print(f"Silver orders created: {len(orders):,} records")
    print(f"Rejected orders: {len(rejected_orders):,} records")


if __name__ == "__main__":
    main()