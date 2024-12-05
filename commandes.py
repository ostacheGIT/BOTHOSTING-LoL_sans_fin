import discord
import os
from discord.ext import commands
from keep_alive import keep_alive
from dotenv import load_dotenv
import random
from events import load_questions

player_scores = {}

def setup(bot, questions):
    @bot.command(name='d', help='Démarre le quiz et commence à poser des questions.')
    async def start_quiz(ctx):
        if ctx.author.id not in player_scores:
            player_scores[ctx.author.id] = 0

        if not questions:
            await ctx.send("Aucune question disponible.")
            return

        # Sélectionner une question aléatoire
        question_data = random.choice(questions)
        question = question_data['question']
        answers = question_data['answers']
        await ctx.send(f"Question: {question}\n1. {answers[0]}\n2. {answers[1]}\n3. {answers[2]}\n4. {answers[3]}")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit() and 1 <= int(m.content) <= 4

        try:
            msg = await bot.wait_for('message', check=check, timeout=30.0)
        except TimeoutError:
            await ctx.send(f"Temps écoulé! Fallait répondre plus vite")
            return

        answer = int(msg.content) - 1
        if question_data['answers'][answer] == question_data['correct_answer']:
            player_scores[ctx.author.id] += 1
            await ctx.send(f"Bonne réponse! Votre score est maintenant: {player_scores[ctx.author.id]}")
        else:
            player_scores[ctx.author.id] = max(0, player_scores[ctx.author.id] - 1)
            await ctx.send(f"Mauvaise réponse! La bonne réponse était: ||{question_data['correct_answer']}||")


    @bot.command(name='sc', help='Affiche le score actuel.')
    async def show_score(ctx):
        if ctx.author.id not in player_scores:
            player_scores[ctx.author.id] = 0
        await ctx.send(f"Votre score actuel est: {player_scores[ctx.author.id]}")