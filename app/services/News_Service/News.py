from dotenv import load_dotenv
import os
import requests

class News:
    def __init__(self):
        load_dotenv()
        self.news_key = os.getenv("NEWS_KEY")
        self.url = "https://newsapi.org/v2/top-headlines"
        self.headers = {"Authorization": f"Bearer {self.news_key}"}
        self.params = {}
    def fetch_news_by_category(self, category):
        self.params = {"category": category, "language": "en", "apiKey": self.news_key}
        responses = requests.get(self.url, params = self.params, headers= self.headers)
        return responses.json()