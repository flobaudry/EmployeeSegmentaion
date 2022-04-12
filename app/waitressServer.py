from app import app
from waitress import serve
from route import *
import os
from callbacks import process_data, load_data

serve(app.server, port=os.environ.get("PORT"))
