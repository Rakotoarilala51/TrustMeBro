from dotenv import load_dotenv
import os
import requests

class NewsService:
    def __init__(self):
        load_dotenv()
        self.news_key = os.getenv("NEWS_KEY")
        self.url = "https://newsapi.org/v2/top-headlines"
        self.headers = {"Authorization": f"Bearer {self.news_key}"}
        self.params = {"category":"", "language":"en", "apikey":self.news_key}
    def fetch_news_by_category(self, category, language):
        self.params["category"] = category
        responses = requests.get(self.url, params = self.params, headers= self.headers)
        return responses.json()