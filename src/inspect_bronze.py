import pandas as pd

from config import BRONZE_DIR


def main() -> None:
    for file_path in BRONZE_DIR.glob("*.parquet"):
        dataframe = pd.read_parquet(file_path)

        print("=" * 80)
        print(file_path.name)
        print(f"Rows: {len(dataframe):,}")
        print(f"Columns: {len(dataframe.columns)}")
        print(dataframe.head())


if __name__ == "__main__":
    main()
    