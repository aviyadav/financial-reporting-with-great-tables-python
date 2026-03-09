import polars as pl
from gapminder import gapminder
from great_tables import GT, loc, nanoplot_options, style

# Convert pandas DataFrame to Polars
gapminder_df = pl.from_pandas(gapminder)

# Use a fixed seed for reproducibility so the same 6 countries are selected every run
random_countries = gapminder_df.select("country").unique().sample(n=6, seed=42)

gapminder_summary = (
    gapminder_df.filter(pl.col("country").is_in(random_countries["country"].to_list()))
    .group_by("country")
    .agg(
        [
            pl.col("year").sort().alias("years"),
            pl.col("pop").sort_by("year").alias("pop_trend"),
            pl.col("pop").sort_by("year").last().alias("population_2007"),
        ]
    )
    .with_columns(pl.col("years").list.last().alias("year"))
    .select(["country", "year", "population_2007", "pop_trend"])
    .sort("population_2007", descending=True)
)

gt_table = (
    GT(gapminder_summary)
    .tab_header(
        title="World Population by Country",
        subtitle="Population trends from 1952-2007",
    )
    .cols_label(
        country="Country",
        year="Latest Year",
        population_2007="Population (2007)",
        pop_trend="Population Trend",
    )
    .data_color(columns="population_2007", palette=["#96C3E0", "#24538E"])
    .fmt_integer(columns="population_2007")
    .fmt_nanoplot(
        columns="pop_trend",
        plot_type="bar",
        options=nanoplot_options(
            data_bar_stroke_color="#7EA2C6",
            data_bar_fill_color="#2C5B8F",
        ),
    )
    # Style the title text to be white and bold against the dark header background
    .tab_style(
        style=style.text(color="#FFFFFF", weight="bold"),
        locations=loc.title(),
    )
    # Style the subtitle text to be a light blue-grey
    .tab_style(
        style=style.text(color="#BDD0E8"),
        locations=loc.subtitle(),
    )
    # Style the column label text to be white and bold
    .tab_style(
        style=style.text(color="#FFFFFF", weight="bold"),
        locations=loc.column_labels(),
    )
    .tab_options(
        heading_background_color="#152649",
        heading_title_font_size="24px",
        heading_subtitle_font_size="14px",
        column_labels_background_color="#2D5C92",
        table_background_color="#F0F4F9",
        table_border_top_color="#152649",
        table_border_top_width="3px",
    )
)

# Export to HTML file for sharing/archiving
output_path = "output.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(gt_table.as_raw_html())

print(f"Table exported to {output_path}")

# Display interactively in browser
gt_table.show()
