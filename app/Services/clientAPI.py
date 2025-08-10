import requests
from typing import List, Optional
from models.schemas import News
from models.entities import NewsCategory
from models.request import NewsRequest
from dotenv import load_dotenv
import os

class NewsAPIClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("NEWS_KEY")
    def get_top_headlines(self, request:NewsRequest):
        url = f"{self.base_url}/top-headlines"
        params = {
            "apikey":self.api_key,
            "category":request.category,
            "language":request.language
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            if data["status"] != "ok":
                raise Exception(f"NewsAPI error: {data.get('message', 'Unknown error')}")
            articles = []
            for article_data in data.get("articles", []):
                if self._is_valid_article(article_data):
                    try:
                        article = News(**article_data)
                        articles.append(article)
                    except Exception as e:
                        continue
            return articles
        except requests.Timeout:
            raise Exception("Request timeout while fetching news")
        except requests.HTTPError as e:
            raise Exception(f"HTTP error: {e.response.status_code}")
        except Exception as e:
            raise Exception(f"Failed to fetch news: {str(e)}")
    def _is_valid_article(self, article_data: dict) -> bool:
        required_fields = ["title", "url", "publishedAt"]
        return all(
            article_data.get(field) and
            article_data.get(field) not in ["[Removed]", None, ""]
            for field in required_fields
        )