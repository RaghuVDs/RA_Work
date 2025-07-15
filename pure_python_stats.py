import csv
import math
from collections import defaultdict, Counter
from typing import List, Dict
from tabulate import tabulate

def is_float(s):
    try:
        float(s)
        return True
    except:
        return False

def summarize_column(col_values: List[str]) -> Dict:
    summary = {}
    numeric_values = [float(val) for val in col_values if is_float(val)]

    summary['count'] = len(col_values)
    if numeric_values:
        summary['mean'] = sum(numeric_values) / len(numeric_values)
        summary['min'] = min(numeric_values)
        summary['max'] = max(numeric_values)
        if len(numeric_values) > 1:
            mean = summary['mean']
            variance = sum((x - mean) ** 2 for x in numeric_values) / (len(numeric_values) - 1)
            summary['std_dev'] = math.sqrt(variance)
    else:
        freq = Counter(col_values)
        summary['unique_count'] = len(freq)
        summary['top_value'], summary['top_freq'] = freq.most_common(1)[0]

    return summary

def format_summary_for_tabulate(summary: Dict, col_name: str) -> List:
    row = [col_name]
    keys = ['count', 'mean', 'min', 'max', 'std_dev', 'unique_count', 'top_value', 'top_freq']
    for k in keys:
        row.append(summary.get(k, '—'))
    return row

def load_and_analyze(filepath: str, groupby_cols: List[str] = None):
    print(f"\nAnalyzing file: {filepath}\n")
    
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    if not data:
        print("No data found!")
        return

    # Overall Summary Table
    print("🔍 Overall Summary")
    column_data = defaultdict(list)
    for row in data:
        for k, v in row.items():
            column_data[k].append(v)

    table = []
    for col, values in column_data.items():
        stats = summarize_column(values)
        row = format_summary_for_tabulate(stats, col)
        table.append(row)

    headers = ['Column', 'Count', 'Mean', 'Min', 'Max', 'Std Dev', 'Unique Count', 'Top Value', 'Top Freq']
    print(tabulate(table, headers=headers, tablefmt='grid'))

    # Grouped Summary
    if groupby_cols:
        print(f"\nGrouped Summary by {groupby_cols} (showing 2 groups only)")
        grouped_data = defaultdict(lambda: defaultdict(list))
        for row in data:
            try:
                group_key = tuple(row[col] for col in groupby_cols)
            except KeyError:
                continue
            for col, val in row.items():
                grouped_data[group_key][col].append(val)

        for group_key, cols in list(grouped_data.items())[:2]:  # show only first 2 groups
            print(f"\nGroup: {group_key}")
            table = []
            for col, values in cols.items():
                if col in groupby_cols:
                    continue
                stats = summarize_column(values)
                row = format_summary_for_tabulate(stats, col)
                table.append(row)
            print(tabulate(table, headers=headers, tablefmt='fancy_grid'))

if __name__ == "__main__":
    files = [
        {
            "name": "Twitter Posts",
            "path": "2024_tw_posts_president_scored_anon.csv",
            "groupby": ["id"]  
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
        load_and_analyze(file["path"], groupby_cols=file["groupby"])
