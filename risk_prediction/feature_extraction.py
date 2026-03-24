import pandas as pd

def extract_features(csv_path="dataset.csv"):

    df = pd.read_csv(csv_path)

    df["timestamp"] = pd.to_numeric(df["timestamp"])

    df["time_gap"] = df["timestamp"].diff().fillna(0)

    df["rolling_attempts"] = df["failed_attempts"].rolling(window=5, min_periods=1).mean()

    feature_columns = [
        "password_entropy",
        "failed_attempts",
        "vulnerability_score",
        "time_gap",
        "rolling_attempts",
        "dictionary_flag"
    ]

    X = df[feature_columns]
    y = df["label"]

    return X, y