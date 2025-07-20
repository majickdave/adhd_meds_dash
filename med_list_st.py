import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Medication Duration Chart", layout="centered")

st.title("💊 Adult ADHD Medication Duration Ranges")

file_path = 'med_list_clean.csv'

df = pd.read_csv(file_path)

# Optional filter
with st.expander("🔍 Filter by Medication Type"):
    selected_types = st.multiselect(
        "Select types to include",
        options=df['Medication Type'].unique(),
        default=df['Medication Type'].unique()
    )
    df = df[df['Medication Type'].isin(selected_types)]

# Plot
fig = px.bar(
    df,
    x='duration',
    y='Brand Name',
    orientation='h',
    base='duration_low',
    color='Medication Type',
    hover_data={
        'Generic Name': True,
        'Duration': True,
        'Mechanism of Action': True,
        'Common Side Effects': True,
        'duration_low': False,
        'duration_high': False,
        'duration': False,
    },
    labels={'duration': 'Duration (hours)'},
    title='Medication Duration Ranges by Brand'
)

df = df.rename(columns={'duration_low': 'Duration (hours)'})

treemap = px.treemap(
    df,
    path=['Medication Type', 'Generic Name', 'Brand Name'],
    values='Duration (hours)',
    color='Medication Type',
    color_discrete_sequence=px.colors.qualitative.Pastel,
    title='Medication Hierarchy by Duration (hours)'
)

# Remove the default "sum of values" from tooltip
treemap.update_traces(
    hovertemplate='<b>%{label}</b><br>Duration: %{value} hours<br><extra></extra>'
)

treemap.update_traces(textinfo='label+value')

st.plotly_chart(treemap)
st.plotly_chart(fig)
st.markdown("[Go to Medication Table App](https://adult-adhd-med-list-f7031a735048.herokuapp.com/)")

# Optional: show raw data
with st.expander("📊 Show Data Table"):
    st.dataframe(df)
