import os

import gradio as gr
import marvin

from dotenv import load_dotenv
from marvin.beta.assistants import Assistant, Thread


load_dotenv()

marvin.settings.openai.api_key = os.getenv("OPENAI_API_KEY")

assistant = Assistant()
thread = Thread()


def chat(message, history):
    message = thread.add(message)
    thread.run(assistant=assistant)
    return thread.get_messages()[-1].content[0].text.value


gr.ChatInterface(chat).launch()
