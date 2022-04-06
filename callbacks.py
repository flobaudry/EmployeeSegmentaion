from app import app
from dash import html, dcc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
from dash.dependencies import Input, Output, State
from layout import fig_layout, start_layout
from process import parse_csv


@app.callback(Output("page-content", "children"),
              Input("process-button", "n_clicks"),
              State("upload-employees", "contents"),
              State("upload-employees", "filename"))
def process_data(n_clicks, contents, filename):
    res = start_layout
    if contents is not None:
        df = parse_csv(contents, filename)
        print(df)
        load_figure_template("darkly")
        figure = px.scatter_3d(df, x="distance_in_m", y="time_in_s", z="CO2_in_g", color="cat", template="darkly")
        res = html.Div(dcc.Graph(id="graph", figure=figure))
    return res
