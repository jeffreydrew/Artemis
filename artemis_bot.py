import discord
import random
TOKEN = 'MTA3NDE5NDk5MTU5OTA3MTMwMw.GDlMDz.YHrtENSw9RWbXm-5n78_roOS8Fg66KHuy5Tbvk'

# --------------------------------------------------------------------------------
#                                      Responses
# --------------------------------------------------------------------------------


def handle_responses(message) -> str:
    p_message = message.lower()

    if p_message == "hello":
        return "Hey there!"

    if p_message == "roll":
        return str(random.randint(1, 6))

    if p_message == "!help":
        return "`This is a help message that you can modify`"

    if p_message == "how are you":
        return "I'm doing great, thanks for asking!"

    if p_message == 'update':
        return "I'm currently being updated"


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
