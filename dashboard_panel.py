from libs.create_data import create_data

import hvplot.pandas
import numpy as np
import pandas as pd
import panel as pn

pn.extension('tabulator')

df_data = create_data()

component1 = pn.Row(
    pn.Column(
        pn.pane.Markdown("### This is the original data"),
        pn.widgets.Tabulator(df_data,
                             pagination='remote', page_size=20,
                             header_filters={
                                c: {'type': 'input', 'func': 'like'} if c != 'Gender'
                                else {'type': 'list', 'valuesLookup': True, 'sort': 'asc'}
                                for c in df_data.columns
                                },
                        ),
    ),
    pn.Column(
        pn.pane.Markdown("### Summary"),
        pn.panel(df_data.describe()),
    ),
)

component2 = pn.Row(

    pn.panel(df_data.hvplot.scatter(x='City', y='Age', by='Gender', title='Age vs City'))
)

component3 = pn.Row(
    pn.Column(
        pn.pane.Markdown('### Pivot ba'),
        pn.panel(
            (
                pd.pivot_table(df_data, index=['Gender', 'City'], columns='Married', values='Age', aggfunc='mean')
                .style.format(precision=2)
            )
        )
    ),
    pn.Column(
        pn.pane.Markdown('### Pivot b'),
        pn.panel(
            (
                pd.pivot_table(df_data, index='Gender', columns=['City', 'Married'], values='Age', aggfunc='mean')
                .style.format(precision=2)
            )
        )
    )
)


component4 = pn.Row(
    pn.Column(
        pn.pane.Markdown('### Pivot ba'),
        pn.widgets.Tabulator(
            (
                pd.pivot_table(df_data, index=['Gender', 'City'], columns='Married', values='Age', aggfunc='mean')
                .style.format(precision=2)
            ),
            hierarchical=True,
        )
    ),
    pn.Column(
        pn.pane.Markdown('### Pivot b'),
        pn.widgets.Tabulator(
            (
                pd.pivot_table(df_data, index='Gender', columns=['City', 'Married'], values='Age', aggfunc='mean')
                .style.format(precision=2)
            ),
            hierarchical=True,
        )
    )
)

pn.template.FastListTemplate(
    title="Example Data Display",
    sidebar=["# Sidebar"],
    main=["## All Data",
          component1,
          '## Scatter Plot',
          component2,
          '## Pivot 1',
          component3,
          '## Pivot 2',
          component4],
    main_layout='card',
).servable()