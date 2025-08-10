from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel

from services.NewsApi import NewsAPIClient, NewsRequest, NewsCategory
from services.GeminiAPi import GeminiAPIClient
from Entity.News import News

# Router
news_router = APIRouter(prefix="/api/v1/news", tags=["News"])


# Response ai-models
class NewsResponse(BaseModel):
    articles: List[News]
    total_count: int
    category: str


class SummaryResponse(BaseModel):
    summary: str
    key_points: List[str]
    category: str
    articles_count: int


class FetchAndSummaryRequest(BaseModel):
    category: NewsCategory
    country: str = "us"
    page_size: int = 20
    max_length: int = 200


# Initialize clients
news_client = NewsAPIClient()
gemini_client = GeminiAPIClient()


@news_router.get("/categories")
async def get_categories():
    """Récupère toutes les catégories disponibles"""
    return {
        "categories": [
            {"value": cat.value, "label": cat.value.title()}
            for cat in NewsCategory
        ]
    }


@news_router.post("/fetch", response_model=NewsResponse)
async def fetch_news(request: NewsRequest):
    """Récupère les news par catégorie"""
    try:
        articles = news_client.get_top_headlines(request)

        return NewsResponse(
            articles=articles,
            total_count=len(articles),
            category=request.category.value
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch news: {str(e)}")


@news_router.get("/search")
async def search_news(
        q: str = Query(..., description="Search query"),
        page_size: int = Query(20, ge=1, le=100),
        page: int = Query(1, ge=1)
):
    """Recherche des articles par mots-clés"""
    try:
        articles = news_client.search_everything(
            query=q,
            page_size=page_size,
            page=page
        )

        return {
            "articles": articles,
            "total_count": len(articles),
            "query": q
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@news_router.post("/summarize", response_model=SummaryResponse)
async def summarize_articles(
        articles: List[News],
        category: str,
        max_length: int = Query(200, ge=50, le=500)
):
    """Résume une liste d'articles fournie"""
    try:
        if not articles:
            raise HTTPException(status_code=400, detail="Articles list cannot be empty")

        summary_data = gemini_client.summarize_articles(
            articles=articles,
            category=category,
            max_length=max_length
        )

        return SummaryResponse(**summary_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")


@news_router.post("/fetch-and-summarize", response_model=SummaryResponse)
async def fetch_and_summarize(request: FetchAndSummaryRequest):
    """Récupère et résume les news en une seule requête"""
    try:
        # 1. Récupérer les articles
        news_request = NewsRequest(
            category=request.category,
            page_size=request.page_size
        )

        articles = news_client.get_top_headlines(news_request)

        if not articles:
            raise HTTPException(
                status_code=404,
                detail=f"No articles found for category: {request.category.value}"
            )

        # 2. Résumer les articles
        summary_data = gemini_client.summarize_articles(
            articles=articles,
            category=request.category.value,
            max_length=request.max_length
        )

        return SummaryResponse(**summary_data)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Operation failed: {str(e)}")


@news_router.get("/health")
async def health_check():
    """Vérifie l'état des services"""
    news_status = "OK"
    gemini_status = "OK"

    try:
        # Test NewsAPI (simple check)
        test_request = NewsRequest(
            category=NewsCategory.GENERAL,
            page_size=1
        )
        news_client.get_top_headlines(test_request)
    except:
        news_status = "ERROR"

    try:
        # Test Gemini
        gemini_client.test_connection()
    except:
        gemini_status = "ERROR"

    return {
        "status": "OK" if news_status == "OK" and gemini_status == "OK" else "PARTIAL",
        "services": {
            "news_api": news_status,
            "gemini_api": gemini_status
        }
    }


# Exemple d'usage dans main.py
"""
from fastapi import FastAPI
from routers.news_router import news_router

app = FastAPI(title="TrustMeBro API", version="1.0.0")

# Register router
app.include_router(news_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

# Exemple d'utilisation des endpoints:
"""
# 1. Récupérer des news
POST /api/v1/news/fetch
{
    "category": "technology",
    "country": "us",
    "page_size": 10
}

# 2. Rechercher des articles
GET /api/v1/news/search?q=AI&page_size=15

# 3. Résumer des articles (avec articles fournis)
POST /api/v1/news/summarize
{
    "articles": [...],  // Liste d'articles News
    "category": "technology",
    "max_length": 150
}

# 4. Récupérer et résumer (tout en un)
POST /api/v1/news/fetch-and-summarize
{
    "category": "sports",
    "country": "us",
    "page_size": 20,
    "max_length": 200
}

# 5. Vérifier l'état
GET /api/v1/news/health
"""