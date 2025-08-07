from fastapi import APIRouter
import requests
from services.News_Service.News import News

router = APIRouter(prefix="/news")
@router.get("/")
async def news():
    nouveau = News()
    response = nouveau.fetch_news_by_category("sport")
    return response