readme_content = """
# Descriptive Statistics of 2024 US Presidential Social Media Data

This project performs descriptive statistical analysis on datasets related to **Facebook Ads**, **Facebook Posts**, and **Twitter Posts** from the 2024 US Presidential election cycle. The analysis is conducted using:

- Pure Python (no third-party libraries)  
- Pandas  
- Polars  

Each method computes summary statistics for all columns and performs group-wise aggregation on key identifiers such as `page_id`, `ad_id`, and `Facebook_Id`.

---

## Datasets Used

> **Note:** Dataset files are not committed to this repo due to size/privacy. You can download them manually:

- [`2024_fb_ads_president_scored_anon.csv`](https://drive.google.com/file/d/1Jq0fPb-tq76Ee_RtM58fT0_M3o-JDBwe/view?usp=sharing)
- `2024_fb_posts_president_scored_anon.csv`
- `2024_tw_posts_president_scored_anon.csv`

---

## How to Run

Make sure you have Python 3.8+ installed.

### 1. Install dependencies:

```bash
pip install pandas polars tabulate
```

# Pure Python (no Pandas or Polars)
```
python script1_pure_python.py
```

# With Pandas
```
python script2_pandas.py
```

# With Polars
```
python script3_polars.py
```

