import streamlit as st
import pandas as pd

st.title("🔐 AI Login Attack Monitoring Dashboard")

try:
    data = pd.read_json("security_log.json", lines=True)

    # Fix data types
    data["risk_score"] = pd.to_numeric(data["risk_score"], errors="coerce")
    data = data.reset_index(drop=True)

    # 🔥 REMOVE slow attack column (if it exists)
    if "slow_attack_detected" in data.columns:
        data = data.drop(columns=["slow_attack_detected"])

    st.write("### Login Events")
    st.dataframe(data)

    st.write("### Risk Score Chart")

    chart_data = data[["risk_score"]]
    chart_data.index = range(len(chart_data))

    st.line_chart(chart_data)

except:
    st.write("No data available yet. Run test_module4.py first.")