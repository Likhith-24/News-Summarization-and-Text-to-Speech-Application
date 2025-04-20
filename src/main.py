import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from src.config import logger  # Absolute import

st.set_page_config(page_title="News Sentiment Analyzer", layout="wide")

def main():
    st.title("🔍 News Sentiment Analyzer")
    st.subheader("Analyze company news sentiment")

    with st.sidebar:
        company_name = st.text_input("Company Name", "Tesla")
        if st.button("Analyze"):
            with st.spinner("Generating Report..."):
                try:
                    response = requests.post(
                        "http://localhost:8000/analyze",
                        json={"company_name": company_name},  # Matches CompanyRequest model
                        timeout=30
                    )
                    response.raise_for_status()
                    st.session_state.report = response.json()
                except requests.exceptions.RequestException as e:
                    st.error(f"Error calling API: {str(e)}")
                    logger.error(f"Streamlit API call failed: {str(e)}")
        
        if "report" in st.session_state:
            sentiment_filter = st.selectbox("Sentiment", ["All", "Positive", "Negative", "Neutral"])
            keyword_filter = st.text_input("Keywords")
            topics = set([t for a in st.session_state.report["articles"] for t in a["topics"]])
            selected_topics = st.multiselect("Topics", list(topics))

    if "report" in st.session_state:
        report = st.session_state.report
        st.header(f"Report for {report['company']}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Positive", report['sentiment_distribution']['Positive'])
        col2.metric("Negative", report['sentiment_distribution']['Negative'])
        col3.metric("Neutral", report['sentiment_distribution']['Neutral'])

        st.write("### Sentiment Distribution")
        df = pd.DataFrame.from_dict(report["sentiment_distribution"], orient="index", columns=["Count"])
        st.bar_chart(df)

        st.write("### Comparative Analysis")
        st.write(f"Common Topics: {', '.join(report['comparative_analysis']['common_topics'])}")
        st.write(f"Unique Positive: {', '.join(report['comparative_analysis']['unique_positive'])}")
        st.write(f"Unique Negative: {', '.join(report['comparative_analysis']['unique_negative'])}")

        st.write("### Word Cloud")
        text = " ".join([a["summary"] for a in report["articles"]])
        wc = WordCloud(width=800, height=400).generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)

        st.write("### Articles")
        filtered = report["articles"]
        if sentiment_filter != "All":
            filtered = [a for a in filtered if a["sentiment"] == sentiment_filter]
        if keyword_filter:
            keywords = keyword_filter.lower().split()
            filtered = [a for a in filtered if all(k in a["summary"].lower() for k in keywords)]
        if selected_topics:
            filtered = [a for a in filtered if any(t in a["topics"] for t in selected_topics)]
        
        for a in filtered:
            with st.expander(a['title']):
                st.write(f"**Summary**: {a['summary']}")
                st.write(f"**Sentiment**: {a['sentiment']}")
                st.write(f"**Topics**: {', '.join(a['topics'])}")
                st.write(f"**Source**: {a['metadata']['source']}")
                st.write(f"**URL**: {a['url']}")

        if report.get('audio_file'):
            st.subheader("Audio Summary (Hindi)")
            st.audio(report['audio_file'])

if __name__ == "__main__":
    main()