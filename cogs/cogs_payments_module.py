import discord
from discord import ui, app_commands
from discord.ext import commands
from util import github_util


class Payments(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="payment", description="manually add a payment")
    async def payment(self, interaction: discord.Interaction, account: discord.User):
        """This command is only available to Working Groups Key Roles."""
        if "Working Groups Key Role" not in [y.name for y in interaction.user.roles]:
            await interaction.response.send_message("You are not allowed to add payments.", ephemeral=True)
            return
        await interaction.response.send_modal(PaymentForm(interaction, discord_name=str(account)))


class PaymentButton(ui.Button):
    def __init__(self):
        super().__init__(label="Pay now", style=discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):
        # get the content of the message that this button belongs to
        message = await interaction.channel.fetch_message(interaction.message.id)
        # the content should contain:
        # - the issue link
        # - the bounty amount
        # - the account (and/or user) to pay
        # - the task description
        discord_name = message.content.split(",")[0]
        bounty = message.content.split(",")[1]
        issue_link = message.content.split(",")[2]
        task_description = message.content.split(",")[3]

        await interaction.response.defer()
        await interaction.response.send_modal(
            PaymentForm(interaction, discord_name, bounty, issue_link, task_description))
        await interaction.followup.send("Payment sent!", ephemeral=True)


class PaymentForm(ui.Modal):
    def __init__(self, interaction: discord.Interaction, discord_name=None, bounty=None, issue_link=None,
                 task_description=None):
        super().__init__(title=f"0L Payment Form: {interaction.user}")
        self.discord_name = discord_name
        self.bounty = bounty
        self.issue_link = issue_link
        self.task_description = task_description
        self.identity = github_util.get_identity(discord_name)
        if self.identity is None:
            self.address = ""

        self.discord_name_field = discord.ui.TextInput(label="Discord Name", default=self.discord_name,
                                                       style=discord.TextStyle.short, required=False)
        self.account_field = discord.ui.TextInput(label="0L Address", style=discord.TextStyle.short,
                                                  placeholder="The recipient", required=True,
                                                  default=self.address, min_length=32, max_length=32)
        self.amount_field = discord.ui.TextInput(label="Bounty amount", style=discord.TextStyle.short,
                                                 placeholder="optional", required=True,
                                                 default=self.bounty)
        self.issue_link_field = discord.ui.TextInput(label="The issue link", style=discord.TextStyle.short,
                                                     placeholder="optional", required=False,
                                                     default=self.issue_link)
        self.task_description_field = discord.ui.TextInput(label="Task description", style=discord.TextStyle.long,
                                                           placeholder="short task description", required=False,
                                                           default=self.task_description)
        self.memo_field = discord.ui.TextInput(label="Memo", style=discord.TextStyle.short,
                                               placeholder="optional", required=False,
                                               default="")
        self.tx_hash_field = discord.ui.TextInput(label="Transaction hash", style=discord.TextStyle.long,
                                                  placeholder="TX HASH", required=True)

        self.add_item(self.account_field)
        self.add_item(self.amount_field)
        self.add_item(self.task_description_field)
        self.add_item(self.issue_link_field)

    async def on_submit(self, interaction: discord.Interaction):
        """This function is called when the user submits the form."""
        payments = github_util.get_payments()
        payment = {
            "address": self.account_field.value,
            "discord_name": self.discord_name,
            "issue_link": self.issue_link_field.value,
            "task_description": self.task_description_field.value,
            "amount": self.amount_field.value,
            "memo": self.memo_field.value,
            "tx_hash": self.tx_hash_field.value
        }
        payments.append(payment)
        github_util.push_payments(payments)

        await interaction.response.send_message(f"Bounty has been paid: {self.bounty} GAS to {self.discord_name}",
                                                ephemeral=False)


async def setup(client):
    print("Payments module loaded.")
    await client.add_cog(Payments(client), guild=discord.Object(696335510037332020))
