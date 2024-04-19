from libs.create_data import create_data

import plotly.express as px
from shiny.express import input, render, ui
from shinywidgets import render_widget, render_plotly

df_data = create_data()


ui.page_opts(title="Example Data Display")

ui.markdown(
    """
    My dashboard is my creation of my art
    """
)


with ui.layout_columns(
    col_widths={"sm": (7, 5, 12)},
    # row_heights=(2, 3),
    # height="700px",
    # when the column width exceeds the screen width, the column will be wrapped to the next row
):
    with ui.card(full_screen=False):
        ui.card_header("All Data")
        ui.markdown("This is the original data")

        @render.data_frame
        def data_ori():
            df = df_data
            return render.DataTable(
                df, filters=True, selection_mode='rows'
            )

    with ui.card(full_screen=False):
        ui.card_header("Summary")
        ui.markdown("This is the summary of the data")

        @render.data_frame
        def data_summary():
            df = df_data.describe()
            return df.reset_index()


ui.markdown("## Other Analysis")

with ui.card(full_screen=False):
    ui.card_header("Scatter Plot of Age vs City")

    @render_plotly
    def scatter_plot():
        fig = px.scatter(df_data, x='City', y='Age', color='Gender', title='Age vs City')
        return fig