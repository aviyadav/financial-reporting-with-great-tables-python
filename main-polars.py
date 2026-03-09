import polars as pl
from great_tables import GT, vals


def basic_financial_statement(income_stmt: pl.DataFrame):
    financial_table = (
        GT(income_stmt)
        .tab_header(
            title="Income Statement Overview",
            subtitle="Quarterly Results (USD)",
        )
        .fmt_currency(
            columns=["Q3 2025", "Q4 2025"],
            currency="USD",
            decimals=0,
        )
        .fmt_percent(
            columns=["YoY Change"],
            decimals=1,
        )
        .opt_stylize(style=1, color="gray")
    )

    financial_table.show()


def accounting_notation(income_stmt: pl.DataFrame):
    financial_table = (
        GT(income_stmt)
        .tab_header(title="Income Statement")
        .fmt_currency(
            columns=["Q3 2025", "Q4 2025"],
            currency="USD",
            decimals=0,
            accounting=True,
        )
        .fmt_percent(columns=["YoY Change"], decimals=1)
    )

    financial_table.show()


def smart_rows_grand_total(income_stmt: pl.DataFrame):
    financial_table = (
        GT(income_stmt, rowname_col="Line Item")
        .tab_header(title="Income Statement")
        .fmt_currency(
            columns=["Q3 2025", "Q4 2025"],
            currency="USD",
            decimals=0,
            accounting=True,
        )
        .fmt_percent(columns=["YoY Change"], decimals=1)
        .grand_summary_rows(
            fns={
                "Total": pl.col("Q3 2025", "Q4 2025").sum(),
            },
            fmt=vals.fmt_currency,
        )
    )

    financial_table.show()


def multiple_currencies():
    multi_currency = pl.DataFrame(
        {
            "Region": ["North America", "Europe", "Asia Pacific"],
            "USD": [1_200_000, 890_000, 1_450_000],
            "EUR": [1_100_000, 820_000, 1_330_000],
            "JPY": [168_000_000, 124_000_000, 202_000_000],
        }
    )

    multi_currency_table = (
        GT(multi_currency)
        .tab_header(title="Regional Revenue by Currency")
        .fmt_currency(columns="USD", currency="USD", decimals=0)
        .fmt_currency(columns="EUR", currency="EUR", decimals=0)
        .fmt_currency(columns="JPY", currency="JPY", decimals=0)
    )

    multi_currency_table.show()


def column_spanners_hierarchical_headers():
    quarterly_comparison = pl.DataFrame(
        {
            "Region": ["North", "South", "East", "West"],
            "Q1_Revenue": [450_000, 380_000, 520_000, 410_000],
            "Q1_Profit": [67_500, 53_200, 78_000, 61_500],
            "Q2_Revenue": [485_000, 395_000, 548_000, 430_000],
            "Q2_Profit": [72_750, 55_300, 82_200, 64_500],
        }
    )

    comparison_table = (
        GT(quarterly_comparison)
        .tab_header(title="Regional Financial Performance")
        .tab_spanner(label="Q1 2025", columns=["Q1_Revenue", "Q1_Profit"])
        .tab_spanner(label="Q2 2025", columns=["Q2_Revenue", "Q2_Profit"])
        .cols_label(
            Q1_Revenue="Revenue",
            Q1_Profit="Profit",
            Q2_Revenue="Revenue",
            Q2_Profit="Profit",
        )
        .fmt_currency(
            columns=["Q1_Revenue", "Q1_Profit", "Q2_Revenue", "Q2_Profit"],
            currency="USD",
            decimals=0,
        )
    )

    comparison_table.show()


def portfolio_performance_dashboard():
    portfolio = pl.DataFrame(
        {
            "Ticker": ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"],
            "Company": [
                "Apple Inc.",
                "Alphabet Inc.",
                "Microsoft Corp.",
                "Amazon.com Inc.",
                "Tesla Inc.",
            ],
            "Shares": [150, 50, 200, 75, 100],
            "Cost Basis": [142.50, 2_450.00, 285.00, 3_150.00, 195.00],
            "Current Price": [178.25, 2_890.00, 367.50, 3_520.00, 242.80],
            "Market Value": [26_737.50, 144_500.00, 73_500.00, 264_000.00, 24_280.00],
            "Gain/Loss": [5_362.50, 22_000.00, 16_500.00, 27_750.00, 4_780.00],
            "Return": [0.251, 0.179, 0.289, 0.117, 0.245],
        }
    )

    portfolio_table = (
        GT(portfolio)
        .tab_header(
            title="Investment Portfolio Summary",
            subtitle="As of January 12, 2026",
        )
        .fmt_integer(columns="Shares")
        .fmt_currency(
            columns=["Cost Basis", "Current Price", "Market Value", "Gain/Loss"],
            currency="USD",
            decimals=2,
        )
        .fmt_percent(columns="Return", decimals=1)
        .data_color(
            columns="Return",
            palette=["#ef4444", "#ffffff", "#22c55e"],
        )
        .tab_source_note("Data is delayed by 15 minutes. Portfolio value: $533,017.50")
        .opt_stylize(style=6, color="blue")
    )

    portfolio_table.show()


if __name__ == "__main__":
    # Sample income statement data using Polars
    income_stmt = pl.DataFrame(
        {
            "Line Item": [
                "Revenue",
                "Cost of Goods Sold",
                "Gross Profit",
                "Operating Expenses",
                "Operating Income",
                "Interest Expense",
                "Net Income",
            ],
            "Q3 2025": [
                2_450_000,
                -920_000,
                1_530_000,
                -680_000,
                850_000,
                -45_000,
                805_000,
            ],
            "Q4 2025": [
                2_890_000,
                -1_050_000,
                1_840_000,
                -720_000,
                1_120_000,
                -42_000,
                1_078_000,
            ],
            "YoY Change": [0.18, 0.14, 0.20, 0.06, 0.32, -0.07, 0.34],
        }
    )

    # basic_financial_statement(income_stmt)
    # accounting_notation(income_stmt)
    # smart_rows_grand_total(income_stmt)
    # multiple_currencies()
    # column_spanners_hierarchical_headers()
    portfolio_performance_dashboard()
