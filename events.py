import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from keep_alive import keep_alive
import re
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    raise ValueError("Le token Discord n'est pas défini dans les variables d'environnement.")

bot = discord.Client(intents=discord.Intents.all())

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await message.channel.send("salut")

keep_alive()
bot.run(TOKEN)