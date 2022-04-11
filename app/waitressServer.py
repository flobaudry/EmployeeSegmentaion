from app import app
from waitress import serve
from route import *
from callbacks import process_data, load_data

serve(app.server, port=8050)
