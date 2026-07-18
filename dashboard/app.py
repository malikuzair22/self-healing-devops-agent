import streamlit as st
import requests
import time


st.title("Self-Healing Devops Agent")
response = requests.get("http://api:8080/incidents")
data = response.json()

for incident in data["incidents"]:
    with st.container():
        st.subheader(f"🔍 {incident[2]}")  # diagnosis
        col1, col2 = st.columns(2)
        col1.metric("Confidence", f"{incident[3]*100:.0f}%")
        col2.metric("Action", incident[4])
        status = incident[5]
        if status == "auto-resolved":
            st.success("🟢 Auto-Resolved")
        else:
            st.warning("🟡 Escalated")
        st.divider()

time.sleep(5)
st.rerun()