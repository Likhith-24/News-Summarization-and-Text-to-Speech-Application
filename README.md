# News-Summarization-and-Text-to-Speech-Application

This application analyzes news sentiment for a given company using NewsAPI, providing summaries, sentiment scores, topics, and Hindi TTS audio.

## Project Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/news_sentiment_app.git
   cd news_sentiment_app```

2. Install dependencies:
```bash 
pip install -r requirements.txt
```
3. Install spaCy model:
```bash
python -m spacy download en_core_web_sm
```

4. Add your NewsAPI key to .env:
```bash
NEWSAPI_KEY=your_newsapi_key_here
```

5. Run the FastAPI server:
```bash
uvicorn api:app --reload
```

6. Run the Streamlit app:
```bash
streamlit run app.py
```

## Usage
- Open http://localhost:8501 in your browser.
- Enter a company name (e.g., "Tesla") and click "Generate Report".
- View the report and listen to the Hindi audio summary.

## Model Details
- Summarization: sshleifer/distilbart-cnn-12-6
- Sentiment Analysis: siebert/sentiment-roberta-large-english
- Translation: Helsinki-NLP/opus-mt-en-hi
- Text-to-Speech: Google TTS (gTTS)

## API Usage
- Endpoint: /generate_report
- Method: POST
- Input: {"company_name": "example"}
- Output: JSON report with articles, analysis, and audio path

## Assumptions & Limitations
- Requires a NewsAPI key.
- Articles must be in English.
- Hindi translation may have minor inaccuracies.
- Web scraping may fail on some sites due to structure variations.

### Explanation
- Provides clear instructions for setup, usage, and API details.
