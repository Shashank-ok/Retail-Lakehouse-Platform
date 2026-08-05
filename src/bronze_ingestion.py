from datetime import datetime, timezone
from pathlib import Path
import uuid

import pandas as pd

from config import SOURCE_DIR, BRONZE_DIR


def ingest_csv_to_bronze(file_path: Path) -> None:
    """Read a source CSV and store it as a Bronze-layer Parquet file."""

    print(f"Ingesting {file_path.name}")

    dataframe = pd.read_csv(file_path)

    dataframe["_source_file"] = file_path.name
    dataframe["_ingestion_timestamp"] = datetime.now(timezone.utc)
    dataframe["_pipeline_run_id"] = str(uuid.uuid4())

    output_name = file_path.stem.replace("_dataset", "")
    output_path = BRONZE_DIR / f"{output_name}.parquet"

    dataframe.to_parquet(output_path, index=False)

    print(
        f"Created {output_path.name}: "
        f"{len(dataframe):,} rows and {len(dataframe.columns)} columns"
    )


def main() -> None:
    csv_files = list(SOURCE_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {SOURCE_DIR}. "
            "Place the source files in the data/source directory."
        )

    for csv_file in csv_files:
        ingest_csv_to_bronze(csv_file)


if __name__ == "__main__":
    main()