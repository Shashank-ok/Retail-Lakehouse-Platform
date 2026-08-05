import pandas as pd

from config import BRONZE_DIR, SILVER_DIR
from data_quality import remove_duplicates, validate_not_null


def main() -> None:
    order_items = pd.read_parquet(
        BRONZE_DIR / "olist_order_items.parquet"
    )

    order_items = remove_duplicates(
        order_items,
        ["order_id", "order_item_id"],
    )

    order_items, rejected = validate_not_null(
        order_items,
        ["order_id", "order_item_id", "product_id", "seller_id"],
    )

    order_items["shipping_limit_date"] = pd.to_datetime(
        order_items["shipping_limit_date"],
        errors="coerce",
    )

    order_items["price"] = pd.to_numeric(
        order_items["price"],
        errors="coerce",
    )

    order_items["freight_value"] = pd.to_numeric(
        order_items["freight_value"],
        errors="coerce",
    )

    order_items = order_items[
        (order_items["price"] >= 0)
        & (order_items["freight_value"] >= 0)
    ].copy()

    order_items["total_item_value"] = (
        order_items["price"] + order_items["freight_value"]
    )

    order_items.to_parquet(
        SILVER_DIR / "order_items.parquet",
        index=False,
    )

    print(f"Silver order items created: {len(order_items):,} records")


if __name__ == "__main__":
    main()
    