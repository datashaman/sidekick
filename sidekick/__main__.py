"""
A simple chatbot that uses the DuckDuckGo API to search the internet for images, news, and weather.
Uses marvin and gradio for the chatbot functionality.
"""
import logging
import os

from typing import Dict, List, Optional

import gradio
import marvin
import requests

from dotenv import load_dotenv
from duckduckgo_search import DDGS
from marvin.beta.assistants import Assistant, Thread


def chat(message, _):
    """Chat with the assistant"""
    message = thread.add(message)
    thread.run(assistant=assistant)
    return thread.get_messages()[-1].content[0].text.value


def images(
    keywords: str,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: Optional[str] = None,
    size: Optional[str] = None,
    color: Optional[str] = None,
    type_image: Optional[str] = None,
    layout: Optional[str] = None,
    license_image: Optional[str] = None,
    max_results: Optional[int] = None,
) -> List[Dict[str, str]]:
    """DuckDuckGo images search. Query params: https://duckduckgo.com/params.

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt", which means worldwide.
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: Day, Week, Month, Year. Defaults to None.
        size: Small, Medium, Large, Wallpaper. Defaults to None.
        color: color, Monochrome, Red, Orange, Yellow, Green, Blue,
            Purple, Pink, Brown, Black, Gray, Teal, White. Defaults to None.
        type_image: photo, clipart, gif, transparent, line.
            Defaults to None.
        layout: Square, Tall, Wide. Defaults to None.
        license_image: any (All Creative Commons), Public (PublicDomain),
            Share (Free to Share and Use), ShareCommercially (Free to Share and Use Commercially),
            Modify (Free to Modify, Share, and Use), ModifyCommercially (Free to Modify, Share, and
            Use Commercially). Defaults to None.
        max_results: max number of results. If None, returns results only from the first response. Defaults to None.

    Returns:
        List of dictionaries with images search results.

    Raises:
        DuckDuckGoSearchException: Base exception for duckduckgo_search errors.
        RatelimitException: Inherits from DuckDuckGoSearchException, raised for exceeding API request rate limits.
        TimeoutException: Inherits from DuckDuckGoSearchException, raised for API request timeouts.
    """
    logger.info(
        "Searching for images: %s, region: %s, safesearch: %s, timelimit: %s, size: %s, color: %s, type_image: %s, layout: %s, license_image: %s, max_results: %s",
        keywords,
        region,
        safesearch,
        timelimit,
        size,
        color,
        type_image,
        layout,
        license_image,
        max_results,
    )
    return ddg.images(
        keywords=keywords,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        size=size,
        color=color,
        type_image=type_image,
        layout=layout,
        license_image=license_image,
        max_results=max_results,
    )


def search(keywords: str, max_results: int = 5) -> list[dict]:
    """Search the internet for the given keywords"""
    logger.info("Searching for: %s, max_results: %s", keywords, max_results)
    return ddg.text(keywords, max_results)


def news(keywords: str, timelimit: str = "w", max_results: int = 5) -> list[dict]:
    """Search the internet for news related to the given keywords, within the given time limit"""
    logger.info(
        "Searching for news: %s, timelimit: %s, max_results: %s",
        keywords,
        timelimit,
        max_results,
    )
    return ddg.news(keywords, timelimit=timelimit, max_results=max_results)


def visit_url(url: str):
    """Fetch the contents of the given URL"""
    logger.info("Visiting URL: %s", url)
    return requests.get(url, timeout=(3,10)).content.decode()


def weather(location: str) -> dict:
    """Get the current weather for the given location"""
    logger.info("Getting weather for: %s", location)
    return ddg.text(f"weather {location}", max_results=1)[0]


load_dotenv()

marvin.settings.openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(
    filename=os.getenv("APP_LOG_FILENAME", "sidekick.log"),
    encoding="utf-8",
    level=getattr(logging, os.getenv("APP_LOG_LEVEL", "INFO").upper()),
)

logger = logging.getLogger(__name__)

assistant_name = os.getenv("APP_ASSISTANT_NAME", "Bob")

assistant = Assistant(
    name=assistant_name,
    instructions=os.getenv(
        "APP_ASSISTANT_INSTRUCTIONS", "You are a helpful AI assistant."
    ),
    tools=[
        images,
        news,
        search,
        visit_url,
        weather,
    ],
)

thread = Thread()

ddg = DDGS()

gradio.ChatInterface(
    fn=chat,
    examples=[
        "Hello",
        "What is the latest news on the war in Ukraine?",
        "What is the weather in Cape Town?",
    ],
    title=f"Chat with {assistant_name}",
).launch()
