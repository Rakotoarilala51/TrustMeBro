import requests
from typing import List, Optional
from models.schemas import News
from models.entities import NewsCategory
from dotenv import load_dotenv
import os

class NewsAPIClient:
    def __init__(self):
        