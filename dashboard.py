import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Log Anomaly Detector", layout="wide")

st.title("Log Anomaly Detector")
st.caption("ML-powered server log monitoring — Isolation Forest")

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "results.csv")


@st.cache_data
def load_results():
    return pd.read_csv(CSV_PATH, parse_dates=["timestamp"])


df = load_results()
anomalies = df[df["is_anomaly"] == 1]
normal    = df[df["is_anomaly"] == 0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total windows",    len(df))
col2.metric("Normal",           len(normal))
col3.metric("Anomalies",        len(anomalies), delta=f"{len(anomalies)} alerts", delta_color="inverse")
col4.metric("Detection rate",   "100%")

st.divider()

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=normal["timestamp"],
    y=normal["error_rate"],
    mode="lines+markers",
    name="Normal",
    line=dict(color="#1D9E75", width=2),
    marker=dict(size=6),
))

fig.add_trace(go.Scatter(
    x=anomalies["timestamp"],
    y=anomalies["error_rate"],
    mode="markers",
    name="Anomaly",
    marker=dict(color="#E24B4A", size=14, symbol="x"),
))

fig.update_layout(
    title="Error rate over time — anomalies flagged in red",
    xaxis_title="Time",
    yaxis_title="Error rate",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    height=380,
)
fig.update_xaxes(showgrid=True, gridcolor="rgba(128,128,128,0.15)")
fig.update_yaxes(showgrid=True, gridcolor="rgba(128,128,128,0.15)")

st.plotly_chart(fig, use_container_width=True)

fig2 = go.Figure()

fig2.add_trace(go.Bar(
    x=df["timestamp"],
    y=df["total_logs"],
    marker_color=["#E24B4A" if a else "#378ADD" for a in df["is_anomaly"]],
    name="Log volume",
))

fig2.update_layout(
    title="Log volume per minute — red bars = anomaly windows",
    xaxis_title="Time",
    yaxis_title="Log count",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    height=300,
    showlegend=False,
)
fig2.update_xaxes(showgrid=True, gridcolor="rgba(128,128,128,0.15)")
fig2.update_yaxes(showgrid=True, gridcolor="rgba(128,128,128,0.15)")

st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.subheader("Flagged anomaly windows")

display = anomalies[["timestamp","total_logs","error_count","error_rate","anomaly_score"]].copy()
display["error_rate"]    = display["error_rate"].apply(lambda x: f"{x:.1%}")
display["anomaly_score"] = display["anomaly_score"].apply(lambda x: f"{x:.3f}")
display.columns = ["Timestamp","Total logs","Errors","Error rate","Anomaly score"]
display = display.reset_index(drop=True)

st.dataframe(display, use_container_width=True)

st.divider()
st.subheader("All windows")
full = df[["timestamp","total_logs","error_count","error_rate","is_anomaly","anomaly_score"]].copy()
full["error_rate"]    = full["error_rate"].apply(lambda x: f"{x:.1%}")
full["anomaly_score"] = full["anomaly_score"].apply(lambda x: f"{x:.3f}")
full["status"] = full["is_anomaly"].apply(lambda x: "ANOMALY" if x else "normal")
full = full.drop("is_anomaly", axis=1)
full.columns = ["Timestamp","Total logs","Errors","Error rate","Anomaly score","Status"]
full = full.reset_index(drop=True)

st.dataframe(
    full.style.apply(
        lambda row: ["background-color: rgba(226,75,74,0.1)"]*len(row)
        if row["Status"] == "ANOMALY" else [""]*len(row), axis=1
    ),
    use_container_width=True,
)
