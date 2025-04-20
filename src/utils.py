import os
import requests
from typing import List, Dict, Any
from newspaper import Article
from src.models import Models  # Absolute import
from src.config import Settings, logger  # Absolute import
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from collections import Counter

nlp = spacy.load('en_core_web_sm')

class NewsAnalyzer:
    def __init__(self):
        self.nlp = nlp

    def fetch_news_articles(self, company_name: str) -> List[Dict[str, Any]]:
        url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={Settings.NEWS_API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            articles_data = response.json().get('articles', [])
            processed = [self._process_article(a) for a in articles_data[:Settings.MAX_ARTICLES] if self._process_article(a)]
            logger.info(f"Fetched and processed {len(processed)} articles for {company_name}")
            return processed
        except Exception as e:
            logger.error(f"News fetch error: {e}")
            return []

    def _process_article(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            article = Article(article_data['url'])
            article.download()
            article.parse()
            text = article.text or "No Content"
            summary = Models.summarizer(text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
            sentiment = self._analyze_sentiment(text)
            topics = self._extract_topics(text)
            return {
                'title': article.title or "No Title",
                'summary': summary,
                'url': article.url,
                'sentiment': sentiment,
                'topics': topics,
                'metadata': {'source': article_data.get('source', {}).get('name', 'Unknown')}
            }
        except Exception as e:
            logger.warning(f"Article process error: {e}")
            return None

    def _analyze_sentiment(self, text: str) -> str:
        try:
            result = Models.sentiment_analyzer(text[:512])[0]
            return result['label']
        except Exception as e:
            logger.error(f"Sentiment error: {e}")
            return 'Neutral'

    def _extract_topics(self, text: str) -> List[str]:
        try:
            doc = self.nlp(text)
            entities = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'EVENT']]
            tfidf = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf.fit_transform([text])
            feature_names = tfidf.get_feature_names_out()
            top_words = [feature_names[i] for i in tfidf_matrix.toarray().argsort()[0][-5:]]
            return list(set(entities + top_words))
        except Exception as e:
            logger.error(f"Topic error: {e}")
            return []

    def translate_to_hindi(self, text: str) -> str:
        try:
            return Models.translator(text)[0]['translation_text']
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text

    def generate_tts(self, text: str, filename: str) -> str:
        try:
            os.makedirs(Settings.STATIC_DIR, exist_ok=True)
            filepath = os.path.join(Settings.STATIC_DIR, filename)
            Models.tts.tts_to_file(text=text, file_path=filepath, language="hi")  # Specify Hindi for XTTS
            logger.info(f"TTS generated at {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return ''

    def generate_report(self, company_name: str) -> Dict[str, Any]:
        articles = self.fetch_news_articles(company_name)
        if not articles:
            return {"error": "No articles found"}
        
        sentiment_dist = {"Positive": 0, "Negative": 0, "Neutral": 0}
        for a in articles:
            sentiment_dist[a['sentiment']] += 1
        
        all_topics = [t for a in articles for t in a["topics"]]
        common_topics = [t for t, c in Counter(all_topics).most_common(5)]
        pos_topics = set([t for a in articles if a["sentiment"] == "Positive" for t in a["topics"]])
        neg_topics = set([t for a in articles if a["sentiment"] == "Negative" for t in a["topics"]])
        unique_pos = list(pos_topics - neg_topics)[:3]
        unique_neg = list(neg_topics - pos_topics)[:3]
        
        summary = f"{company_name}: {sentiment_dist['Positive']} positive, {sentiment_dist['Negative']} negative, {sentiment_dist['Neutral']} neutral articles."
        hindi_summary = self.translate_to_hindi(summary)
        audio_file = self.generate_tts(hindi_summary, f"{company_name}_summary.mp3")
        
        return {
            'company': company_name,
            'articles': articles,
            'sentiment_distribution': sentiment_dist,
            'comparative_analysis': {
                'common_topics': common_topics,
                'unique_positive': unique_pos,
                'unique_negative': unique_neg
            },
            'summary': summary,
            'audio_file': audio_file
        }