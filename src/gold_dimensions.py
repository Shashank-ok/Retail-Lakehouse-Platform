import pandas as pd

from config import BRONZE_DIR, SILVER_DIR, GOLD_DIR


def create_customer_dimension() -> pd.DataFrame:
    customers = pd.read_parquet(
        SILVER_DIR / "customers.parquet"
    )

    dimension = customers[
        [
            "customer_id",
            "customer_unique_id",
            "customer_city",
            "customer_state",
            "customer_zip_code_prefix",
        ]
    ].copy()

    dimension = dimension.reset_index(drop=True)
    dimension.insert(0, "customer_key", dimension.index + 1)

    return dimension


def create_product_dimension() -> pd.DataFrame:
    products = pd.read_parquet(
        BRONZE_DIR / "olist_products.parquet"
    )

    selected_columns = [
        "product_id",
        "product_category_name",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]

    dimension = products[selected_columns].copy()

    dimension = dimension.drop_duplicates(
        subset=["product_id"],
        keep="last",
    )

    dimension["product_category_name"] = (
        dimension["product_category_name"]
        .fillna("unknown")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    dimension = dimension.reset_index(drop=True)
    dimension.insert(0, "product_key", dimension.index + 1)

    return dimension


def create_seller_dimension() -> pd.DataFrame:
    sellers = pd.read_parquet(
        BRONZE_DIR / "olist_sellers.parquet"
    )

    dimension = sellers[
        [
            "seller_id",
            "seller_city",
            "seller_state",
            "seller_zip_code_prefix",
        ]
    ].copy()

    dimension = dimension.drop_duplicates(
        subset=["seller_id"],
        keep="last",
    )

    dimension["seller_city"] = (
        dimension["seller_city"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    dimension["seller_state"] = (
        dimension["seller_state"]
        .astype(str)
        .str.upper()
    )

    dimension = dimension.reset_index(drop=True)
    dimension.insert(0, "seller_key", dimension.index + 1)

    return dimension


def create_date_dimension() -> pd.DataFrame:
    orders = pd.read_parquet(
        SILVER_DIR / "orders.parquet"
    )

    start_date = orders["order_purchase_timestamp"].min().normalize()
    end_date = orders["order_purchase_timestamp"].max().normalize()

    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    dimension = pd.DataFrame({"full_date": dates})

    dimension["date_key"] = (
        dimension["full_date"].dt.strftime("%Y%m%d").astype(int)
    )
    dimension["year"] = dimension["full_date"].dt.year
    dimension["quarter"] = dimension["full_date"].dt.quarter
    dimension["month_number"] = dimension["full_date"].dt.month
    dimension["month_name"] = dimension["full_date"].dt.month_name()
    dimension["day"] = dimension["full_date"].dt.day
    dimension["day_name"] = dimension["full_date"].dt.day_name()
    dimension["is_weekend"] = (
        dimension["full_date"].dt.dayofweek >= 5
    ).astype("int8")

    return dimension[
        [
            "date_key",
            "full_date",
            "year",
            "quarter",
            "month_number",
            "month_name",
            "day",
            "day_name",
            "is_weekend",
        ]
    ]


def main() -> None:
    dimensions = {
        "dim_customer": create_customer_dimension(),
        "dim_product": create_product_dimension(),
        "dim_seller": create_seller_dimension(),
        "dim_date": create_date_dimension(),
    }

    for table_name, dataframe in dimensions.items():
        dataframe.to_parquet(
            GOLD_DIR / f"{table_name}.parquet",
            index=False,
        )

        print(f"{table_name}: {len(dataframe):,} records")


if __name__ == "__main__":
    main()