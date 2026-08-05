import pandas as pd

from config import BRONZE_DIR, SILVER_DIR
from data_quality import remove_duplicates, validate_not_null


def main() -> None:
    customers = pd.read_parquet(
        BRONZE_DIR / "olist_customers.parquet"
    )

    customers = remove_duplicates(customers, ["customer_id"])

    customers, rejected_customers = validate_not_null(
        customers,
        ["customer_id", "customer_unique_id"],
    )

    customers["customer_city"] = (
        customers["customer_city"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    customers["customer_state"] = (
        customers["customer_state"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    customers.to_parquet(
        SILVER_DIR / "customers.parquet",
        index=False,
    )

    if not rejected_customers.empty:
        rejected_customers.to_parquet(
            SILVER_DIR / "rejected_customers.parquet",
            index=False,
        )

    print(f"Silver customers created: {len(customers):,} records")


if __name__ == "__main__":
    main()
    