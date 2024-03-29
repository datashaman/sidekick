import logging
import os

import gradio
import marvin

from dotenv import load_dotenv
from duckduckgo_search import DDGS
from marvin.beta.assistants import Assistant, Thread


def chat(message, history):
    message = thread.add(message)
    thread.run(assistant=assistant)
    return thread.get_messages()[-1].content[0].text.value


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
        search,
        news,
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
