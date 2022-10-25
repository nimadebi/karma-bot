import discord


class TestForm(discord.ui.Modal, title="test form"):
    answer = discord.ui.TextInput(label="Test input", style=discord.TextStyle.short, placeholder="holdtest",
                                  required=True)

    async def on_submit(self, interaction: discord.Interaction):
        print("succes")


class Identity:
    client = None
    tree = None

    def __init__(self, client, tree):
        self.client = client
        self.tree = tree

    @tree.command(guild=discord.Object(696335510037332020), name="form", description="test form")
    async def modal(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TestForm())
