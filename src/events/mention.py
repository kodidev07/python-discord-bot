import discord
from discord.ext import commands

class Mention(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if self.bot.user in message.mentions:
            await message.reply(
                f"{message.author.mention} ¡Hola! 👋 \nRevisa tus mensajes privados.",
            )

            embed = discord.Embed(
                description=(
                    "**Usa** `/help` **para ver todos mis comandos.**"
                ),
                color=discord.Color.yellow()
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url
            )
            embed.set_footer(text="made by kodidev")

            try:
                await message.author.send(embed=embed)
            except discord.Forbidden:
                await message.channel.send(
                    f"{message.author.mention}, no puedo enviarte un mensaje al DM. \nActiva que no filtre mensajes en ``Configuracion de usuario > Contenido y Social > DM``",
                    ephemeral = True
                )

async def setup(bot):
    await bot.add_cog(Mention(bot))