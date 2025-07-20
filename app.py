import os
import dash
from dash import dash_table, html, dcc, Input, Output
import pandas as pd

# --- load your data ---
file_path = 'med_list_clean.csv'
df = pd.read_csv(file_path)

df['Brand Name'] = df['Brand Name'] + ' - ' + df['Generic Name']

# Columns to use
visible_cols = ['Brand Name']
hidden_cols = ['Generic Name', 'Duration', 'Mechanism of Action', 'Common Side Effects']

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
df['Brand Name Display'] = df.apply(lambda row: f"{type_emoji_map[row['Medication Type']]} {row['Brand Name']}", axis=1)

# --- build tooltips ---
def make_tooltip(row):
    details = "\n".join(
        f"**{col}**: {row[col]}"
        for col in ['Medication Type'] + hidden_cols
    )
    return {'Brand Name Display': {'value': details, 'type': 'markdown'}}

# --- create a legend ---
legend_items = [
    html.Div([
        html.Span(type_emoji_map[med_type], style={'fontSize': '20px', 'marginRight': '8px'}),
        html.Span(med_type)
    ], style={'margin': '5px', 'display': 'inline-flex', 'alignItems': 'center'})
    for med_type in unique_types
]

legend_section = html.Div([
    html.Div(legend_items, style={
        'display': 'flex',
        'flexWrap': 'wrap',
        'justifyContent': 'center',
        'gap': '15px',
        'padding': '10px'
    })
])

# --- Dash app ---
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('ADHD Medications', style={'textAlign': 'center', 'margin': '20px 0'}),
    
    html.Div([
        dcc.Input(
            id='brand-search',
            type='text',
            placeholder='Search Brand Name or Generic...',
            style={'width': '50%', 'padding': '10px', 'marginBottom': '20px'}
        )
    ], style={'textAlign': 'center'}),
        
    legend_section,

    html.Div(
        dash_table.DataTable(
            id='med-table',
            columns=[{'name': 'Brand Name', 'id': 'Brand Name Display'}],
            data=[],
            tooltip_data=[],
            tooltip_duration=None,
            style_table={'width': '80%', 'margin': '0 auto', 'overflowX': 'auto'},
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
        ),
        style={'textAlign': 'center'}
    ),
        
    html.Div(
        html.A('⏳ Medication Duration Range Data Visualization',
               href='https://adhdmeddash.streamlit.app/', target='_blank'),
        style={'textAlign': 'center', 'marginTop': '30px', 'fontSize': '18px'}
    ),

])

# --- callback to filter data ---
@app.callback(
    Output('med-table', 'data'),
    Output('med-table', 'tooltip_data'),
    Input('brand-search', 'value')
)
def update_table(search_text):
    if not search_text:
        filtered = df
    else:
        filtered = df[df['Brand Name'].str.contains(search_text, case=False, na=False)]

    data = filtered[['Brand Name Display']].to_dict('records')
    tooltips = [make_tooltip(row) for _, row in filtered.iterrows()]
    return data, tooltips

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
