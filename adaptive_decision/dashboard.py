import streamlit as st
import pandas as pd

st.title("🔐 AI Login Attack Monitoring Dashboard")

try:
    data = pd.read_json("security_log.json", lines=True)

    st.write("### Login Events")
    st.dataframe(data)

    st.write("### Risk Score Chart")
    st.bar_chart(data["risk_score"])

except:
    st.write("No data available yet. Run test_module4.py first.")