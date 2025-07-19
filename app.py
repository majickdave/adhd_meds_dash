import os
import dash
from dash import dash_table, html
import pandas as pd
import random


# --- load your data ---
file_path = 'med_list_clean.csv'
df = pd.read_csv(file_path)
print(df.columns)
df.drop(columns=['duration', 'duration_low', 'duration_high'])

# show everything except the last 6 columns
visible_cols = ['Medication Type', 'Brand Name', 'Generic Name']
hidden_cols  = ['Duration', 'Mechanism of Action', 'Common Side Effects']

data = df[visible_cols].to_dict('records')

# --- build tooltips: one dict per row ---
tooltip_data = []
for row in df.to_dict('records'):
    # build a multi-line markdown string of hidden cols for this row
    details = "\n".join(f"**{col}**: {row[col]}" for col in hidden_cols)
    # attach the same details to each visible cell in this row
    tooltip_data.append({
        col: {'value': details, 'type': 'markdown'}
        for col in visible_cols
    })
# Generate a unique color for each Medication Type
unique_types = df['Medication Type'].unique()
color_palette = [
    '#ffcccc', '#ccffcc', '#ccccff', '#ffffcc', '#e0ccff',
    '#ccffff', '#ffd9b3', '#e6f7ff', '#d1f2eb', '#f9e79f'
]

type_color_map = {
    med_type: color_palette[i % len(color_palette)]
    for i, med_type in enumerate(unique_types)
}

# Create conditional styling rules based on Medication Type
type_based_styles = [
    {
        'if': {
            'filter_query': f'{{Medication Type}} = "{med_type}"'
        },
        'backgroundColor': color,
        'color': 'black'
    }
    for med_type, color in type_color_map.items()
]

# --- assemble your Dash app ---
app = dash.Dash(__name__)

app.layout = html.Div([
    # Title centered above the table
    html.H2(
        '💊 Adult ADHD Medication Duration Ranges',
        style={
            'textAlign': 'center',
            'margin': '20px 0',
            'fontFamily': 'Arial, sans-serif'
        }
    ),

    # DataTable wrapped in a div to center
    html.Div(
        dash_table.DataTable(
            id='med-table',
            columns=[{'name': c, 'id': c} for c in visible_cols],
            data=data,
            tooltip_data=tooltip_data,
            tooltip_duration=None,       # keep tooltip visible until mouseout

            # Table-level styling
            style_table={
                'width': '90%',
                'margin': '0 auto',         # center horizontally
                'overflowX': 'auto'
            },

            # Cell styling
            style_cell={
                'whiteSpace': 'normal',     # wrap text
                'height': 'auto',
                'textAlign': 'center',      # center text within cells
                'padding': '8px',
                'fontFamily': 'Arial, sans-serif'
            },

            # Header styling
            style_header={
                'backgroundColor': '#f2f2f2',
                'fontWeight': 'bold',
                'border': '1px solid #dfe6e9'
            },

            # Optional: zebra striping for rows
            style_data_conditional=type_based_styles

        ),
        style={'textAlign': 'center'}
    ),
    html.Div(
        html.A('⏳ Medication Duration Range Data Vizualization', href='https://adhdmeddash.streamlit.app/', target='_blank'),
        style={'textAlign': 'center', 'marginTop': '30px', 'fontSize': '18px'}
    )
], style={'fontFamily': 'Arial, sans-serif'})

server = app.server

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
