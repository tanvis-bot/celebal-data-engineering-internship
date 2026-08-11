from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "source"

files = [
    "patients.csv",
    "doctors.csv",
    "appointments.csv",
    "treatments.csv",
    "billing.csv"
]

for file in files:
    df = pd.read_csv(SOURCE / file)

    print("\n", "=" * 70)
    print(file)
    print("=" * 70)

    print("Shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nNulls:")
    print(df.isnull().sum())

    print("\nDuplicates:")
    print(df.duplicated().sum())

    print("\nDtypes:")
    print(df.dtypes)