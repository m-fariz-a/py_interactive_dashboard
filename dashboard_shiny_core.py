import pandas as pd
import plotly.express as px
from shiny import App, render, ui, Session
from shinywidgets import output_widget, render_widget
from libs.create_data import create_data

def pivot_data(param: str):
    if param == "multiindex_index":
        df = (
            pd.pivot_table(df_data, index=['Gender', 'City'], columns='Married', values='Age', aggfunc='mean')
        )
    elif param == "multiindex_column":
        df = (
            pd.pivot_table(df_data, index='Gender', columns=['City', 'Married'], values='Age', aggfunc='mean')
        )
    return df


df_data = create_data()


app_ui = ui.page_navbar(
    ui.nav_panel(
        'General Data',
        ui.navset_card_tab(
            ui.nav_panel(
                "All Data",
               ui.output_data_frame("general_all_data"),
            ),
            ui.nav_panel(
                "Summary",
                ui.output_data_frame("summary_data")
            )
        )
    ),
    ui.nav_panel(
        "Graph",
        ui.card(
            ui.card_header("Coba grafik"),
            output_widget("scatter_plot")
        )
    ),
    ui.nav_panel(
        'Pivot',
        ui.navset_card_tab(
            ui.nav_panel(
                "Shiny Rendering",
                ui.layout_columns(
                    ui.card(
                        ui.card_header("Multiindex Index"),
                        ui.output_table("pivot_sh_mi")
                    ),
                    ui.card(
                        ui.card_header("Multiindex Column"),
                        ui.output_table("pivot_sh_mc")

                    ),
                    col_widths={"sm": (6, 6)},
                    height="500px",
                )
            ),
        )
    )
    ,
    title = 'Example Data Display',
    fillable=False, fillable_mobile=False,
    fluid=True,
    sidebar= ui.sidebar("Sidebar", bg="#f8f8f8"),
    bg = "#990000",
    inverse=True # bright font color
)


def server(session: Session):

    @render.data_frame
    def general_all_data():
        return render.DataGrid(df_data)

    @render.data_frame
    def summary_data():
        return df_data.describe().T

    @render_widget
    def scatter_plot():
        fig = px.scatter(df_data, x='City', y='Age', color='Gender', title='Age vs City')
        return fig

    @render.table
    def pivot_sh_mi():
        df = pivot_data("multiindex_index")

        return (
            df.style
            .format(precision=2)
            .set_table_attributes("class='table table-striped table-bordered table-hover table-condensed shiny-table w-auto'")
            .set_sticky(axis='columns')
            # .set_sticky(axis='columns')

        )

    @render.table
    def pivot_sh_mc():
        df = pivot_data("multiindex_column")

        return (
            df.style
            .format(precision=2)
            .set_table_attributes("class='table table-striped table-bordered table-hover table-condensed shiny-table w-auto'")
            .set_sticky(axis='index')
            # .set_sticky(axis='columns')

        )

app = App(app_ui, server, debug=False)