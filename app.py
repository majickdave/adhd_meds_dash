import os
import dash
from dash import dash_table, html
import pandas as pd

# --- load your data ---
file_path = 'med_list_clean.csv'
df = pd.read_csv(file_path)

# Columns to use
visible_cols = ['Brand Name']
hidden_cols = ['Duration', 'Mechanism of Action', 'Common Side Effects']

# Define emoji map for medication types
unique_types = df['Medication Type'].unique()
emoji_palette = [
    '🧠', '⚡️', '💊', '🌙', '🌀',
    '🔥', '🌿', '🧪', '🚀', '🔄'
]
type_emoji_map = {
    med_type: emoji_palette[i % len(emoji_palette)]
    for i, med_type in enumerate(unique_types)
}

# Add emoji prefix to Brand Name in display
df['Brand Name'] = df.apply(lambda row: f"{type_emoji_map[row['Medication Type']]} {row['Brand Name']}", axis=1)

# --- build tooltips ---
tooltip_data = []
for row in df.to_dict('records'):
    details = "\n".join(
        f"**{col}**: {row[col]}"
        for col in ['Medication Type'] + hidden_cols
    )
    tooltip_data.append({
        'Brand Name': {'value': details, 'type': 'markdown'}
    })

# --- create a legend ---
legend_items = [
    html.Div([
        html.Span(type_emoji_map[med_type], style={'fontSize': '20px', 'marginRight': '8px'}),
        html.Span(med_type)
    ], style={'margin': '5px', 'display': 'inline-flex', 'alignItems': 'center'})
    for med_type in unique_types
]

legend_section = html.Div([
    html.H4('Legend: Medication Type Icons', style={'textAlign': 'center'}),
    html.Div(legend_items, style={
        'display': 'flex',
        'flexWrap': 'wrap',
        'justifyContent': 'center',
        'gap': '15px',
        'padding': '10px'
    })
])

# --- assemble your Dash app ---
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(
        'ADHD Medications',
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
            }
            # Removed style_data_conditional
        ),
        style={'textAlign': 'center'}
    ),
    legend_section,
    html.Div(
        html.A('⏳ Medication Duration Range Data Visualization', href='https://adhdmeddash.streamlit.app/', target='_blank'),
        style={'textAlign': 'center', 'marginTop': '30px', 'fontSize': '18px'}
    )
])

server = app.server

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
