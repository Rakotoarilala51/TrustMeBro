from fastapi import APIRouter, HTTPException
from typing import List

from Services.clientAPI import NewsAPIClient
from models.request import NewsRequest
summary_router = APIRouter(prefix="/api/v1/summary", tags=["News"])
news_client = NewsAPIClient()

@summary_router.post("/")
async def get_summary(request: NewsRequest):
    try:
        articles = news_client.get_top_headlines(request)
        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch news: {str(e)}")