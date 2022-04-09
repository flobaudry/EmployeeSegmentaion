import dash
from flask import Flask
import dash_bootstrap_components as dbc
from layout import layout

server = Flask(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY],
                suppress_callback_exceptions=True,
                server=server,
                url_base_pathname="/dash/",
                title="employee segmentation"
                )

app.layout = layout
