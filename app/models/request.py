from pydantic import  BaseModel
from entities import NewsCategory
class Request(BaseModel):
    category: NewsCategory
    language: str ="en"