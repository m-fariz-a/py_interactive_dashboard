import random
import pandas as pd
import plotly.express as px
from shiny import App, render, ui, Session
from shinywidgets import output_widget, render_widget
from itables.shiny import DT

def create_data():
    # Define lists for generating random data
    names = ['John', 'Alice', 'Bob', 'Emma', 'Michael', 'Sophia', 'James', 'Olivia', 'William', 'Ava']
    genders = ['Male', 'Female']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']

    # Generate 100 rows of data
    data = {
        'Name': random.choices(names, k=100),
        'Age': [random.randint(20, 60) for _ in range(100)],
        'Gender': random.choices(genders, k=100),
        'City': random.choices(cities, k=100),
        'Salary': [random.randint(30000, 100000) for _ in range(100)],
        'Married': random.choices(['Yes', 'No'], k=100)
    }
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    return df

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
                # [ui.markdown("This is the original data")],
               ui.output_ui("general_all_data"),
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
            ui.nav_panel(
                "Itables Rendering",
                ui.layout_columns(
                    ui.card(
                        ui.card_header("Multiindex Index"),
                        ui.output_ui("pivot_it_mi")
                    ),
                    ui.card(
                        ui.card_header("Multiindex Column"),
                        ui.output_ui("pivot_it_mc"),
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
    fluid=False
)


def server(session: Session):

    @render.ui
    def general_all_data():
        return ui.HTML(
            DT(
                df_data,
                # showIndex=True,
                autoWidth=False,
                pageLength=10,
                lengthMenu = [5, 10, 20],
                alternative_pagination='full_numbers',
                searching=False, paging=True,
                layout={
                    'topEnd':'pageLength'
                    },
                # scrollY=400, scrollCollapse=True,
                column_filters="footer",
                buttons=['csvHtml5', 'excelHtml5'],
            )
        )

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

    @render.ui
    def pivot_it_mi():
        df = pivot_data("multiindex_index")

        return ui.HTML(
            DT(
                df, info=False, searching=False, paging=False,
                # fixedRows={'top': 2},
                # scrollY=True,
                autoWidth=False,
                buttons=['csv', 'excel'],
            )
        )

    @render.ui
    def pivot_it_mc():
        df = pivot_data("multiindex_column")

        return ui.HTML(
            DT(
                df, info=False, searching=False, paging=False,
                # fixedColumns={'start': 1},
                # scrollX=True,
                autoWidth=False,
                buttons=['csv', 'excel'],
            )
        )


app = App(app_ui, server, debug=False)