import pandas as pd

from config import SOURCE_DIR


def main() -> None:
    source_path = SOURCE_DIR / "olist_orders_dataset.csv"

    orders = pd.read_csv(
        source_path,
        parse_dates=["order_purchase_timestamp"],
    )

    cutoff_date = orders["order_purchase_timestamp"].quantile(0.90)

    historical = orders[
        orders["order_purchase_timestamp"] <= cutoff_date
    ].copy()

    incremental = orders[
        orders["order_purchase_timestamp"] > cutoff_date
    ].copy()

    historical.to_csv(
        SOURCE_DIR / "orders_historical.csv",
        index=False,
    )

    incremental.to_csv(
        SOURCE_DIR / "orders_incremental.csv",
        index=False,
    )

    print(f"Historical rows: {len(historical):,}")
    print(f"Incremental rows: {len(incremental):,}")
    print(f"Cutoff date: {cutoff_date}")


if __name__ == "__main__":
    main()