# Retail Sales Analysis

A data analysis of six months of transactions across four stores for a South African grocery retailer, built to answer a real business questions: which products, categories, and stores drive revenue - and what should the business do next?

## Author

**Kuhlekonke Phungula** - 2026 Data Science Jan Cohort - Melsoft Academy

## The Dataset

`data/sales_data.csv` contains 600 individual sales transactions across four stores (Sandton, Rosebank, Soweto, Pretoria), covering roughly six months.
Each row records the date, a unique transaction ID, the product sold (ID, name, category), the store, quantity, unit price (in Rand), and payment method. Revenue is not provided directly - it's calculated in this analysis
as `quantity * unit_price`.

The raw file contains several deliberate real-world data issues (missing values, invalid entries, inconsistent formatting, duplicates) which are detected and removed in code before any analysis runs - see the Data Quality
Report printed in `analysis.ipynb`.

## How to Run

pip install -r requirements.txt

Then open `analysis.ipynb` in Jupyter (or VS Code) and run all cells from top to bottom. The notebook imports its cleaning, analysis, and charting logic from `helpers.py`, prints the data-quality report and all descriptive
results, and saves three charts into `charts/`.

## Key Findings

- **Beverages is the top revenue category** (R109,320), not because it sells the most units (Dairy does, at 1,054 vs Beverages' 1,009) or because it's the priciest (Meat is, at R127.57/unit average vs Beverages' R108.51) -
it wins by combining strong volume and a mid-to-high price, while Dairy and Meat each only have one of those two factors working in their favor.

![alt text](image.png)

- **Sandton is the top-performing store** (R89,137.50), narrowly ahead of Pretoria and Soweto, with Rosebank trailing.

- **Volume and profitability point to different products.** Rooibos Tea 100g is the best-seller by quantity (570 units), but Coffee Beans 1kg earns the most revenue (R77,760) - a cheap, frequently-repurchased product isn't the same product as the one generating the most money.

- **Revenue trended upward from January through May** before dropping in June. The dataset appears to end mid-way through July (only a single day's transactions are recorded for that month), so the sharp apparent drop in July reflects incomplete data, not a real decline in sales.

- **Mobile is the most common payment method**, ahead of Card, Cash, and EFT.

## Recommendations

- **Double down on Beverages and investigate Meat's volume gap.** Meat has the highest average price per unit but is held back by low volume - a promotion or bundling strategy aimed at moving more units could lift its revenue.
- **Look into Rosebank specifically before allocating further investment anywhere.** Its underperformance on revenue which suggests something structural - store size, local foot traffic, or staffing - that's worth understanding rather than assuming it's simply a smaller market.
- **Understand what drove the May peak** so it can potentially be replicated - a seasonal effect, a promotion, or a one-off event will each suggest a different action.
- **Fix data collection.** The incomplete July data makes the most recent trend impossible to read reliably; a partial month should either be excluded from monthly comparisons or clearly flagged.

## Limitations & Next Steps

This analysis only has **revenue, not cost or profit margin** - a high-revenue category or store isn't necessarily the most profitable one, and that distinction matters for any investment decision. It also has no customer-level data, so repeat-purchase behavior and customer loyalty can't be assessed. Before committing to any of the recommendations above, I'd want: complete data through the end of July, and store-level context such as foot traffic, size, and local competition.

## Tools Used

- **Python** - functions, loops, exception handling (`try`/`except`), and the standard library `datetime` module, used throughout the data-cleaning functions in `helpers.py`
- **Pandas** - `groupby`, `sum`, `mean`, and `sort_values` for the descriptive analysis.
- **Matplotlib** - bar and line charts, generated through  reusable, parameterized chart-saving functions rather than repeated per-chart code