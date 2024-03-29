import logging
import os

from typing import Dict, List, Optional

import gradio
import marvin

from dotenv import load_dotenv
from duckduckgo_search import DDGS
from marvin.beta.assistants import Assistant, Thread


def chat(message, history):
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
    logger.info(f"Searching for images: {keywords}, region: {region}, safesearch: {safesearch}, timelimit: {timelimit}, size: {size}, color: {color}, type_image: {type_image}, layout: {layout}, license_image: {license_image}, max_results: {max_results}")
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
    """ Search the internet for the given keywords """
    logger.info(f"Searching for: {keywords}, max_results: {max_results}")
    return ddg.text(keywords, max_results)


def news(keywords: str, timelimit: str = "w", max_results: int = 5) -> list[dict]:
    """ Search the internet for news related to the given keywords, within the given time limit"""
    logger.info(f"Searching for news: {keywords}, timelimit: {timelimit}, max_results: {max_results}")
    return ddg.news(keywords, timelimit=timelimit, max_results=max_results)


def weather(location: str) -> dict:
    """ Get the current weather for the given location """
    logger.info(f"Getting weather for: {location}")
    return ddg.text(f"weather {location}", max_results=1)[0]


load_dotenv()

marvin.settings.openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(
    filename=os.getenv('APP_LOG_FILENAME', 'sidekick.log'),
    encoding='utf-8',
    level=getattr(logging, os.getenv('APP_LOG_LEVEL', 'INFO').upper())
)

logger = logging.getLogger(__name__)

assistant_name = os.getenv('APP_ASSISTANT_NAME', 'Bob')

assistant = Assistant(
    name=assistant_name,
    instructions=os.getenv('APP_ASSISTANT_INSTRUCTIONS', 'You are a helpful AI assistant.'),
    tools=[
        images,
        news,
        search,
        weather,
    ]
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
