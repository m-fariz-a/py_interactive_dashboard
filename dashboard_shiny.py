import random
import pandas as pd
from shiny.express import render, ui
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
df_data = create_data()



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

with ui.nav_panel("Pivot v2"):

    with ui.navset_card_tab():

        with ui.nav_panel("Shiny Rendering"):

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
                            .set_sticky(axis='index')
                            # .set_sticky(axis='columns')

                        )


        with ui.nav_panel("itables rendering"):

            with ui.layout_columns(
                col_widths={"sm": (6, 6)},
                # row_heights=(2, 2),
                height="500px",
                # when the column width exceeds the screen width, the column will be wrapped to the next row
            ):

                with ui.card(full_screen=True):
                    ui.card_header("Pivot c")

                    df_pivotc = (
                        pd.pivot_table(df_data, index=['Gender', 'City'], columns='Married', values='Age', aggfunc='mean')
                    )
                    ui.HTML(
                        DT(
                            df_pivotc, info=False, searching=False, paging=False,
                            fixedRows={'top': 2}, scrollY=True
                        )
                    )

                with ui.card(full_screen=True):
                    ui.card_header("Pivot d")

                    df_pivotd = (
                        pd.pivot_table(df_data, index='Gender', columns=['City', 'Married'], values='Age', aggfunc='mean')
                    )

                    ui.HTML(
                        DT(
                            df_pivotd, info=False, searching=False, paging=False,
                            fixedColumns={'start': 1}, scrollX=True
                        )
                    )