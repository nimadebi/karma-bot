import discord
import os
import github_handler
from dotenv import load_dotenv
from discord import ui, app_commands
'''
CHECK IF WALLET IS SLOW TYPE!
CHECK IF DATA IS CORRECT! (wallet length etc)

'''


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


class IdentityForm(discord.ui.Modal):
    account = ""
    github_id = ""
    twitter_id = ""
    identity = {}

    def __init__(self, interaction: discord.Interaction):
        super().__init__(title=f"0L Identity Form: {interaction.user}")
        self.identities = github_handler.get_identities()
        self.discord_id = interaction.user.id
        self.discord_name = str(interaction.user)
        for index, i in enumerate(self.identities):
            if i["details"]["discordId"] == interaction.user.id:
                self.identity_index = index
                self.account = i["account"]
                if "githubId" in i["details"]:
                    self.github_id = i["details"]["githubId"]
                if "twitterId" in i["details"]:
                    self.twitter_id = i["details"]["twitterId"]
                break

        self.account_input = discord.ui.TextInput(label="0L Address (slow wallet!)", style=discord.TextStyle.short,
                                                  placeholder="This should be a slow wallet address!", required=True,
                                                  default=self.account)
        self.github_id_input = discord.ui.TextInput(label="Your Github ID", style=discord.TextStyle.short,
                                                    placeholder="optional", required=False,
                                                    default=self.github_id)
        self.twitter_id_input = discord.ui.TextInput(label="Your Twitter ID", style=discord.TextStyle.short,
                                                     placeholder="optional", required=False,
                                                     default=self.twitter_id)
        self.add_item(self.account_input)
        self.add_item(self.github_id_input)
        self.add_item(self.twitter_id_input)

    async def on_submit(self, interaction: discord.Interaction):
        self.identities[self.identity_index]["account"] = self.account_input.value
        self.identities[self.identity_index]["details"]["discordId"] = self.discord_id
        self.identities[self.identity_index]["details"]["discordName"] = self.discord_name
        if self.github_id_input.value != "":
            self.identities[self.identity_index]["details"]["githubId"] = self.github_id_input.value
        if self.twitter_id_input.value != "":
            self.identities[self.identity_index]["details"]["twitterId"] = self.twitter_id_input.value

        github_handler.push_identities(self.identities)

        await interaction.response.send_message("Thanks for submitting your identity!", ephemeral=True)


@tree.command(guild=discord.Object(696335510037332020), name="account", description="add or update your account")
# TODO: add lock to prevent multiple submissions at the same time.
# TODO: add limit to prevent spamming.
async def modal(interaction: discord.Interaction):
    if not github_handler.is_in_identities(interaction.user.id):
        await interaction.response.send_message("You are not in the list of contributors.", ephemeral=True)
        return
    await interaction.response.send_modal(IdentityForm(interaction))


@tree.command(guild=discord.Object(696335510037332020), name="whitelist", description="whitelist an account")
async def whitelist(interaction: discord.Interaction, account: discord.User):
    """This command is only available to certain people.
    TODO: add support for type 1 accounts (groups)
    TODO: add support for only certain people being able to whitelist accounts.
    TODO: check if account is already in the list."""
    if "Working Groups Key Role" not in [y.name for y in interaction.user.roles]:
        await interaction.response.send_message("You are not allowed to whitelist accounts.", ephemeral=True)
        return
    # await interaction.response.send_message("You can't to use this command.")
    await interaction.response.defer()
    github_handler.add_identity("None", 0, account.id, str(account), None, None)
    await interaction.followup.send(f"We have added {str(account)} to the whitelist.", ephemeral=True)


discord_client.run(os.getenv("discord-key"))
