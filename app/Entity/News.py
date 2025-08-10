from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Optional
from datetime import datetime


class News(BaseModel):
    source_id: Optional[str] = Field(None, alias="source.id")
    source_name: str = Field(alias="source.name")
    title: str
    description: Optional[str] = None
    url: HttpUrl
    url_to_image: Optional[HttpUrl] = Field(None, alias="urlToImage")
    published_at: datetime = Field(alias="publishedAt")
    author: Optional[str] = None
    content: Optional[str] = None

    class Config:
        allow_population_by_field_name = True

    @validator('published_at', pre=True)
    def parse_date(cls, v):
        if isinstance(v, str) and v.endswith('Z'):
            v = v.replace('Z', '+00:00')
        return datetime.fromisoformat(v) if isinstance(v, str) else v

    @validator('content')
    def clean_content(cls, v):
        if v and '[+' in v and 'chars]' in v:
            import re
            return re.sub(r'\s*\[\+\d+\s+chars\]$', '', v)
        return v