from dash import dcc, html
import dash_bootstrap_components as dbc

upload_layer = html.Div(children=[dbc.Row(dbc.Col(dcc.Upload(
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
                    className="d-grid gap-2", width=2), justify="center")])

start_layout = html.Div(children=[
    dbc.Collapse([dbc.Row([dbc.Col([dbc.Button("New upload", id="open_upload", className="h-100")],
                                   id="button_place", width=2)],  justify="left", className="my-3"),
                  dbc.Row(dbc.Col(dbc.Alert(id="show_filename", color="success")), className="my-3")],
                 id="collapse_button", is_open=False, className="m-3"),
    dbc.Collapse(upload_layer, id="upload_collapse", is_open=True),
    dbc.Row(dbc.Col(id='3Dgraph', width=12), className="m-3", justify="center"),
    dbc.Row(id="pie_charts", className="m-3"),
    dbc.Row(id="histogram", className="m-3")
]
)

layout = html.Div(
    id="page-content",
    children=start_layout
)
