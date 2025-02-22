import os
import zipfile
import pandas as pd
from tqdm import tqdm

t100_zip_dir = (
    "/Users/snehsuresh/Desktop/Projects/aviation_data_projects/data/raw/t100_pending"
)
merged_csv = "/Users/snehsuresh/Desktop/Projects/aviation_data_projects/data/raw/merged_airline_data.csv"
output_csv = "/Users/snehsuresh/Desktop/Projects/aviation_data_projects/data/raw/raw_airline_data.csv"


def make_route_key_str(row):
    return "-".join(
        sorted([str(row["ORIGIN_CITY_MARKET_ID"]), str(row["DEST_CITY_MARKET_ID"])])
    )


def clean_city_name(city):
    if pd.isna(city):
        return city
    return city.split(",")[0].strip()


def extract_origin_dest_from_t100(df):
    df = df.copy()
    df["ROUTE_KEY"] = df.apply(make_route_key_str, axis=1)
    df["CARRIER"] = df["UNIQUE_CARRIER"]
    df["ORIGIN_CITY_NAME"] = df["ORIGIN_CITY_NAME"].apply(clean_city_name)
    df["DEST_CITY_NAME"] = df["DEST_CITY_NAME"].apply(clean_city_name)

    patch = (
        df.groupby(["YEAR", "QUARTER", "ROUTE_KEY", "CARRIER"], as_index=False)
        .agg(
            {
                "ORIGIN": "first",
                "DEST": "first",
                "ORIGIN_CITY_NAME": "first",
                "DEST_CITY_NAME": "first",
                "ORIGIN_STATE_ABR": "first",
                "DEST_STATE_ABR": "first",
            }
        )
        .rename(
            columns={"ORIGIN_STATE_ABR": "ORIGIN_STATE", "DEST_STATE_ABR": "DEST_STATE"}
        )
    )

    return patch


def main():
    print("🔍 Loading merged dataset...")
    merged_df = pd.read_csv(merged_csv, dtype=str)

    # Normalize keys in merged_df
    merged_df["ROUTE_KEY"] = merged_df["ROUTE_KEY"].apply(
        lambda x: "-".join(sorted([str(i) for i in eval(x)])) if pd.notna(x) else x
    )

    # Split into missing/fixed parts
    missing_rows = merged_df[
        merged_df["ORIGIN"].isna() | merged_df["DEST"].isna()
    ].copy()
    filled_rows = merged_df[
        ~(merged_df["ORIGIN"].isna() | merged_df["DEST"].isna())
    ].copy()

    print(f"🚫 Rows with missing ORIGIN/DEST: {len(missing_rows)}")

    all_patches = []

    for zipname in tqdm(os.listdir(t100_zip_dir), desc="📦 Processing zip files"):
        if not zipname.endswith(".zip"):
            continue
        zip_path = os.path.join(t100_zip_dir, zipname)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            for fname in zip_ref.namelist():
                if not fname.endswith(".csv"):
                    continue
                print(f"\n📂 Reading {fname} from {zipname}")
                with zip_ref.open(fname) as csvfile:
                    try:
                        df = pd.read_csv(csvfile, dtype=str)
                        if "ORIGIN_CITY_MARKET_ID" not in df.columns:
                            print("⚠️ Required columns missing, skipping.")
                            continue
                        patch = extract_origin_dest_from_t100(df)
                        all_patches.append(patch)
                    except Exception as e:
                        print(f"❌ Failed to process {fname}: {e}")

    if not all_patches:
        print("❌ No patch data extracted.")
        return

    patch_df = pd.concat(all_patches, ignore_index=True)

    # Normalize keys in both
    for df in [missing_rows, patch_df]:
        df["YEAR"] = df["YEAR"].astype(str)
        df["QUARTER"] = df["QUARTER"].astype(str)
        df["ROUTE_KEY"] = df["ROUTE_KEY"].astype(str)
        df["CARRIER"] = df["CARRIER"].astype(str)

    print("\n🔁 Merging patch into missing rows...")
    patched_missing = pd.merge(
        missing_rows.drop(
            columns=[
                "ORIGIN",
                "DEST",
                "ORIGIN_CITY_NAME",
                "DEST_CITY_NAME",
                "ORIGIN_STATE",
                "DEST_STATE",
            ],
            errors="ignore",
        ),
        patch_df,
        on=["YEAR", "QUARTER", "ROUTE_KEY", "CARRIER"],
        how="left",
    )

    final_df = pd.concat([filled_rows, patched_missing], ignore_index=True)
    final_df.to_csv(output_csv, index=False)

    print(f"\n✅ Final patched file saved as: {output_csv}")


if __name__ == "__main__":
    main()
