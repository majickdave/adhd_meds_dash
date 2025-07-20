import os
import dash
from dash import dash_table, html
import pandas as pd

# --- load your data ---
file_path = 'med_list_clean.csv'
df = pd.read_csv(file_path)

# Columns to use
visible_cols = ['Brand Name']
hidden_cols  = ['Duration', 'Mechanism of Action', 'Common Side Effects']
# Keep 'Medication Type' for tooltips and styling but don't show in table

# --- build tooltips: one dict per row ---
tooltip_data = []
for row in df.to_dict('records'):
    details = "\n".join(
        f"**{col}**: {row[col]}"
        for col in ['Medication Type'] + hidden_cols
    )
    tooltip_data.append({
        'Brand Name': {'value': details, 'type': 'markdown'}
    })

# Generate color mapping
unique_types = df['Medication Type'].unique()
color_palette = [
    '#ffcccc', '#ccffcc', '#ccccff', '#ffffcc', '#e0ccff',
    '#ccffff', '#ffd9b3', '#e6f7ff', '#d1f2eb', '#f9e79f'
]
type_color_map = {
    med_type: color_palette[i % len(color_palette)]
    for i, med_type in enumerate(unique_types)
}

# Conditional formatting (still based on Medication Type)
type_based_styles = [
    {
        'if': {
            'filter_query': f'{{Medication Type}} = "{med_type}"',
            'column_id': 'Brand Name'
        },
        'backgroundColor': color,
        'color': 'black'
    }
    for med_type, color in type_color_map.items()
]

# --- assemble your Dash app ---
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2(
        '💊 ADHD Medications — Brand Names',
        style={'textAlign': 'center', 'margin': '20px 0'}
    ),
    html.Div(
        dash_table.DataTable(
            id='med-table',
            columns=[{'name': c, 'id': c} for c in visible_cols],
            data=df.to_dict('records'),
            tooltip_data=tooltip_data,
            tooltip_duration=None,
            style_table={
                'width': '80%',
                'margin': '0 auto',
                'overflowX': 'auto'
            },
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'center',
                'padding': '8px',
                'fontFamily': 'Arial, sans-serif'
            },
            style_header={
                'backgroundColor': '#f2f2f2',
                'fontWeight': 'bold',
                'border': '1px solid #dfe6e9'
            },
            style_data_conditional=type_based_styles
        ),
        style={'textAlign': 'center'}
    ),
    html.Div(
        html.A('⏳ Medication Duration Range Data Visualization', href='https://adhdmeddash.streamlit.app/', target='_blank'),
        style={'textAlign': 'center', 'marginTop': '30px', 'fontSize': '18px'}
    )
])

server = app.server

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
