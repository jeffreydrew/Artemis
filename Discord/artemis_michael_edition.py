import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import discord
from discord import ui, app_commands
from datetime import datetime
from discord_openai_module import *

brownieGamma = os.environ.get("GAMMATOKEN")


class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all(), activity=discord.Game("Terminating Sarah Conner..."))
        self.synced = False  # bot doesn't sync commands more than once
        self.added = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # check if slash commands are synced
            await tree.sync()
            #await tree.sync(guild=discord.Object(id=1074200283598561360))
            self.synced = True
        if not self.added:
            self.add_view(ButtonView())
            self.added = True
        print(f"Logged in as {self.user}")


class ButtonView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Ask another question",
        style=discord.ButtonStyle.gray,
        custom_id="search")
    async def search(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(myModal())


class myModal(ui.Modal, title='Ask another question'):
    response = ui.TextInput(
        label='Question: ',
        style=discord.TextStyle.short,
        placeholder='Where is Sarah Conner?')

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Responding to the question: {str(self.response)}")
        embed = discord.Embed(
            title=self.title,
            description=f"**{self.response.label}**\n{self.response}\n\n**Response:**\n{gpt_query(str(self.response))}",
            timestamp=datetime.now(),
            color=discord.Colour.teal())
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        await interaction.followup.send(embed=embed)
        # await interaction.delete_original_response()


aclient = client()
tree = app_commands.CommandTree(aclient)

# @tree.command(guild=discord.Object(id=1074200283598561360), name='modal',
#               description='Modal for user data')  # guild specific command
# async def modal(interaction: discord.Interaction):
#     await interaction.response.send_message(myModal())

# guild=discord.Object(id=1074200283598561360),
@tree.command(name='askgpt',
              description='Updatable chat with an OpenAI language model')
async def modal(interaction: discord.Interaction, question: str = "What time is it?"):
    await interaction.response.send_message(f"Responding to the question: {str(question)}")
    embed = discord.Embed(title="ChatGPT Response",
                          description=f"**Reply: **\n{gpt_query(question)}",
                          timestamp=datetime.now(),
                          color=discord.Colour.teal())
    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
    await interaction.followup.send(embed=embed, view=ButtonView())
    # await interaction.delete_original_response()


@aclient.event
async def on_message(message):
    if message.author == aclient.user:
        return
    if "words order" in message.content:
        await message.channel.send(message.content)
    elif "each color" in message.content:
        await message.channel.send(message.content)
    elif "emoji" in message.content:
        await message.channel.send(message.content)


aclient.run(brownieGamma)
