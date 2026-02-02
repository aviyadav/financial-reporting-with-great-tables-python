import polars as pl
from gapminder import gapminder

from great_tables import GT, nanoplot_options

gapminder_df = pl.from_pandas(gapminder)

random_countries = gapminder_df.select("country").unique().sample(n=6)

gapminder_summary = (
    gapminder_df.filter(pl.col("country").is_in(random_countries["country"]))
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
    .tab_header(title="World Population by Country", subtitle="Population trends from 1952-2007")
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
    .tab_options(
        heading_background_color="#152649",
        heading_title_font_size="24px",
        heading_subtitle_font_size="14px",
        column_labels_background_color="#2D5C92",
    )
)

gt_table.show()