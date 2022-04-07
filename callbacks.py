from app import app
from dash import html, dcc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from process import parse_csv


@app.callback(Output("graph", "children"),
              Input("process-button", "n_clicks"),
              State("upload-employees", "contents"),
              State("upload-employees", "filename"))
def process_data(n_clicks, contents, filename):
    cluster_number = 3
    res = html.Div(children=[])
    if contents is not None:
        df, kmeans = parse_csv(contents, filename, cluster_number)
        load_figure_template("darkly")
        figure = px.scatter_3d(df, x="distance_in_m", y="time_in_s", z="CO2_in_g", color="transport_mean",
                               template="darkly")

        figure.add_trace(go.Scatter3d(x=kmeans.cluster_centers_[:, 0], y=kmeans.cluster_centers_[:, 1],
                                      z=kmeans.cluster_centers_[:, 2], mode="markers", name="centroids",
                                      marker=go.scatter3d.Marker(opacity=0.7, size=16, color=['blue', 'red', 'green'])))
        if 'category' in df.columns:
            fig = px.scatter_3d(df, x="distance_in_m", y="time_in_s", z="CO2_in_g", color="category", template="darkly")
            res.children.append(
                dbc.Row([dbc.Col([html.H2("Computed segmentation"), dcc.Graph(figure=figure)], width=6),
                         dbc.Col([html.H2("Real segmentation"), dcc.Graph(figure=fig)], width=6)]))
        else:
            res.children.append(dbc.Row(dbc.Col(dcc.Graph(figure=figure))))
    return res


@app.callback(Output("collapse_button", "is_open"),
              Input("process-button", "n_clicks"),
              State("upload-employees", "contents"))
def show_collapse_button(button, contents):
    if contents is None:
        raise PreventUpdate
    return True


@app.callback(Output("upload_collapse", "is_open"),
              Input("open_upload", "n_clicks"),
              Input("process-button", "n_clicks"),
              State("upload-employees", "contents"),
              State("upload_collapse", "is_open")
              )
def toggle_collapse(button, process_button, contents, collapse):
    if contents is None:
        raise PreventUpdate
    return not collapse


@app.callback(Output("alert", "children"),
              Output("alert", "color"),
              Input("upload-employees", "contents"),
              State("upload-employees", "filename"))
def load_data(contents, filename):
    if contents is None:
        raise PreventUpdate
    else:
        return f"{filename} has been loaded", "success"
