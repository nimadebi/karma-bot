import discord
import os
import dotenv
from modules.identity import Identity


class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(696335510037332020))  # change after testing to 0L guildID.
            self.synced = True
        print(f"Logged in as {self.user}.")


dotenv.load_dotenv()
discord_client = Client()
tree = discord.app_commands.CommandTree(discord_client)


def main():
    # Modules
    Identity(discord_client, tree)
    # Payment(discord_client, tree)
    discord_client.run(os.getenv("discord-key"))


if __name__ == '__main__':
    main()
