import pandas as pd
from tabulate import tabulate

TOP_N_GROUPS = 5  # Change this to control how many top groups to display

def summarize_overall(df: pd.DataFrame):
    print("🔍 Overall Summary: Numeric Columns")
    numeric_summary = df.describe(include=[float, int]).T
    numeric_summary.reset_index(inplace=True)
    print(tabulate(numeric_summary, headers='keys', tablefmt='grid', showindex=False))

    print("\nOverall Summary: Categorical Columns")
    cat_cols = df.select_dtypes(include='object').columns
    table = []
    for col in cat_cols:
        top_val = df[col].value_counts().idxmax() if not df[col].value_counts().empty else '—'
        top_freq = df[col].value_counts().max() if not df[col].value_counts().empty else '—'
        row = [
            col,
            df[col].nunique(),
            top_val,
            top_freq
        ]
        table.append(row)
    headers = ['Column', 'Unique Count', 'Top Value', 'Top Freq']
    print(tabulate(table, headers=headers, tablefmt='grid'))

def summarize_grouped_top_n(df: pd.DataFrame, groupby_cols):
    print(f"\nGrouped Summary by {groupby_cols} (Top {TOP_N_GROUPS} Groups by Size)")
    grouped = df.groupby(groupby_cols)

    # Count group sizes and get top N
    top_groups = grouped.size().sort_values(ascending=False).head(TOP_N_GROUPS).index

    for group_key in top_groups:
        group_df = grouped.get_group(group_key)
        print(f"\nGroup: {group_key}")
        numeric_summary = group_df.describe(include=[float, int]).T
        numeric_summary.reset_index(inplace=True)
        print(tabulate(numeric_summary, headers='keys', tablefmt='fancy_grid', showindex=False))

def analyze_file(filepath: str, groupby_cols=None):
    print(f"\nAnalyzing: {filepath}")
    try:
        df = pd.read_csv(filepath)
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
            "groupby": None  # no grouping for unique tweet id
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
