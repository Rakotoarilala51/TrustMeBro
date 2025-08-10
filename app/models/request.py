from pydantic import  BaseModel
from entities import NewsCategory
class NewsRequest(BaseModel):
    category: NewsCategory
    language: str ="en"