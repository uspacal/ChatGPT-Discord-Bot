from transformers import GPT2Tokenizer
from datetime import datetime
import openai
import json


# log mechanism #
def log(message, response):
    with open("ai_response.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()}; {message.author}; {message.content}; {str(response).encode()}\n")
        print(f"{datetime.now()}; {message.author}; {message.guild}")


# open ai api request #
def open_api_request(text, model="text-davinci-003", temperature=0, max_tokens=4096):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    in_token = tokenizer(text)['input_ids']
    in_token_len = len(in_token)

    response = openai.Completion.create(
        model=model,
        prompt=text,
        temperature=temperature,
        max_tokens=max_tokens - in_token_len
    )
    return json.loads(str(response))


# discord manage messages #
async def dc_reply(message, text):
    if len(text) <= 2000:
        this_message = await message.reply(text)
        return this_message
    else:
        print("dc_reply longtext!")
        await message.reply(text[:2000])
        await dc_reply(message, text[2000:])


async def dc_edit(message, prev_message, text):
    if len(text) <= 2000:
        await message.edit(content=text)
    else:
        print("dc_edit longtext!")
        await message.edit(content=text[:2000])
        await dc_reply(prev_message, text[2000:])


async def dc_send(channel, text):
    if len(text) <= 2000:
        this_message = await channel.send(text)
        return this_message
    else:
        print("dc_send longtext!")
        this_message = await channel.send(text[:2000])
        await dc_reply(this_message, text[2000:])


# commands #
async def own_message(message):
    return


async def no_guild(message):
    text = """Don't slide in my dms!"""
    log(message, "DM")
    await dc_reply(message, text)


async def command_not_found(message):
    text = """I'm sorry, I don't know this command...
Use `&help` to see the full list :)"""
    await dc_reply(message, text)


async def command_ai(message):
    if len(message.content) <= 4:
        await dc_reply(message, "You message is VERY short...")
        return
    try:
        this_message = await dc_reply(message, "Let me think..")
        try:
            response = open_api_request(text=message.content[4:])
            reply = response['choices'][0]['text'].replace("\n\n", "\n").strip()
        except Exception as err:
            print(err)
            response = None
            reply = "openapi error, failed to get response"
        log(message, response)
        await dc_edit(this_message, message, reply)
    finally:
        pass


async def command_help(message):
    text = """Commands:
`&help` -> Shows you this!
`&ai <prompt>` -> Lets you interact with the GPT-3 text AI
`&tos` -> Shows you the usage policy of GPT-3
`&about` -> Shows you the about section.
`&status` -> If this works you might be good..."""
    await dc_reply(message, text)


async def command_custom():
    pass


async def command_tos(message):
    text = """By using this bot you agree to the ToS:
https://beta.openai.com/docs/usage-policies/use-case-policy
We prohibit building products that target the following use-cases:
 - Illegal or harmful industries
 - Misuse of personal data
 - Promoting dishonesty
 - Deceiving or manipulating users
 - Trying to influence politics
It is also not allowed to produce the following content:
https://beta.openai.com/docs/usage-policies/content-policy
Hate, Harassment, Violence, Self-harm, Sexual, Political, Spam, Deception, Malware
"""
    await dc_reply(message, text)


async def command_about(message):
    text = """This discord bot features the GPT-3 model from openai.
By using this bot you agree to the ToS found under `&tos`
This bot was created by Käse. If you want to support me with this project send me a picture of your/ a wiener."""
    await dc_reply(message, text)


async def command_status(message):
    text = "The Bot is up and running!"
    await dc_reply(message, text)


async def command_(message):
    text = ""
    await dc_reply(message, text)
