import streamlit as st
import requests

st.title("News Sentiment Analysis")

company_name = st.text_input("Enter company name:")

if st.button("Generate Report"):
    if company_name:
        response = requests.post("http://localhost:8000/generate_report", json={"company_name": company_name})
        report = response.json()
        st.write(report)
        st.audio(report["Audio"])
    else:
        st.warning("Please enter a company name.")