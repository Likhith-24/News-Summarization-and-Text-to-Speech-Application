import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

class Settings:
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
    MAX_ARTICLES = 10
    LOG_FILE = 'logs/app.log'
    STATIC_DIR = 'static/audio'
    SENTIMENT_MODEL = 'siebert/sentiment-roberta-large-english'
    SUMMARIZATION_MODEL = 'sshleifer/distilbart-cnn-12-6'
    TRANSLATION_MODEL = 'Helsinki-NLP/opus-mt-en-hi'
    TTS_MODEL = 'tts_models/multilingual/multi-dataset/xtts_v2'  # Multilingual model with Hindi support

    @classmethod
    def configure_logging(cls):
        logger.remove()
        logger.add(cls.LOG_FILE, rotation="10 MB", level="INFO", format="{time} {level} {message}")
        return logger

logger = Settings.configure_logging()