import subprocess
import sys


SCRIPTS = [
    "src/silver_customers.py",
    "src/silver_orders.py",
    "src/silver_order_items.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"Running {script}")

        result = subprocess.run(
            [sys.executable, script],
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Pipeline failed at {script}")

    print("Silver pipeline completed successfully.")


if __name__ == "__main__":
    main()