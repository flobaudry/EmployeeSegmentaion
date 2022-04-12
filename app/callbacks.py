from app import app
from dash import html, dcc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
from process import parse_csv

df: pd.DataFrame
COLOR_MAP = {"car": "#B71E1D", "bike": "#06A843", "public transport": "#324C71"}
CAT_ORDER = {"transport_mean": ["car", "public transport", "bike"], "category": ["car", "public", "bike"]}


@app.callback(Output("3Dgraph", "children"),
              Output("show_filename", "children"),
              Output("show_filename", "color"),
              Output("pie_charts", "children"),
              Output("histogram", "children"),
              Input("process-button", "n_clicks"),
              State("upload-employees", "contents"),
              State("upload-employees", "filename"), prevent_initial_call=True)
def process_data(n_clicks, contents, filename):
    show_filename_text = f"{filename} is currently used"
    show_filename_color = "success"
    res_3d, res_pie, res_histogram = generate_graphs(contents)
    if len(res_3d.children) == 0:
        show_filename_text = "Bad input format"
        show_filename_color = "danger"
    elif 'category' not in df.columns:
        res_pie = html.Div()

    return res_3d, show_filename_text, show_filename_color, res_pie, res_histogram


def generate_graphs(contents):
    global df
    cluster_number = 3
    colors = {"car": "red", "bike": "blue", "public transport": "green"}
    try:
        df, kmeans = parse_csv(contents, cluster_number)
        df["color"] = df["transport_mean"].apply(lambda x: colors.get(x))
        load_figure_template("darkly")
        return generate_3d_graphs(kmeans), generate_pie_dropdown(), generate_hist_graph()
    except ValueError:
        return dbc.Col(children=[]), dbc.Col(children=[]), dbc.Col(children=[])


def generate_3d_graphs(kmeans):
    res = html.Div(children=[])
    figure = px.scatter_3d(df, x="distance_in_m", y="time_in_s", z="CO2_in_g", color="transport_mean",
                           template="darkly", color_discrete_map=COLOR_MAP, category_orders=CAT_ORDER)

    figure.add_trace(go.Scatter3d(x=kmeans.cluster_centers_[:, 0], y=kmeans.cluster_centers_[:, 1],
                                  z=kmeans.cluster_centers_[:, 2], mode="markers", name="centroids", marker_symbol="x",
                                  marker_color="white", marker_opacity=0.8))
    if "category" in df.columns:
        fig = px.scatter_3d(df, x="distance_in_m", y="time_in_s", z="CO2_in_g", color="category", template="darkly")
        res.children.append(
            dbc.Row([dbc.Col([html.H2("Computed segmentation"), dcc.Graph(figure=figure)], width=6),
                     dbc.Col([html.H2("Real segmentation"), dcc.Graph(figure=fig)], width=6)]))
    else:
        res.children.append(
            dbc.Row([dbc.Col([html.H2("Computed segmentation"), dcc.Graph(figure=figure)], width=6),
                     dbc.Col([generate_pie_dropdown()], width=6)]))
    return res


def generate_hist_graph():
    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="avg", x=df["transport_mean"], y=df["CO2_in_g"], name="average CO2 emission",
                               marker_color="#ffbb00"))
    fig.add_trace(go.Histogram(histfunc="avg", x=df["transport_mean"], y=df["distance_in_m"], name="average distance",
                               marker_color="#00fff7"))
    fig.add_trace(go.Histogram(histfunc="avg", x=df["transport_mean"], y=df["time_in_s"], name="average time",
                               marker_color="#ff00dd"))
    fig.update_layout(height=600)

    res = dbc.Col([html.H2("Averages"), dcc.Graph(figure=fig)])
    return res


def generate_pie_dropdown():
    columns = ["CO2 in g", "distance in m", "time in s", "total count"]
    res = dbc.Row(children=[])
    dropdown = dcc.Dropdown(columns, "CO2 in g", id="pie-dropdown", className="mb-2", searchable=False)
    res.children.append(
        dbc.Col([html.H2("Global observations"), dbc.Row(dcc.Graph(id="pie_chart_graph")), dbc.Row(dropdown)]))
    return res


@app.callback(Output("pie_chart_graph", "figure"),
              Input("pie-dropdown", "value"))
def generate_pie_graphs(value):
    if value == "total count":
        df["count"] = 1
        value = "count"
    res = px.pie(df, values=value.replace(" ", "_"), names="transport_mean",
                 color="transport_mean", color_discrete_map=COLOR_MAP)
    return res


@app.callback(Output("collapse_button", "is_open"),
              Input("process-button", "n_clicks"), prevent_initial_call=True)
def show_collapse_button(button):
    return True


@app.callback(Output("upload_collapse", "is_open"),
              Input("open_upload", "n_clicks"),
              Input("process-button", "n_clicks"),
              Input("show_filename", "color"),
              State("upload_collapse", "is_open"), prevent_initial_call=True
              )
def toggle_collapse(button, process_button, error, collapse):
    if error == "danger":
        return True
    return not collapse


@app.callback(Output("alert", "children"),
              Output("alert", "color"),
              Input("upload-employees", "contents"),
              Input("process-button", "n_clicks"),
              State("upload-employees", "filename"), prevent_initial_call=True)
def load_data(contents, button, filename):
    return f"{filename} has been loaded", "success"
