from app import app
from dash import html, dcc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from process import parse_csv
import pandas as pd

df: pd.DataFrame


@app.callback(Output("3Dgraph", "children"),
              Output("show_filename", "children"),
              Output("pie_charts", "children"),
              Input("process-button", "n_clicks"),
              State("upload-employees", "contents"),
              State("upload-employees", "filename"), prevent_initial_call=True)
def process_data(n_clicks, contents, filename):
    res_3d, res_pie = generate_graphs(contents, filename)
    if 'category' not in df.columns:
        res_pie = html.Div()
    return res_3d, f"{filename} is currently used", res_pie


def generate_pie_dropdown():
    res = dbc.Row(children=[])
    columns = ["CO2_in_g", "distance_in_m", "time_in_s"]
    dropdown = dcc.Dropdown(columns, "CO2_in_g", id="pie-dropdown", className="mb-2", searchable=False)
    res.children.append(
        dbc.Col([html.H2("Global observations"), dbc.Row(dcc.Graph(id="pie_chart_graph")), dbc.Row(dropdown)]))
    return res


@app.callback(Output("pie_chart_graph", "figure"),
              Input("pie-dropdown", "value"))
def generate_pie_graphs(value):
    return px.pie(df, values=value, names="transport_mean")


def generate_graphs(contents, filename):
    global df
    cluster_number = 3
    df, kmeans = parse_csv(contents, cluster_number)
    load_figure_template("darkly")

    return generate_3d_graphs(kmeans), generate_pie_dropdown()


def generate_3d_graphs(kmeans):
    res = html.Div(children=[])
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
        res.children.append(
            dbc.Row([dbc.Col([html.H2("Computed segmentation"), dcc.Graph(figure=figure)], width=6),
                     dbc.Col([generate_pie_dropdown()], width=6)]))
    return res


@app.callback(Output("collapse_button", "is_open"),
              Input("process-button", "n_clicks"),
              State("upload-employees", "contents"), prevent_initial_call=True)
def show_collapse_button(button, contents):
    return True


@app.callback(Output("upload_collapse", "is_open"),
              Input("open_upload", "n_clicks"),
              Input("process-button", "n_clicks"),
              State("upload_collapse", "is_open"), prevent_initial_call=True
              )
def toggle_collapse(button, process_button, collapse):
    return not collapse


@app.callback(Output("alert", "children"),
              Output("alert", "color"),
              Input("upload-employees", "contents"),
              State("upload-employees", "filename"), prevent_initial_call=True)
def load_data(contents, filename):
    return f"{filename} has been loaded", "success"
