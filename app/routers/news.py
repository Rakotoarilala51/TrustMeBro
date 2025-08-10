from fastapi import APIRouter
import requests
from services.News_Service.News import NewsService
from services.NewsApi import NewsAPIClient, NewsRequest, NewsCategory, Request
router = APIRouter(prefix="/new")
news_client = NewsAPIClient()
@router.get("/")
async def news():
    nouveau = NewsService()
    response = nouveau.fetch_news_by_category("technology", "en")
    return response

@router.post("/")
async def new(request:Request):
    print(request)
    article = news_client.top_headlines(request)
    return "Hello"