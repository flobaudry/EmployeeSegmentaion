import base64
import io
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd


def parse_csv(contents, cluster_number):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
    df.columns = df.columns.str.replace(" ", "")
    if not test_columns(df):
        raise ValueError
    df, kmeans = categorize(df, cluster_number)
    return df, kmeans


def parse_csv_api(df, cluster_number):
    df.columns = df.columns.str.replace(" ", "")
    if not test_columns(df):
        raise ValueError
    df, kmeans = categorize(df, cluster_number)
    return df


def test_columns(df: pd.DataFrame):
    return all(col in list(df.columns) for col in ["CO2_in_g", "distance_in_m", "time_in_s"])


def define_transport(df, cluster_number):
    categories = []
    for i in range(cluster_number):
        filtr = df["cat"] == i
        categories.append(df[filtr].copy())
    min_co2 = df["CO2_in_g"].min()
    max_co2 = df["CO2_in_g"].max()
    cat = 0
    for category in categories:
        if category["CO2_in_g"].min() == min_co2:
            category.loc[:, "transport_mean"] = "bike"
        elif category["CO2_in_g"].max() == max_co2:
            category.loc[:, "transport_mean"] = "car"
        else:
            category.loc[:, "transport_mean"] = "public transport"
        cat += 1
    df = pd.concat(categories)
    return df


def categorize(df: pd.DataFrame, cluster_number):
    np_array = np.array(df.loc[:, ("distance_in_m", "time_in_s", "CO2_in_g")])
    kmeans = KMeans(n_clusters=cluster_number, max_iter=1000).fit(np_array)
    df.loc[:, "cat"] = kmeans.labels_
    df = define_transport(df, cluster_number)
    return df, kmeans
