import asyncio
import threading
import time
from typing import Union, Optional

import discord
from discord import app_commands

import constants
from minecraftServerController import MinecraftServerController

MY_GUILD = discord.Object(id=constants.GUILD_ID)


class MinecraftBotClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # used to get the contents of all messages

        super(MinecraftBotClient, self).__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

        self.is_running = False
        self.channel: Optional[Union[discord.abc.GuildChannel, discord.PartialMessageable, discord.Thread]] = None
        self.minecraft: MinecraftServerController = MinecraftServerController()
        print("8")
        self.looping: bool = True
        print("9")

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

    # def createLoopThread(self):
    #     print("thread")
    #     loop = asyncio.new_event_loop()
    #     asyncio.run_coroutine_threadsafe(self.loop_thread(), loop)

    async def loop_thread(self):
        print("hello")
        while self.looping:
            print("hi")
            await asyncio.sleep(5)
            if self.channel is not None:
                message_to_send: str = ""
                if not self.minecraft.isRunning():
                    self.channel = None
                while not self.minecraft.outputThread.queue.empty():
                    message_to_send += f"MINECRAFT -- {self.minecraft.outputThread.queue.get()}\n"
                while not self.minecraft.errorThread.queue.empty():
                    message_to_send += f"MINECRAFT_ERROR -- {self.minecraft.errorThread.queue.get()}\n"

                if message_to_send != "":
                    message_to_send = f"Message: {message_to_send}"
                    print(message_to_send)
                    await self.channel.send(content=message_to_send)


client = MinecraftBotClient()
print("1")


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    client.looping = True
    await asyncio.create_task(client.loop_thread())


@client.tree.command()
async def start(interaction: discord.Interaction):
    """Starts the server"""
    if client.is_running:
        await interaction.response.send_message("The server is already running", ephemeral=True)
        return

    client.is_running = True
    client.channel = interaction.channel
    client.minecraft.startServer()
    await interaction.response.send_message("Hello!")


@client.tree.command()
async def is_running(interaction: discord.Interaction):
    """Checks to see if the server is running"""
    await interaction.response.send_message("The app is running" if client.is_running else "The app is not running",
                                            ephemeral=True)


@client.tree.command()
async def stop(interaction: discord.Interaction):
    """Stops the server"""
    if not client.is_running:
        await interaction.response.send_message("The server is already stopped", ephemeral=True)
        return

    client.is_running = False
    client.minecraft.stopServer()
    await interaction.response.send_message("Stopping server, Goodbye!")
    client.looping = False
    await client.close()


@client.event
async def on_message(message: discord.Message):
    if client.is_running and message.author.id != client.user.id:
        if client.channel is not None and message.channel.id == client.channel.id:
            print(f"Received {message.content}")
            client.minecraft.inputThread.queue.put(message.content)


print("h")
client.run(constants.TOKEN)
print("3")
