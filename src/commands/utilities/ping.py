import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="ping",
        description="🏓 Muestra tu latencia y la del bot."
    )
    @discord.app_commands.allowed_contexts(
        guilds=True,
        dms=True,
        private_channels=True
    )
    async def ping(self, interaction: discord.Interaction):

        # Reply inicial (como "Calculando latencia...")
        await interaction.response.send_message(
            "Calculando latencia...",
            ephemeral=True
        )

        # Mensaje enviado (para medir latencia tipo REST)
        sent = await interaction.original_response()

        latency = round(
            (sent.created_at - interaction.created_at).total_seconds() * 1000
        )

        api_ping = round(self.bot.latency * 1000)

        embed = discord.Embed(
            title="🏓 Pong!",
            color=discord.Color.from_rgb(255, 255, 0),
            timestamp=discord.utils.utcnow()
        )

        embed.add_field(
            name="📡 Latencia general",
            value=f"`{latency} ms`",
            inline=True
        )

        embed.add_field(
            name="🌐 Latencia de la API",
            value=f"`{api_ping} ms`",
            inline=True
        )

        await interaction.edit_original_response(
            content=None,
            embed=embed
        )

async def setup(bot):
    await bot.add_cog(Ping(bot))