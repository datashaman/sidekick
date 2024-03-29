# sidekick

Chat interface using gradio and marvin.

## installation

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## configuration

```
cp .env.example .env
```

Edit the .env file to your taste. An OpenAI API key is required for the AI assistant to function.

## usage

```
source .venv/bin/activate
python -m sidekick
```

Open https://127.0.0.1:7860 in your browser.

## tools

The AI assistant has access to the following tools:

* images - image search using duckduckgo.com.
* news - news search using duckduckgo.com.
* search - internet search using duckduckgo.com.
* weather - weather search using duckduckgo.com.
