import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

df = pd.DataFrame([
    {'ID':'001','Name':'Alice','Role':'Admin'},
    {'ID':'002','Name':'Bob','Role':'User'}
])

gb = GridOptionsBuilder.from_dataframe(df)
# Enable tooltip on every column, pulling from a parallel dict
gb.configure_columns(df.columns.tolist(), 
                     tooltipField="__tooltip")
# Attach a tooltip column (won’t be shown)
tooltip_data = [{**row, '__tooltip': f"Extra info for {row['Name']}"} 
                for row in df.to_dict('records')]
AgGrid(pd.DataFrame(tooltip_data), gridOptions=gb.build())
