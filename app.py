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
    return ddg.text(keywords, max_results)


def news(keywords: str, timelimit: str = "w", max_results: int = 5) -> list[dict]:
    """ Search the internet for news related to the given keywords, within the given time limit"""
    return ddg.news(keywords, timelimit=timelimit, max_results=max_results)


def weather(location: str) -> dict:
    """ Get the current weather for the given location """
    return ddg.text(f"weather {location}", max_results=1)[0]


load_dotenv()

marvin.settings.openai.api_key = os.getenv("OPENAI_API_KEY")

assistant = Assistant(
    name=os.getenv('ASSISTANT_NAME', 'Bob'),
    instructions=os.getenv('ASSISTANT_INSTRUCTIONS', 'You are a helpful AI assistant.'),
    tools=[
        search,
        news,
        weather,
    ]
)

thread = Thread()

ddg = DDGS()

gradio.ChatInterface(chat).launch()
