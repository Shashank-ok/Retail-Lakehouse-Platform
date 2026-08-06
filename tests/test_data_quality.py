import pandas as pd

from src.data_quality import remove_duplicates, validate_not_null


def test_remove_duplicates() -> None:
    dataframe = pd.DataFrame(
        {
            "order_id": ["A", "A", "B"],
            "value": [100, 200, 300],
        }
    )

    result = remove_duplicates(dataframe, ["order_id"])

    assert len(result) == 2
    assert result.loc[result["order_id"] == "A", "value"].iloc[0] == 200


def test_validate_not_null() -> None:
    dataframe = pd.DataFrame(
        {
            "order_id": ["A", None, "C"],
            "customer_id": ["X", "Y", "Z"],
        }
    )

    valid, rejected = validate_not_null(
        dataframe,
        ["order_id", "customer_id"],
    )

    assert len(valid) == 2
    assert len(rejected) == 1