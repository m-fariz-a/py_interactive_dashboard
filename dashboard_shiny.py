from libs.create_data import create_data

import pandas as pd
import plotly.express as px
from shiny.express import input, render, ui
from shinywidgets import render_widget, render_plotly
from itables.shiny import DT

df_data = create_data()

index_names = {
    'selector': '.index_name',
    'props': 'font-style: italic; color: darkgrey; font-weight:normal;'
}
headers = {
    'selector': 'th:not(.index_name)',
    'props': 'background-color: #000066; color: white;'
}

ui.page_opts(title="Example Data Display", fillable=False)

# ui.markdown(
#     """
#     My dashboard is my creation of my art
#     """
# )

with ui.nav_panel("General Data"):

    with ui.navset_card_tab():

        with ui.nav_panel("All Data"):
            ui.markdown("This is the original data")

            ui.HTML(
                DT(
                    df_data, showIndex=True, searching=False, autowidth=True,
                    paging=True, scrollY=400, scrollCollapse=True,
                    alternative_pagination='full_numbers',
                    column_filters="footer", layout={'topEnd':'pageLength'},
                    buttons=['csvHtml5', 'excelHtml5']
                    )
            )

        with ui.nav_panel("Summary"):
            ui.markdown("This is the summary of the data")

            @render.data_frame
            def summary():
                return df_data.describe().T


with ui.nav_panel("Other Analysis"):

    with ui.card(full_screen=True):
        ui.card_header("Scatter Plot of Age vs City")

        @render_plotly
        def scatter_plot():
            fig = px.scatter(df_data, x='City', y='Age', color='Gender', title='Age vs City')
            return fig

with ui.nav_panel("Pivot v2"):
    with ui.layout_columns(
        col_widths={"sm": (6, 6)},
        # row_heights=(2, 2),
        height="500px",
        # when the column width exceeds the screen width, the column will be wrapped to the next row
    ):

        with ui.card(full_screen=True):
            ui.card_header("Pivot a")

            @render.table
            def pivot1b():
                df = (
                    pd.pivot_table(df_data, index=['Gender', 'City'], columns='Married', values='Age', aggfunc='mean')
                )
                return (
                    df.style
                    .format(precision=2)
                    .set_table_attributes("class='table table-striped table-bordered table-hover table-condensed shiny-table w-auto'")
                    # .set_table_styles([index_names, headers])
                    .set_sticky(axis='columns')
                    # .set_sticky(axis='columns')

                )

        with ui.card(full_screen=True):
            ui.card_header("Pivot b")

            @render.table
            def pivot2b():
                df = (
                    pd.pivot_table(df_data, index='Gender', columns=['City', 'Married'], values='Age', aggfunc='mean')
                )
                return (
                    df.style
                    .format(precision=2)
                    .set_table_attributes("class='table table-striped table-bordered table-hover table-condensed shiny-table w-auto'")
                    # .set_table_styles([index_names, headers])
                    .set_sticky(axis='index')
                    # .set_sticky(axis='columns')

                )