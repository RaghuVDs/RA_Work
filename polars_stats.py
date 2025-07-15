import polars as pl
from tabulate import tabulate
from functools import reduce
import operator

TOP_N_GROUPS = 5  # Show only top N groups by size

def summarize_overall(df: pl.DataFrame):
    print("🔍 Overall Summary: Numeric Columns")
    numeric_summary = df.select(pl.col(pl.NUMERIC_DTYPES)).describe().transpose()
    print(tabulate(numeric_summary.to_numpy(), headers=numeric_summary.columns, tablefmt='grid'))

    print("\nOverall Summary: Categorical Columns")
    cat_cols = [col for col in df.columns if df[col].dtype == pl.Utf8]
    table = []
    for col in cat_cols:
        try:
            vc = df[col].value_counts().sort("counts", descending=True)
            top_val = vc[0, "unique"]
            top_freq = vc[0, "counts"]
        except:
            top_val, top_freq = "—", "—"
        row = [col, df[col].n_unique(), top_val, top_freq]
        table.append(row)
    headers = ['Column', 'Unique Count', 'Top Value', 'Top Freq']
    print(tabulate(table, headers=headers, tablefmt='grid'))

def summarize_grouped_top_n(df: pl.DataFrame, groupby_cols):
    print(f"\nGrouped Summary by {groupby_cols} (Top {TOP_N_GROUPS} Groups by Size)")

    group_sizes = (
        df.group_by(groupby_cols)
        .agg(pl.count().alias("group_size"))
        .sort("group_size", descending=True)
    )
    top_groups = group_sizes[:TOP_N_GROUPS]

    for row in top_groups.iter_rows():
        group_key = tuple(row[:len(groupby_cols)])
        print(f"\n🧾 Group: {group_key}")

        # Fix: Create proper AND mask using reduce + operator.and_
        conditions = [df[col] == val for col, val in zip(groupby_cols, group_key)]
        mask = reduce(operator.and_, conditions)

        group_df = df.filter(mask)
        numeric_summary = group_df.select(pl.col(pl.NUMERIC_DTYPES)).describe().transpose()
        print(tabulate(numeric_summary.to_numpy(), headers=numeric_summary.columns, tablefmt='fancy_grid'))

def analyze_file(filepath: str, groupby_cols=None):
    print(f"\nAnalyzing: {filepath}")
    try:
        df = pl.read_csv(filepath)
    except Exception as e:
        print(f"Failed to read file: {e}")
        return

    summarize_overall(df)

    if groupby_cols:
        summarize_grouped_top_n(df, groupby_cols)

if __name__ == "__main__":
    files = [
        {
            "name": "Twitter Posts",
            "path": "2024_tw_posts_president_scored_anon.csv",
            "groupby": None
        },
        {
            "name": "Facebook Posts",
            "path": "2024_fb_posts_president_scored_anon.csv",
            "groupby": ["Facebook_Id"]
        },
        {
            "name": "Facebook Ads",
            "path": "2024_fb_ads_president_scored_anon.csv",
            "groupby": ["page_id", "ad_id"]
        }
    ]

    for file in files:
        print(f"\n========== {file['name']} ==========")
        analyze_file(file["path"], groupby_cols=file["groupby"])
