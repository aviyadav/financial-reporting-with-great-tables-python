# Financial Reporting with Great Tables (Python)

Create beautiful, publication-ready tables in Python using [Great Tables](https://posit-dev.github.io/great-tables/) and [Polars](https://pola.rs/).

## Features

- 📊 Interactive data tables with nanoplots (sparklines/bar charts)
- 🎨 Customizable styling and color palettes
- 📈 Population trend visualization using Gapminder data

## Requirements

- Python 3.13+

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/financial-reporting-with-great-tables-python.git
   cd financial-reporting-with-great-tables-python
   ```

2. Install dependencies:
   ```bash
   pip install -r pyproject.toml
   # or using uv
   uv sync
   ```

## Usage

Run the complete example:

```bash
python complete-example.py
```

This will generate an interactive table showing world population data by country with:
- Country names
- Latest year data (2007)
- Population figures with conditional color formatting
- Population trend nanoplots showing historical growth

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

## License

MIT
