import re
import pandas as pd


def clean_text(value: str) -> str:
    if pd.isna(value):
        return value
    s = str(value)
    s = s.replace("Â", "")
    s = re.sub(r"\s+", " ", s).strip()
    s = s.rstrip(":").strip()
    return s


def load_table(path: str) -> pd.DataFrame:
    if path.lower().endswith(".csv"):
        return pd.read_csv(path, encoding="latin1")
    return pd.read_excel(path)


def parse_estimate(value):
    if pd.isna(value):
        return pd.NA
    s = str(value).strip()

    # remove common non-numeric formatting
    s = s.replace(",", "")      # 753,329 -> 753329
    s = s.replace("$", "")
    s = s.replace("%", "")
    s = s.replace("—", "")
    s = s.replace("-", "") if s == "-" else s

    return pd.to_numeric(s, errors="coerce")


def main():
    years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
    OUTPUT_FILE = r"WFH.csv"

    all_dfs = []

    for i in years:
        INPUT_FILE = r"datasets\work\[CLEAN] " + str(i) + " ACS 5-Year Estimates Detailed Tables.csv"

        df = load_table(INPUT_FILE)

        df.columns = [clean_text(c) for c in df.columns]

        first_col = df.columns[0]
        if "unnamed" in first_col.lower():
            df = df.drop(columns=[first_col])

        label_col = next((c for c in df.columns if "label" in c.lower()), df.columns[0])
        df[label_col] = df[label_col].apply(clean_text)

        value_cols = [c for c in df.columns if c != label_col]

        long_df = df.melt(
            id_vars=[label_col],
            value_vars=value_cols,
            var_name="county",
            value_name="estimate"
        )

        long_df["county"] = (
            long_df["county"]
            .str.replace("!!Estimate", "", regex=False)
            .str.strip()
        )

        # FIX: robust numeric parsing
        long_df["estimate"] = long_df["estimate"].apply(parse_estimate)

        long_df = long_df.dropna(subset=["estimate"])

        # Add year column
        long_df["year"] = i

        all_dfs.append(long_df)

    # Combine all years
    combined_df = pd.concat(all_dfs, ignore_index=True)

    combined_df = pd.read_csv(OUTPUT_FILE)

    combined_df["Label (Grouping)"].replace({
        "Worked at home": "Worked from home",
        "Public transportation (excluding taxicab)": "Public transportation",
        "Taxicab, motorcycle, bicycle, or other means": "Taxi or ride-hailing services, motorcycle, bicycle, or other means"
        }, inplace=True)

    combined_df.rename(columns={"Label (Grouping)": "method"}, inplace=True)

    combined_df["county"] = combined_df["county"].str.replace(", California", "")

    combined_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved: {OUTPUT_FILE}")
    print(f"Rows written: {len(combined_df)}")


if __name__ == "__main__":
    main()