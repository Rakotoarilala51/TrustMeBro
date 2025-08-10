from fastapi import APIRouter
import requests
from services.News_Service.News import NewsService

router = APIRouter(prefix="/news")
@router.get("/")
async def news():
    nouveau = NewsService()
    response = nouveau.fetch_news_by_category("sport", "en")
    return response