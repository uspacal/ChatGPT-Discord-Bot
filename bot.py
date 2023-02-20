from yaml.loader import SafeLoader
import bot_addin
import openai
import yaml
import discord
import asyncio

with open('config.yaml') as f:
    data = yaml.load(f, Loader=SafeLoader)
openai.api_key = data["keys"]["openai"]
bot_tokens = [
    data["keys"]["discord"]["main"],
]


async def run_client(token):
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user.name}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            await bot_addin.own_message(message)

        elif not message.guild:
            await bot_addin.no_guild(message)

        elif message.content.startswith('&ai'):
            await bot_addin.command_ai(message)

        elif message.content.startswith('&help'):
            await bot_addin.command_help(message)

        elif message.content.startswith('&tos'):
            await bot_addin.command_tos(message)

        elif message.content.startswith('&about'):
            await bot_addin.command_about(message)

        elif message.content.startswith('&status'):
            await bot_addin.command_status(message)

        elif message.content.startswith('&'):
            await bot_addin.command_not_found(message)

        return

    await client.start(token)


async def main():
    tasks = []
    for token in bot_tokens:
        task = asyncio.create_task(run_client(token))
        tasks.append(task)

    await asyncio.gather(*tasks)

asyncio.run(main())
