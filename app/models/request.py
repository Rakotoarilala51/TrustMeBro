from pydantic import  BaseModel
from models.entities import NewsCategory
class NewsRequest(BaseModel):
    category: NewsCategory
    language: str ="en"