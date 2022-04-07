import dash
import dash_bootstrap_components as dbc
from layout import layout

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)

app.layout = layout
