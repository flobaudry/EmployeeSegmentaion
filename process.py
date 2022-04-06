import base64
import io
from sklearn.cluster import KMeans

import pandas as pd


def parse_csv(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    df.columns = df.columns.str.replace(' ', '')
    df["cat"] = 1
    return df
