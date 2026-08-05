import json
from datetime import timezone
from pathlib import Path

import pandas as pd

from config import SOURCE_DIR, BRONZE_DIR


WATERMARK_FILE = Path("data") / "watermark.json"
OUTPUT_FILE = BRONZE_DIR / "orders_incremental.parquet"


def read_watermark() -> pd.Timestamp:
    with WATERMARK_FILE.open("r", encoding="utf-8") as file:
        watermarks = json.load(file)

    return pd.Timestamp(watermarks["orders"], tz="UTC")


def update_watermark(timestamp: pd.Timestamp) -> None:
    watermark_value = timestamp.isoformat()

    with WATERMARK_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            {"orders": watermark_value},
            file,
            indent=2,
        )


def main() -> None:
    current_watermark = read_watermark()

    incoming = pd.read_csv(
        SOURCE_DIR / "orders_incremental.csv",
        parse_dates=["order_purchase_timestamp"],
    )

    incoming["order_purchase_timestamp"] = pd.to_datetime(
        incoming["order_purchase_timestamp"],
        utc=True,
    )

    new_records = incoming[
        incoming["order_purchase_timestamp"] > current_watermark
    ].copy()

    if new_records.empty:
        print("No new records found.")
        return

    if OUTPUT_FILE.exists():
        existing = pd.read_parquet(OUTPUT_FILE)

        combined = pd.concat(
            [existing, new_records],
            ignore_index=True,
        )

        combined = combined.drop_duplicates(
            subset=["order_id"],
            keep="last",
        )
    else:
        combined = new_records

    combined.to_parquet(OUTPUT_FILE, index=False)

    new_watermark = new_records[
        "order_purchase_timestamp"
    ].max()

    update_watermark(new_watermark)

    print(f"New records processed: {len(new_records):,}")
    print(f"Updated watermark: {new_watermark}")


if __name__ == "__main__":
    main()