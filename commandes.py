import discord
import os
from discord.ext import commands
from keep_alive import keep_alive
from dotenv import load_dotenv
import random 
from events import *

def setup(bot, questions):
    @bot.command(name='d', help='Démarre le quiz et commence à poser des questions.')
    async def start_quiz(ctx):
        if ctx.author.id not in player_scores:
            player_scores[ctx.author.id] = 0
        question = random.choice(questions)
        await ctx.send(f"Question: {question['question']}\n1. {question['answers'][0]}\n2. {question['answers'][1]}\n3. {question['answers'][2]}\n4. {question['answers'][3]}")

    @bot.command(name='a', help='Arrête le quiz en cours.')
    async def stop_quiz(ctx):
        await ctx.send("Quiz arrêté.")

    @bot.command(name='score', help='Affiche le score ELO actuel du joueur.')
    async def show_score(ctx):
        score = player_scores.get(ctx.author.id, 0)
        await ctx.send(f"Votre score ELO actuel est de {score} points.")

    @bot.command(name='lb', help='Affiche le classement des joueurs.')
    async def show_leaderboard(ctx):
        sorted_scores = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)
        leaderboard = "\n".join([f"{ctx.guild.get_member(user_id).name}: {score}" for user_id, score in sorted_scores])
        await ctx.send(f"Classement des joueurs:\n{leaderboard}")

    @bot.command(name='aide', help='Affiche une liste des commandes disponibles.')
    async def show_help(ctx):
        help_text = """
        Commandes disponibles:
        !d - Démarre le quiz et commence à poser des questions.
        !a - Arrête le quiz en cours.
        !score - Affiche le score ELO actuel du joueur.
        !lb - Affiche le classement des joueurs.
        !help - Affiche une liste des commandes disponibles.
        """
        await ctx.send(help_text)