from flask import request, redirect
from app import server, app
from process import parse_csv_api
import pandas as pd
from io import StringIO


@server.route("/dash")
def my_dash_app():
    return app.index()


@server.route("/")
def redirect_main():
    return redirect("/dash")


@server.route("/api", methods=["GET", "POST"])
def api_request():
    url = request.args.get("url")
    raw = request.args.get("raw")
    if url is not None:
        df = pd.read_csv(url)
    elif raw is not None:
        data = StringIO(raw)
        df = pd.read_csv(data)
    else:
        return "No data given"
    try:
        df = parse_csv_api(df, 3)
        df.set_index("employee_ID", inplace=True)
        return df.to_csv()
    except ValueError:
        return "Error: Bad data input"
