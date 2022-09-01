import asyncio
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
        self.is_shutdown: bool = False
        self.is_io_looping: bool = False
        self.is_io_loop_dead: bool = True
        self.channel: Optional[Union[discord.abc.GuildChannel, discord.PartialMessageable, discord.Thread]] = None
        self.minecraft: MinecraftServerController = MinecraftServerController()

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

    async def loop_thread(self):
        print("hello")
        while self.is_io_looping:
            print("hi")
            self.is_io_loop_dead = False
            await asyncio.sleep(2)
            if self.channel is not None:
                message_to_send: str = ""

                while not self.minecraft.outputThread.queue.empty():
                    message_to_send += f"{str(self.minecraft.outputThread.queue.get())[2:-5]}\n"
                while not self.minecraft.errorThread.queue.empty():
                    message_to_send += f"ERROR -- {str(self.minecraft.errorThread.queue.get())[2:-5]}\n"

                if message_to_send != "":
                    print(message_to_send)
                    if self.channel is not None:
                        await self.channel.send(content=message_to_send)
                    else:
                        print("This shouldn't happen")
        print("Stopped main io loop")
        self.is_io_loop_dead = True


client = MinecraftBotClient()
print("1")


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command()
async def start(interaction: discord.Interaction):
    """Starts the server"""
    if client.is_running and not client.is_shutdown:
        await interaction.response.send_message("The server is already running", ephemeral=True)
        return

    await interaction.response.send_message("Starting server...")

    client.is_running = True
    client.channel = client.get_channel(interaction.channel.id)
    client.minecraft.startServer()

    if not client.is_io_looping:
        client.is_io_looping = True
        # small delay just to make sure a dying thread had died
        await asyncio.sleep(0.1)
        if client.is_io_loop_dead:
            asyncio.create_task(client.loop_thread())
    await interaction.channel.send("Started server!")


@client.tree.command()
async def is_running(interaction: discord.Interaction):
    """Checks to see if the server is running"""
    await interaction.response.send_message("The app is running" if client.is_running else "The app is not running",
                                            ephemeral=True)


@client.tree.command()
async def get_status(interaction: discord.Interaction, whisper_result: bool = True):
    match client.minecraft.minecraft_process.poll():
        case None:
            await interaction.response.send_message("The server process is still running")
        case value:
            await interaction.response.send_message(f"The server process has exited with code {value}",
                                                    ephemeral=whisper_result)


@client.tree.command()
async def stop(interaction: discord.Interaction):
    """Stops the server"""
    if not client.is_running:
        await interaction.response.send_message("The server is already stopped", ephemeral=True)
        return

    client.is_running = False
    await interaction.response.send_message("Stopping server")
    return_code = client.minecraft.stopServer()
    await interaction.channel.send(f"Server stopped with code {return_code}")

    client.is_io_looping = False


@client.tree.command()
async def shutdown(interaction: discord.Interaction):
    if client.is_running:
        await interaction.response.send_message("The server is still running, plz stop first")
        return
    client.is_shutdown = True
    await interaction.response.send_message("Shutting down")


@client.event
async def on_message(message: discord.Message):
    # For some reason editing the interaction's message doesn't work
    # So here is this mess
    if message.author.id == client.user.id and message.content == "Shutting down":
        firstloop = True
        while True:
            for i in range(3):
                await asyncio.sleep(1)
                if not firstloop and client.is_io_loop_dead:
                    break
                await message.edit(content=f"{message.content}.")
            if client.is_io_loop_dead:
                break
            await asyncio.sleep(1)
            await message.edit(content="Shutting down")
        await message.edit(content="Shut down")
        await client.close()

    elif client.is_running and message.author.id != client.user.id:
        if client.channel is not None and message.channel.id == client.channel.id:
            print(f"Received {message.content}")
            client.minecraft.inputThread.queue.put(message.content)


print("h")
client.run(constants.TOKEN)
print("3")
