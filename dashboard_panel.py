from libs.create_data import create_data

import hvplot.pandas
import numpy as np
import pandas as pd
import panel as pn

pn.extension('tabulator')

df_data = create_data()


global_collapsible = False
global_align = 'center'
global_margin = 10
global_width_polcy = 'max'
global_card_header_background = 'transparent'

data_responden = pn.widgets.Tabulator(df_data,
                                pagination='remote', page_size=20,
                                header_filters={
                                    c: {'type': 'input', 'func': 'like'} if c != 'Gender'
                                    else {'type': 'list', 'valuesLookup': True, 'sort': 'asc'}
                                    for c in df_data.columns
                                    },
                                layout='fit_data_table',
                                theme='fast',
                )
filename, button = data_responden.download_menu(
    text_kwargs={'name': 'Enter filename', 'value': 'data_responden.csv'},
    button_kwargs={'name': 'Download table'}
)


font_size = "10pt"
def magnify():
    return [dict(selector="th",
                 props=[("font-size", font_size)]),
            dict(selector="td",
                 props=[("font-size", font_size)]),
            dict(selector="tr",
                 props=[("font-size", font_size)])
    ]


class Halaman1:
    def __init__(self):
        self.content = pn.Row(
            pn.Card(
                pn.Column(
                    filename, button,
                    data_responden,
                    align=global_align,
                ),
                collapsible=global_collapsible,
                title = "This is the original data",
                margin=global_margin,
                width_policy=global_width_polcy,
                header_background=global_card_header_background,
            ),
            pn.layout.HSpacer(),
            pn.Card(
                pn.Column(
                    pn.pane.Str("Ini adalah summary data saja", styles={'font-size': '20pt'},
                                ),
                    pn.pane.DataFrame(df_data.describe().style.set_table_styles(magnify())),
                    align=global_align,
                ),
                collapsible=global_collapsible,
                title = "Summary",
                margin=global_margin,
                width_policy=global_width_polcy,
                header_background=global_card_header_background,
            )
        )

    def view(self):
        return self.content

class Halaman2:
    def __init__(self):
        self.content = pn.Card(
            pn.Row(
                pn.panel(df_data.hvplot.scatter(x='City', y='Age', by='Gender', title='Age vs City')),
                align=global_align
            ),
            collapsible=global_collapsible,
            title = "Scatter Plot",
            margin=global_margin,
            width_policy=global_width_polcy,
            header_background=global_card_header_background,
        )

    def view(self):
        return self.content

class Halaman3:
    def __init__(self):
        self.content = pn.Row(
            pn.Card(
                pn.Column(
                    pn.pane.DataFrame(
                        (
                            pd.pivot_table(df_data, index=['Gender', 'City'], columns='Married', values='Age', aggfunc='mean')
                            .style.format(precision=2)
                            .set_table_styles(magnify())
                        ),
                        sizing_mode="stretch_width",
                    ),
                    align=global_align,
                ),
                collapsible=global_collapsible,
                title = "Pivot a",
                margin=global_margin,
                width_policy=global_width_polcy,
                header_background=global_card_header_background,
            ),
            pn.layout.HSpacer(),
            pn.Card(
                pn.Column(
                    pn.pane.DataFrame(
                        (
                            pd.pivot_table(df_data, index='Gender', columns=['City', 'Married'], values='Age', aggfunc='mean')
                            .style.format(precision=2)
                            .set_table_styles(magnify())
                            .set_sticky(axis=0)
                        ),
                        sizing_mode="stretch_width",
                    ),
                    align=global_align,
                ),
                collapsible=global_collapsible,
                title = "Pivot b",
                margin=global_margin,
                width_policy=global_width_polcy,
                header_background=global_card_header_background,
            )
        )

    def view(self):
        return self.content

class Halaman4:
    def __init__(self):
        self.content = pn.Row(
            pn.Card(
                pn.Column(
                    pn.pane.Markdown('### Pivot ba'),
                    pn.widgets.Tabulator(
                        (
                            pd.pivot_table(df_data, index=['Gender', 'City'], columns='Married', values='Age', aggfunc='mean')
                            .style.format(precision=2)
                        ),
                        hierarchical=True,
                        theme='fast',
                    ),
                align=global_align,
                ),
                collapsible=global_collapsible,
                title = "Pivot ba",
                margin=global_margin,
                width_policy=global_width_polcy,
                header_background=global_card_header_background,
            ),
            pn.layout.HSpacer(),
            pn.Card(
                pn.Column(
                    pn.pane.Markdown('### Pivot b'),
                    pn.widgets.Tabulator(
                        (
                            pd.pivot_table(df_data, index='Gender', columns=['City', 'Married'], values='Age', aggfunc='mean')
                            .style.format(precision=2)
                        ),
                        hierarchical=True,
                        theme='fast',
                    ),
                align=global_align,
                ),
                collapsible=global_collapsible,
                title = "Pivot bb",
                margin=global_margin,
                width_policy=global_width_polcy,
                header_background=global_card_header_background,
            )
        )

    def view(self):
        return self.content

# # Function to create a navigation sidebar
# def create_buttons(pages):
#     buttons = []
#     for k, v in pages.items():
#         _button = pn.widgets.Button(name=k, button_type='primary', sizing_mode='stretch_width')
#         _button.on_click(lambda event: show_page(v))
#         buttons.append(_button)

#     return buttons

def show_page(page_instance):
    main_area.clear()
    main_area.append(page_instance.view())

dashboard_obj = pn.template.BootstrapTemplate(
    title="Example Data Display",
    sidebar=["## Daftar isi"],
    # main=[
    #     "## All Data",
    #     component1,
    #     '## Scatter Plot',
    #     component2,
    #     '## Pivot 1',
    #     component3,
    #     '## Pivot 2',
    #     component4
    # ],
    sidebar_width=300,
    header_background="maroon",
)


pages = {
    "halaman 1": Halaman1(),
    "halaman 2": Halaman2(),
    "halaman 3": Halaman3(),
    "halaman 4": Halaman4(),
}

# Create the sidebar
# page_buttons = create_buttons(pages)
# sidebar = pn.Column(page_buttons, width=200)

# Define buttons to navigate between pages
page1_button = pn.widgets.Button(name="halaman 1", button_type="default", sizing_mode='stretch_width')
page2_button = pn.widgets.Button(name="halaman 2", button_type="default", sizing_mode='stretch_width')
page3_button = pn.widgets.Button(name="halaman 3", button_type="default", sizing_mode='stretch_width')
page4_button = pn.widgets.Button(name="halaman 4", button_type="default", sizing_mode='stretch_width')

# Set up button click callbacks
page1_button.on_click(lambda event: show_page(pages["halaman 1"]))
page2_button.on_click(lambda event: show_page(pages["halaman 2"]))
page3_button.on_click(lambda event: show_page(pages["halaman 3"]))
page4_button.on_click(lambda event: show_page(pages["halaman 4"]))

# Create the sidebar
sidebar = pn.Column(page1_button, page2_button, page3_button, page4_button)

# Create the main area
main_area = pn.Column(pages["halaman 1"].view())

# Append a layout to the main area, to demonstrate the list-like API
dashboard_obj.main.append(
    main_area
)

dashboard_obj.sidebar.append(
    sidebar
)

dashboard_obj.servable()