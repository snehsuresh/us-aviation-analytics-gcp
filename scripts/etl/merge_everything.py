import os
import zipfile
import pandas as pd

DATA_DIR = "data"
OUTPUT_FILE = "merged_airline_data.csv"


def extract_zip_if_needed(path):
    """Extract zip if found. Return path to the extracted folder."""
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if zipfile.is_zipfile(item_path):
            extract_path = os.path.join(path, item.replace(".zip", ""))
            with zipfile.ZipFile(item_path, "r") as zip_ref:
                zip_ref.extractall(extract_path)
            print(f"Unzipped: {item_path} → {extract_path}")
            return extract_path
    return None  # No zip found


def find_csv_files(folder):
    """Find all relevant CSVs in a folder."""
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".csv") and f.startswith("nonstop_route_merged")
    ]


def main():
    all_dfs = []

    for year_folder in sorted(os.listdir(DATA_DIR)):
        year_path = os.path.join(DATA_DIR, year_folder)
        if not os.path.isdir(year_path):
            continue

        print(f"Processing: {year_folder}")

        # Look in year folder itself for CSVs
        csv_files = find_csv_files(year_path)

        # Look for zip/extracted folder (if any)
        extracted_path = extract_zip_if_needed(year_path)

        # ✅ NEW: If no zip, try to find exactly one subfolder inside (e.g. OneDrive_13_25-06-2025)
        if not extracted_path:
            subfolders = [
                os.path.join(year_path, f)
                for f in os.listdir(year_path)
                if os.path.isdir(os.path.join(year_path, f))
            ]
            if len(subfolders) == 1:
                extracted_path = subfolders[0]

        # Add CSVs from the extracted folder
        if extracted_path and os.path.isdir(extracted_path):
            csv_files += find_csv_files(extracted_path)

        if not csv_files:
            print(f"⚠️ Skipping {year_folder}, no valid CSVs found.")
            continue

        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                all_dfs.append(df)
            except Exception as e:
                print(f"❌ Failed to load {csv_file}: {e}")

    if all_dfs:
        merged_df = pd.concat(all_dfs, ignore_index=True)
        merged_df = merged_df.sort_values(by=["YEAR", "QUARTER"]).reset_index(drop=True)
        merged_df.to_csv(OUTPUT_FILE, index=False)
        print(f"\n✅ Merged {len(all_dfs)} files. Output saved to {OUTPUT_FILE}")
    else:
        print("❌ No data was merged.")


if __name__ == "__main__":
    main()
