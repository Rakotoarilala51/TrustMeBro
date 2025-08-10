import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from typing import List, Optional, Dict, Any
from typing import List, Optional
from models.schemas import News
from models.entities import NewsCategory
from models.request import NewsRequest
from dotenv import load_dotenv
import os
import re
import json

class NewsAPIClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("NEWS_KEY")
        self.base_url = "https://newsapi.org/v2"
    def get_top_headlines(self, request:NewsRequest):
        url = f"{self.base_url}/top-headlines"
        params = {
            "apikey":self.api_key,
            "category":request.category,
            "language":request.language
        }
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            if data["status"] != "ok":
                raise Exception(f"NewsAPI error: {data.get('message', 'Unknown error')}")
            articles = []
            for article_data in data.get("articles", []):
                if self._is_valid_article(article_data):
                    try:
                        article = News(**article_data)
                        articles.append(article)
                    except Exception as e:
                        continue
            return articles
        except requests.Timeout:
            raise Exception("Request timeout while fetching news")
        except requests.HTTPError as e:
            raise Exception(f"HTTP error: {e.response.status_code}")
        except Exception as e:
            raise Exception(f"Failed to fetch news: {str(e)}")
    def _is_valid_article(self, article_data: dict) -> bool:
        required_fields = ["title", "url", "publishedAt"]
        return all(
            article_data.get(field) and
            article_data.get(field) not in ["[Removed]", None, ""]
            for field in required_fields
        )

class GeminiAPIClient:
    def __init__(self, model: str = "gemini-2.0-flash"):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.model = model

        # Initialize the LangChain client
        self.llm = ChatGoogleGenerativeAI(
            model=self.model,
            google_api_key=self.api_key,
            temperature=0.3,
            max_tokens=1024,
            top_p=0.8
        )

    def summarize_articles(self, articles: List[News], category: str, max_length: int = 200) -> Dict[str, Any]:
        """Résume une liste d'articles"""
        if not articles:
            raise ValueError("Articles list cannot be empty")

        # Préparer le contenu des articles
        articles_content = self._prepare_articles_content(articles)

        # Créer le prompt de résumé
        system_prompt = self._create_system_prompt()
        user_prompt = self._create_summary_prompt(articles_content, category, max_length)

        try:
            # Appel à Gemini via LangChain
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]

            response = self.llm.invoke(messages)

            # Parser la réponse
            summary_data = self._parse_response(response.content)

            return {
                "summary": summary_data.get("summary", ""),
                "key_points": summary_data.get("key_points", []),
                "category": category,
                "articles_count": len(articles)
            }

        except Exception as e:
            raise Exception(f"Failed to summarize articles: {str(e)}")

    def _prepare_articles_content(self, articles: List[News]) -> str:
        """Prépare le contenu des articles pour le prompt"""
        content_parts = []

        for i, article in enumerate(articles, 1):
            article_text = f"Article {i}:\n"
            article_text += f"Titre: {article.title}\n"

            if article.description:
                article_text += f"Description: {article.description}\n"

            if article.content:
                # Limiter le contenu pour éviter les limites de tokens
                content = article.content[:300] + "..." if len(article.content) > 300 else article.content
                article_text += f"Contenu: {content}\n"

            article_text += f"Source: {article.source.name}\n"
            article_text += "-" * 50 + "\n"

            content_parts.append(article_text)

        return "\n".join(content_parts)

    def _create_system_prompt(self) -> str:
        """Crée le prompt système"""
        return """Tu es un expert journaliste spécialisé dans la synthèse d'actualités. 
        Ta mission est de créer des résumés clairs, objectifs et informatifs à partir d'articles de presse.

        Règles à suivre:
        - Reste factuel et objectif
        - Identifie les points clés et tendances
        - Évite les répétitions
        - Structure ton analyse de manière logique
        - Réponds UNIQUEMENT en format JSON valide"""

    def _create_summary_prompt(self, articles_content: str, category: str, max_length: int) -> str:
        """Crée le prompt utilisateur pour le résumé"""
        return f"""Analyse ces articles de la catégorie "{category}" et produis un résumé structuré.

Articles à analyser:
{articles_content}

Consignes:
- Résumé principal: maximum {max_length} mots
- Points clés: 3-5 points essentiels
- Focus sur les informations les plus importantes et actuelles

Format de réponse (JSON uniquement):
{{
    "summary": "Ton résumé complet ici...",
    "key_points": [
        "Point clé 1",
        "Point clé 2", 
        "Point clé 3"
    ]
}}"""

    def _parse_response(self, response_content: str) -> Dict[str, Any]:
        """Parse la réponse de Gemini en JSON"""
        try:
            # Essayer de parser directement le JSON
            cleaned_response = self._clean_json_response(response_content)
            return json.loads(cleaned_response)

        except json.JSONDecodeError:
            # Fallback: extraction manuelle
            return self._manual_parse_response(response_content)

    def _clean_json_response(self, response: str) -> str:
        """Nettoie la réponse pour extraire le JSON"""
        # Supprimer les markdown code blocks si présents
        response = re.sub(r'```json\s*', '', response)
        response = re.sub(r'```\s*$', '', response)

        # Trouver le JSON dans la réponse
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json_match.group(0).strip()

        return response.strip()

    def _manual_parse_response(self, response: str) -> Dict[str, Any]:
        """Parse manuel en cas d'échec du JSON"""
        try:
            # Extraire le résumé
            summary_match = re.search(r'"summary":\s*"([^"]*)"', response, re.DOTALL)
            summary = summary_match.group(1) if summary_match else "Résumé non disponible"

            # Extraire les points clés
            key_points = []
            key_points_match = re.search(r'"key_points":\s*\[(.*?)\]', response, re.DOTALL)
            if key_points_match:
                points_text = key_points_match.group(1)
                points = re.findall(r'"([^"]*)"', points_text)
                key_points = points

            if not key_points:
                # Fallback: chercher des bullet points
                bullet_points = re.findall(r'[-•]\s*(.+?)(?=\n|$)', response)
                key_points = bullet_points[:5] if bullet_points else ["Points clés non disponibles"]

            return {
                "summary": summary,
                "key_points": key_points
            }

        except Exception:
            # Fallback ultime
            return {
                "summary": "Erreur lors du parsing du résumé",
                "key_points": ["Erreur lors de l'extraction des points clés"]
            }

    def test_connection(self) -> bool:
        """Test la connexion à Gemini"""
        try:
            test_message = [HumanMessage(content="Dis bonjour en une phrase.")]
            response = self.llm.invoke(test_message)
            return bool(response.content)
        except Exception:
            return False