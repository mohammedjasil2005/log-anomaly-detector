import re
import pandas as pd
from datetime import datetime


LOG_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>INFO|WARNING|ERROR)\s+"
    r"(?P<message>.+)"
)


def parse_log_file(filepath: str) -> pd.DataFrame:
    """
    Parse a raw log file into a structured DataFrame.

    Each row = one log entry with:
      - timestamp   : datetime
      - level       : INFO / WARNING / ERROR
      - message     : raw log message
      - is_error    : 1 if ERROR, else 0
      - is_warning  : 1 if WARNING, else 0
      - msg_length  : character count of message
    """
    records = []

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = LOG_PATTERN.match(line)
            if match:
                records.append(match.groupdict())
            else:
                print(f"[WARN] Could not parse line: {line[:80]}")

    df = pd.DataFrame(records)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["is_error"]   = (df["level"] == "ERROR").astype(int)
    df["is_warning"] = (df["level"] == "WARNING").astype(int)
    df["msg_length"] = df["message"].str.len()

    df = df.sort_values("timestamp").reset_index(drop=True)

    return df


def engineer_features(df: pd.DataFrame, window: str = "1min") -> pd.DataFrame:
    """
    Roll up raw log rows into time-window features for the ML model.

    For each 1-minute window we compute:
      - total_logs    : how many log lines fired
      - error_count   : how many were ERRORs
      - warning_count : how many were WARNINGs
      - error_rate    : fraction of logs that were errors
      - avg_msg_len   : average message length (spikes = unusual messages)
    """
    df = df.set_index("timestamp")

    features = df.resample(window).agg(
        total_logs    = ("level",      "count"),
        error_count   = ("is_error",   "sum"),
        warning_count = ("is_warning", "sum"),
        avg_msg_len   = ("msg_length", "mean"),
    ).fillna(0)

    features["error_rate"] = (
        features["error_count"] / features["total_logs"].replace(0, 1)
    )

    return features.reset_index()


if __name__ == "__main__":
    import os

    log_path = os.path.join(os.path.dirname(__file__), "data", "server.log")

    print("Parsing logs...")
    df = parse_log_file(log_path)
    print(f"  Parsed {len(df):,} log entries")
    print(f"  Time range: {df['timestamp'].min()} → {df['timestamp'].max()}")
    print(f"  Error count: {df['is_error'].sum()}")
    print()

    print("Engineering features (1-minute windows)...")
    features = engineer_features(df)
    print(features.to_string())

    out = os.path.join(os.path.dirname(__file__), "data", "features.csv")
    features.to_csv(out, index=False)
    print(f"\nSaved -> data/features.csv")
