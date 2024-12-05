import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from keep_alive import keep_alive
from events import *
from commandes import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    raise ValueError("Le token Discord n'est pas défini dans les variables d'environnement.")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$', intents=intents)

questions = load_questions('donnees/questions.txt')

setup(bot, questions)

@bot.event
async def on_message(message):
    await on_message(message, bot, questions)



keep_alive()
if __name__ == "__main__":
    bot.run(TOKEN)