import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.dm_messages = True
intents.presences = True

bot = commands.Bot(
    command_prefix="k.",
    intents=intents
)

async def load_commands():
    base = "src/commands"
    for folder in os.listdir(base):
        folder_path = os.path.join(base, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".py"):
                    await bot.load_extension(
                        f"commands.{folder}.{file[:-3]}"
                    )

async def load_events():
    base = "src/events"
    for file in os.listdir(base):
        if file.endswith(".py"):
            await bot.load_extension(
                f"events.{file[:-3]}"
            )

async def main():
    async with bot:
        await load_commands()
        await load_events()
        await bot.start(TOKEN)

asyncio.run(main())