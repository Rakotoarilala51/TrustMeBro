import requests
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel
from Entity.News import News
from dotenv import load_dotenv
import os
class NewsCategory(str, Enum):
    BUSINESS = "business"
    ENTERTAINMENT = "entertainment"
    GENERAL = "general"
    HEALTH = "health"
    SCIENCE = "science"
    SPORT = "sports"
    TECHNOLOGY = "technology"
class NewsRequest(BaseModel):
    category: NewsCategory
    country: str = "us"
    page_size: int = 20
    page: int = 1
    q: Optional[str] = None
class Request(BaseModel):
    category: NewsCategory
    language: str ="en"
class NewsAPIClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("NEWS_KEY")
        self.base_url = "https://newsapi.org/v2"
    def top_headlines(self, request:Request):
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
                        print(article)
                        print(" ")
                        articles.append(article)
                    except Exception as e:
                        continue
            print(articles)
            return articles
        except requests.Timeout:
            raise Exception("Request timeout while fetching news")
        except requests.HTTPError as e:
            raise Exception(f"HTTP error: {e.response.status_code}")
        except Exception as e:
            raise Exception(f"Failed to fetch news: {str(e)}")
    def get_top_headlines(self, request: NewsRequest) -> List[News]:
        url = f"{self.base_url}/top-headlines"
        params = {
            "apiKey": self.api_key,
            "category": request.category.value,
            "country": request.country,
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

    def search_everything(self, query: str, page_size: int = 20, page: int = 1) -> List[News]:
        url = f"{self.base_url}/everything"
        params = {
            "apiKey": self.api_key,
            "q": query,
            "pageSize": page_size,
            "page": page,
            "sortBy": "publishedAt",
            "language": "en"
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
                    except:
                        continue

            return articles

        except requests.Timeout:
            raise Exception("Request timeout while fetching news")
        except requests.HTTPError as e:
            raise Exception(f"HTTP error: {e.response.status_code}")
        except Exception as e:
            raise Exception(f"Failed to search news: {str(e)}")
    def _is_valid_article(self, article_data: dict) -> bool:
        required_fields = ["title", "url", "publishedAt"]
        return all(
            article_data.get(field) and
            article_data.get(field) not in ["[Removed]", None, ""]
            for field in required_fields
        )


# Usage example:
"""
# Initialisation
news_client = NewsAPIClient(api_key="your_api_key")

# Récupérer les news par catégorie
request = NewsRequest(category=NewsCategory.TECHNOLOGY, page_size=10)
articles = news_client.get_top_headlines(request)

# Rechercher des news
articles = news_client.search_everything("AI technology")
"""