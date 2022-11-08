import discord
import os
from dotenv import load_dotenv
from discord.ext import commands


class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents, command_prefix="!")
        self.synced = False

    async def setup_hook(self):
        print(f"\033[31mLogged in as {client.user}\033[39m")
        cogs_folder = f"{os.path.abspath(os.path.dirname(__file__))}/cogs"
        for filename in os.listdir(cogs_folder):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{filename[:-3]}")
        await client.tree.sync()
        print("Loaded cogs")


load_dotenv()
client = Client()
client.run(os.getenv("discord-key"))
