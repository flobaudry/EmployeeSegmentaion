from app import app
from dash import html, dcc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from layout import start_layout
from process import parse_csv


@app.callback(Output("page-content", "children"),
              Input("process-button", "n_clicks"),
              State("upload-employees", "contents"),
              State("upload-employees", "filename"))
def process_data(n_clicks, contents, filename):
    res = start_layout
    if contents is not None:
        df, kmeans = parse_csv(contents, filename)
        print(kmeans.cluster_centers_)
        load_figure_template("darkly")
        figure = px.scatter_3d(df, x="distance_in_m", y="time_in_s", z="CO2_in_g", color="cat", template="darkly")
        figure.add_trace(go.Scatter3d(x=kmeans.cluster_centers_[:, 0], y=kmeans.cluster_centers_[:, 1],
                                      z=kmeans.cluster_centers_[:, 2], mode="markers", marker=go.scatter3d.Marker(opacity=0.8,size=16, color=list(range(3)))))
        fig = px.scatter_3d(df, x="distance_in_m", y="time_in_s", z="CO2_in_g", color="category", template="darkly")
        res = html.Div([dcc.Graph(id="graph", figure=figure), dcc.Graph(figure=fig)])
    return res


@app.callback(Output("alert", "children"),
              Output("alert", "color"),
              Input("upload-employees", "contents"),
              State("upload-employees", "filename"))
def load_data(contents, filename):
    if contents is None:
        raise PreventUpdate
    else:
        return f"{filename} has been loaded", "success"
