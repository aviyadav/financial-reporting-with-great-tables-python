# Financial Reporting with Great Tables (Python)

Create beautiful, publication-ready financial tables in Python using [Great Tables](https://posit-dev.github.io/great-tables/), [Polars](https://pola.rs/), and [pandas](https://pandas.pydata.org/).

## Features

- 📊 Interactive data tables with nanoplots (sparklines/bar charts)
- 💱 Multi-currency formatting and accounting notation
- 🏗️ Hierarchical column spanners for structured financial layouts
- 📈 Population trend visualization using Gapminder data
- 🎨 Customizable styling, color palettes, and conditional formatting
- 💾 HTML export for sharing and archiving
- 🔁 Reproducible output via fixed random seed

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/financial-reporting-with-great-tables-python.git
   cd financial-reporting-with-great-tables-python
   ```

2. Install dependencies using `uv` (recommended):
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install -e .
   ```

## Scripts

| File | Description | Data library | Output |
|---|---|---|---|
| `main.py` | Financial reporting examples using pandas | pandas | Browser |
| `main-polars.py` | Same examples fully ported to Polars | Polars | Browser |
| `complete-example.py` | Gapminder population table with nanoplots | Polars | `output.html` + browser |
| `complete-example-pandas.py` | Same Gapminder table, data wrangling in pandas | pandas + Polars (GT handoff) | `output-pandas.html` + browser |

---

## Usage

### Financial reporting examples

`main.py` and `main-polars.py` each contain six functions demonstrating different Great Tables features.
To switch between them, uncomment the desired function call at the bottom of the file.

**pandas version:**
```bash
uv run main.py
```

**Polars version (recommended):**
```bash
uv run main-polars.py
```

#### Functions

| Function | GT features demonstrated |
|---|---|
| `basic_financial_statement` | `fmt_currency`, `fmt_percent`, `opt_stylize` |
| `accounting_notation` | `fmt_currency(accounting=True)` for parenthesised negatives |
| `smart_rows_grand_total` | `rowname_col`, `grand_summary_rows` with column totals |
| `multiple_currencies` | Per-column `fmt_currency` with USD, EUR, and JPY |
| `column_spanners_hierarchical_headers` | `tab_spanner`, `cols_label` for two-level headers |
| `portfolio_performance_dashboard` | `fmt_integer`, `fmt_currency`, `fmt_percent`, `data_color`, `tab_source_note`, `opt_stylize` |

To run a specific function, edit the `if __name__ == "__main__"` block and uncomment the relevant call:

```python
# basic_financial_statement(income_stmt)
# accounting_notation(income_stmt)
# smart_rows_grand_total(income_stmt)
# multiple_currencies()
# column_spanners_hierarchical_headers()
portfolio_performance_dashboard()   # currently active
```

---

### Gapminder population table

**Polars version:**
```bash
uv run complete-example.py
```

**pandas version:**
```bash
uv run complete-example-pandas.py
```

Both scripts:
1. Sample 6 random countries from the Gapminder dataset (reproducibly via a fixed seed)
2. Build a per-country summary with the latest year, latest population, and a full trend list
3. Render a styled Great Tables HTML table with inline nanoplot bar charts
4. Export the result to an HTML file
5. Open the table interactively in the browser

---

## Polars vs pandas

### `main.py` → `main-polars.py`

All `great_tables` methods (`fmt_currency`, `fmt_percent`, `data_color`, `tab_spanner`, etc.) accept both
pandas and Polars DataFrames without any changes. The only differences are:

| Area | pandas (`main.py`) | Polars (`main-polars.py`) |
|---|---|---|
| Import | `import pandas as pd` | `import polars as pl` |
| DataFrame construction | `pd.DataFrame({...})` | `pl.DataFrame({...})` |
| `grand_summary_rows` aggregation | `lambda df: df[cols].sum()` | `pl.col("Q3 2025", "Q4 2025").sum()` |
| `grand_summary_rows` formatting | Not passed (unformatted) | `fmt=vals.fmt_currency` |

The Polars version of `grand_summary_rows` uses a native Polars expression and passes `fmt=vals.fmt_currency`
so the grand total row is automatically currency-formatted — cleaner and more idiomatic than the pandas lambda approach.

---

### `complete-example.py` → `complete-example-pandas.py`

| Operation | Polars | pandas |
|---|---|---|
| Load data | `pl.from_pandas(gapminder)` | `gapminder` directly (already a pandas DataFrame) |
| Sample with seed | `.sample(n=6, seed=42)` | `.sample(n=6, random_state=42)` |
| Filter rows | `pl.col("country").is_in([...])` | `df["country"].isin(...)` |
| Pre-sort before group | Not needed (uses `sort_by` inside `agg`) | `.sort_values("year")` before `groupby` |
| Group + list aggregation | `.group_by().agg(pl.col().sort_by("year"))` | `.groupby().agg(col=("col", list))` |
| Extract last list element | `pl.col("years").list.last()` | `df["years"].str[-1]` |
| Sort descending | `.sort("col", descending=True)` | `.sort_values("col", ascending=False)` |
| Pass to `GT` | `GT(polars_df)` | `GT(polars_df)` — see known issue below |

---

## Known Issues

### `fmt_nanoplot` crashes with pandas list columns

When a pandas DataFrame containing list-typed columns is passed directly to `GT`, `great_tables` internally
calls `pd.isna(x)` on each cell. When `x` is a Python list, `pd.isna` returns an array of booleans
rather than a single bool, raising:

```
ValueError: The truth value of an array with more than one element is ambiguous.
```

**Workaround:** Perform all data wrangling in pandas, then convert the final DataFrame to Polars via
`pl.from_pandas()` before passing it to `GT`. Cast `pop_trend` list values to `float` at this point
since Polars requires a uniform element type for list columns:

```python
gapminder_summary_pl = pl.from_pandas(
    gapminder_summary.assign(
        pop_trend=gapminder_summary["pop_trend"].apply(lambda x: [float(v) for v in x])
    )
)
gt_table = GT(gapminder_summary_pl)
```

---

### `gapminder` package incompatible with Python 3.13

The `gapminder` package uses the deprecated `pkg_resources` API to load its bundled CSV. This module
is not available by default in Python 3.13 virtual environments, causing:

```
ModuleNotFoundError: No module named 'pkg_resources'
```

**Fix:** Patch `.venv/lib/python3.13/site-packages/gapminder/data.py` to use the modern
`importlib.resources` API:

```python
# Before
import pkg_resources

def _load_gapminder():
    content = pkg_resources.resource_string('gapminder', 'gapminder.csv').decode()
    return pd.read_csv(StringIO(content))

# After
from importlib.resources import files

def _load_gapminder():
    content = files('gapminder').joinpath('gapminder.csv').read_text(encoding='utf-8')
    return pd.read_csv(StringIO(content))
```

---

## Dependencies

- **great-tables** - Create beautiful tables in Python
- **polars** - Fast DataFrame library
- **gapminder** - Sample dataset for demonstrations
- **pandas** - Data manipulation (required by gapminder)
- **pyarrow** - Arrow integration for data processing

## Example Output

The script generates a styled table with:
- Custom header with dark blue background
- Color-coded population values (light to dark blue gradient)
- Inline bar charts showing population trends from 1952-2007

