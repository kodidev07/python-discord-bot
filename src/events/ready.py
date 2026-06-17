from discord.ext import commands
import discord

class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            status=discord.Status.idle,
            activity=discord.CustomActivity(name="en desarrollo...")
        )

        synced = await self.bot.tree.sync()
        print("---------------------------")
        print(f"Bot conectado: {self.bot.user}")
        print(f"Slash Commands: {len(synced)}")
        print("---------------------------")
        

async def setup(bot):
    await bot.add_cog(Ready(bot))