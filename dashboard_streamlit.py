import streamlit as st
import pandas as pd
import plotly.express as px

from libs.create_data import create_data

df = create_data()

st.set_page_config(layout="wide")

# Display the data using Streamlit
st.title('Example Data Display')

st.write("My dashboard is my creation of my art")

# Display the DataFrame
st.write('## Summary:')

col1, col2= st.columns(2)
with col1:
    st.markdown('### First 5 Rows:')
    st.dataframe(df)

with col2:
    st.markdown('### Summary Statistics:')
    st.dataframe(df.describe())

# Display a bar chart of ages
st.write('## Bar Chart of Ages:')
st.bar_chart(df['Age'])

# Plotly scatter plot of age vs city
st.write('## Scatter Plot of Age vs City:')
fig = px.scatter(df, x='City', y='Age', color='Gender', title='Age vs City')
st.plotly_chart(fig)

# Pivot table with multi-index index
st.write('## Pivot Table with Multi-Index Index:')
pivot_table_index = pd.pivot_table(df, index=['Gender', 'City'], columns='Married', values='Age', aggfunc='mean')
st.dataframe(pivot_table_index)

# Pivot table with multi-index columns
st.write('## Pivot Table with Multi-Index Columns:')
pivot_table_columns = pd.pivot_table(df, index='Gender', columns=['City', 'Married'], values='Age', aggfunc='mean')
st.dataframe(pivot_table_columns)
st.table(pivot_table_columns)
