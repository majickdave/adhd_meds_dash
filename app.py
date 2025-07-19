import dash
from dash import dash_table, html
import pandas as pd

# --- load your data ---
file_path = 'med_list_clean.csv'
df = pd.read_csv(file_path)

# show everything except the last 6 columns
visible_cols = df.columns[:-6]
hidden_cols  = df.columns[-6:]

data = df[visible_cols].to_dict('records')

# --- build tooltips: one dict per row ---
tooltip_data = []
for row in df.to_dict('records'):
    # build a multi‐line string of hidden cols for this row
    details = "\n".join(f"**{col}**: {row[col]}" for col in hidden_cols)
    # attach the same details to each visible cell in this row
    tooltip_data.append({
        col: {'value': details, 'type': 'markdown'}
        for col in visible_cols
    })

# --- assemble your Dash app ---
app = dash.Dash(__name__)
app.layout = html.Div([
    dash_table.DataTable(
        id='med-table',
        columns=[{'name': c, 'id': c} for c in visible_cols],
        data=data,
        tooltip_data=tooltip_data,
        tooltip_duration=None,       # keep tooltip visible until mouseout
        style_cell={'whiteSpace': 'normal'},  # allow line‑wrap in tooltips
    )
])

server = app.server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
