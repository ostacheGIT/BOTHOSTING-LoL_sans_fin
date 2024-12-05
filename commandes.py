import discord
import os
from discord.ext import commands
from keep_alive import keep_alive
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    raise ValueError("Le token Discord n'est pas défini dans les variables d'environnement.")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command(
    description='Repeats a message back to the user',
    brief='Repeats a message',
    help='This command takes a message and repeats it back to the user.'
)
async def hello_world(context):
    await context.send("Hello World!")

keep_alive()
if __name__ == "__main__":
    bot.run(TOKEN)