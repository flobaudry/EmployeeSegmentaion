import base64
import io
from sklearn.cluster import KMeans
import numpy as np

import pandas as pd


def parse_csv(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    df.columns = df.columns.str.replace(' ', '')
    df, kmeans = categorize(df)
    return df, kmeans


def categorize(df: pd.DataFrame):
    np_array = np.array(df.drop(['employee_ID', 'category'], inplace=False, axis=1))
    kmeans = KMeans(n_clusters=3, max_iter=1000).fit(np_array)
    df['cat'] = kmeans.labels_
    return df, kmeans
