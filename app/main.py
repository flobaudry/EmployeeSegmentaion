from app import app
from route import *
from callbacks import process_data, load_data

if __name__ == '__main__':
    app.run_server(debug=True)
