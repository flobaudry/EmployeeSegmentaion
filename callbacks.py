from app import app
from dash import html
from dash.dependencies import Input, Output, State
from layout import fig_layout, start_layout
from process import parse_csv


@app.callback(Output("page-content", "children"),
              Input("process-button", "n_clicks"),
              State("upload-employees", "contents"),
              State("upload-employees", "filename"))
def process_data(n_clicks, contents, filename):
    if contents is not None:
        parse_csv(contents, filename)
    return start_layout
