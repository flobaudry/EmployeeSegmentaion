from dash import dcc, html
import dash_bootstrap_components as dbc

start_layout = html.Div(children=[
    dbc.Row(dbc.Col(dcc.Upload(
        id="upload-employees",
        children=html.Div([
            "Drag and Drop or ",
            html.A("Select Files", className="alert-link")
        ]),
        style={
            'width': '100%',
            'height': '120px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ), width=8), justify="center"),
    dbc.Row(dbc.Col(dbc.Alert("No file loaded", id="alert", color="danger"),
                    className="text-center", width=3), justify="center"),
    dbc.Row(dbc.Col(dbc.Button("Launch process", id="process-button", color="info", n_clicks=0),
                    className="d-grid gap-2", width=2), justify="center")
]
)

fig_layout = html.Div(
    dcc.Graph(id="graph")
)

layout = html.Div(
    id="page-content",
    children=start_layout
)
