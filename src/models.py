from transformers import pipeline
from TTS.api import TTS
from src.config import Settings  # Absolute import

class Models:
    sentiment_analyzer = pipeline("sentiment-analysis", model=Settings.SENTIMENT_MODEL)
    summarizer = pipeline("summarization", model=Settings.SUMMARIZATION_MODEL)
    translator = pipeline("translation_en_to_hi", model=Settings.TRANSLATION_MODEL)
    tts = TTS(model_name=Settings.TTS_MODEL, progress_bar=False)