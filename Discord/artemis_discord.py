import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import discord
from config import *
from responses import *
from Trader.simple_buy import *

intents = discord.Intents.default()
intents.message_content = True


async def send_message(message, user_message, is_private):
    try:
        response = handle_responses(user_message)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)


def run_artemis():
    token = TOKEN
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} has connected to Discord!")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} sent a message in {channel}: {user_message}")

        if user_message[0] == "?":
            user_message = user_message[1:]
            await send_message(message, user_message, True)
        else:
            await send_message(message, user_message, False)

    client.run(token)

if __name__ == "__main__":
    run_artemis()
