import discord
import os
import github_handler
from dotenv import load_dotenv
from discord import ui, app_commands


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


load_dotenv()
discord_client = Client()
tree = app_commands.CommandTree(discord_client)


class TestForm(discord.ui.Modal, title="test form"):
    account = discord.ui.TextInput(label="Test input", style=discord.TextStyle.short, placeholder="holdtest",
                                  required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Your answer was {self.account.value}.")


@tree.command(guild=discord.Object(696335510037332020), name="account", description="add or update your account")
async def modal(interaction: discord.Interaction):
    if not github_handler.is_in_identities(interaction.user.id):
        await interaction.response.send_message("You are not in the list of contributors.")
        return
    await interaction.response.send_modal(TestForm())


@tree.command(guild=discord.Object(696335510037332020), name="whitelist", description="whitelist an account")
async def whitelist(interaction: discord.Interaction, account: discord.User):
    """This command is only available to certain people.
    TODO: add support for type 1 accounts (groups)"""
    # await interaction.response.send_message("You are not whitelisted to use this command.")
    github_handler.add_identity("None", 0, account.id, str(account), None, None)
    await interaction.response.send_message(f"We have added {str(account)} to the whitelist.")

discord_client.run(os.getenv("discord-key"))
