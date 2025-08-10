from enum import Enum
class NewsCategory(str, Enum):
    BUSINESS = "business"
    ENTERTAINMENT = "entertainment"
    GENERAL = "general"
    HEALTH = "health"
    SCIENCE = "science"
    SPORT = "sports"
    TECHNOLOGY = "technology"