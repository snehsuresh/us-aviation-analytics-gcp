import pandas as pd

# === Input & Output Paths ===
input_path = "/Users/snehsuresh/Desktop/Projects/aviation_data_projects/data/raw/raw_airline_data.csv"
output_path = "/Users/snehsuresh/Desktop/Projects/aviation_data_projects/data/raw/raw_airline_data_sorted.csv"


def main():
    print("📂 Loading raw_airline_data.csv...")
    df = pd.read_csv(input_path)

    print("🔢 Sorting by YEAR and QUARTER...")
    df["YEAR"] = df["YEAR"].astype(int)
    df["QUARTER"] = df["QUARTER"].astype(int)
    df_sorted = df.sort_values(by=["YEAR", "QUARTER"])

    df_sorted.to_csv(output_path, index=False)
    print(f"✅ Sorted file saved to: {output_path}")


if __name__ == "__main__":
    main()
