import pandas as pd

from config import GOLD_DIR


def main() -> None:
    for file_path in GOLD_DIR.glob("*.parquet"):
        dataframe = pd.read_parquet(file_path)

        print("=" * 80)
        print(f"File: {file_path.name}")
        print(f"Rows: {len(dataframe):,}")
        print("Columns:")
        print(dataframe.columns.tolist())
        print(dataframe.head(3))


if __name__ == "__main__":
    main()