import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    raise ValueError("Le token Discord n'est pas défini dans les variables d'environnement.")


bot = discord.Client(intents=discord.Intents.all())
keep_alive()
bot.run(TOKEN)