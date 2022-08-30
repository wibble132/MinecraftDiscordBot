import discord
from discord import app_commands

import constants

MY_GUILD = discord.Object(id=constants.GUILD_ID)


class MinecraftBotClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        # intents.message_content = True  # used to get the contents of all messages

        super(MinecraftBotClient, self).__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

        self.is_running = False

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


client = MinecraftBotClient()


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command()
async def start(interaction: discord.Interaction):
    """Starts the server"""
    if client.is_running:
        await interaction.response.send_message("The server is already running")
        return

    client.is_running = True
    await interaction.response.send_message("Hello!")


@client.tree.command()
async def is_running(interaction: discord.Interaction):
    """Checks to see if the server is running"""
    await interaction.response.send_message("The app is running" if client.is_running else "The app is not running")


@client.tree.command()
async def stop(interaction: discord.Interaction):
    """Stops the server"""
    if not client.is_running:
        await interaction.response.send_message("The server is already stopped")
        return

    client.is_running = False
    await interaction.response.send_message("Stopping server, Goodbye!")


client.run(constants.TOKEN)
