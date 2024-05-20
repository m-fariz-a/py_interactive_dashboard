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

component1 = pn.Row(
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
            pn.pane.Markdown("Ini adalah summary data saja"),
            pn.panel(df_data.describe()),
            align=global_align,
        ),
        collapsible=global_collapsible,
        title = "Summary",
        margin=global_margin,
        width_policy=global_width_polcy,
        header_background=global_card_header_background,
    )
)

component2 = pn.Card(
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

component3 = pn.Row(
    pn.Card(
        pn.Column(
            pn.panel(
                (
                    pd.pivot_table(df_data, index=['Gender', 'City'], columns='Married', values='Age', aggfunc='mean')
                    .style.format(precision=2)
                )
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
            pn.panel(
                (
                    pd.pivot_table(df_data, index='Gender', columns=['City', 'Married'], values='Age', aggfunc='mean')
                    .style.format(precision=2)
                )
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


component4 = pn.Row(
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

dashboard_obj = pn.template.BootstrapTemplate(
    title="Example Data Display",
    sidebar=["# Sidebar"],
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

# Append a layout to the main area, to demonstrate the list-like API
dashboard_obj.main.append(
    pn.Column(
        component1,
        component2,
        component3,
        component4,
    )
)

dashboard_obj.servable()