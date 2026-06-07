import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import os

FEATURES = ["total_logs", "error_count", "warning_count", "avg_msg_len", "error_rate"]


def load_features(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    return df


def detect_anomalies(df: pd.DataFrame, contamination: float = 0.1) -> pd.DataFrame:
    """
    Train an Isolation Forest on the feature windows and flag anomalies.

    contamination = expected fraction of anomalies (0.1 = ~10% of windows)
    Returns the same DataFrame with two new columns:
      - anomaly_score : raw score (more negative = more anomalous)
      - is_anomaly    : 1 if flagged, 0 if normal
    """
    X = df[FEATURES].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=42
    )
    model.fit(X_scaled)

    df["anomaly_score"] = model.score_samples(X_scaled)
    df["is_anomaly"]    = (model.predict(X_scaled) == -1).astype(int)

    return df


def print_results(df: pd.DataFrame):
    anomalies = df[df["is_anomaly"] == 1].copy()
    normal    = df[df["is_anomaly"] == 0].copy()

    print(f"Total windows   : {len(df)}")
    print(f"Normal windows  : {len(normal)}")
    print(f"Anomalies found : {len(anomalies)}")
    print()
    print("Flagged anomaly windows:")
    print("-" * 70)
    for _, row in anomalies.iterrows():
        print(
            f"  {row['timestamp']}  |  "
            f"errors={int(row['error_count']):>3}  |  "
            f"error_rate={row['error_rate']:.2f}  |  "
            f"total_logs={int(row['total_logs']):>3}  |  "
            f"score={row['anomaly_score']:.3f}"
        )


if __name__ == "__main__":
    csv_path = os.path.join(os.path.dirname(__file__), "data", "features.csv")

    print("Loading features...")
    df = load_features(csv_path)

    print("Running Isolation Forest...\n")
    df = detect_anomalies(df)

    print_results(df)

    out = os.path.join(os.path.dirname(__file__), "data", "results.csv")
    df.to_csv(out, index=False)
    print(f"\nSaved -> data/results.csv")
