import dash
import dash_bootstrap_components as dbc
from flask import Flask
from layout import layout

server = Flask(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY],
                suppress_callback_exceptions=True,
                server=server,
                url_base_pathname="/dash/",
                title="Employee Segmentation"
                )

app.layout = layout
