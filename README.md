# ChatGPT-Discord-Bot

## general
Put bot.py, bot_addin.py and config.yaml in one folder and download the  requirements.

The config.yaml needs to be created and adjusted.

e.g.: `pip3 install yaml`

Run script with: `python3 bot.py` make sure you are in the right directory.

## requirements:
- `yaml`
- `(bot_addin)`
- `openai`
- `yaml`
- `discord`
- `asyncio`
- `transformers`
- `json`
- `datetime`

## config file:
name: config.yaml
content:

```
---
keys:
  openai: <openai_key>
  discord:
    main: <discord_token>
    fluxx: <discord_token2>
...
```
