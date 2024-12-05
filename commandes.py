import discord
import os
from discord.ext import commands
from keep_alive import keep_alive
from dotenv import load_dotenv
import random
from events import load_questions

player_scores = {}

def setup(bot, questions):
    @bot.command(name='q', help='Démarre le quiz et commence à poser des questions.')
    async def start_quiz(ctx):
        if ctx.author.id not in player_scores:
            player_scores[ctx.author.id] = 0

        if not questions:
            await ctx.send("Aucune question disponible.")
            return

        question_data = random.choice(questions)
        question = question_data['question']
        answers = question_data['answers']
        correct_answer = question_data['correct_answer']
        difficulty = question_data['difficulty']
        
        points_rules = {
        1: {'add': 5, 'subtract': 25},
        2: {'add': 10, 'subtract': 20},
        3: {'add': 15, 'subtract': 15},
        4: {'add': 20, 'subtract': 10},
        5: {'add': 25, 'subtract': 5}
        }
        points_to_add = points_rules[difficulty]['add']
        points_to_subtract = points_rules[difficulty]['subtract']

        view = discord.ui.View()
        for i, answer in enumerate(answers):
            button = discord.ui.Button(label=answer, style=discord.ButtonStyle.primary)
            
            async def button_callback(interaction, selected_answer=answer):
                if interaction.user.id == ctx.author.id:
                    if selected_answer == correct_answer:
                        player_scores[ctx.author.id] += points_to_add
                        await interaction.response.send_message(f" ✅ Bonne réponse! Continuez comme ça !  *+{points_to_add}LP*")
                    else:
                        player_scores[ctx.author.id] = max(0, player_scores[ctx.author.id] - points_to_subtract)
                        await interaction.response.send_message(f" ❌ Mauvaise réponse! La bonne réponse était: ||{correct_answer}||  *-{points_to_subtract}LP*")
                    view.stop()

            button.callback = button_callback
            view.add_item(button)

        await ctx.send(f"Question: {question}", view=view)



    @bot.command(name='sc', help='Affiche le score actuel.')
    async def show_score(ctx):
        if ctx.author.id not in player_scores:
            player_scores[ctx.author.id] = 0
        await ctx.send(f"Votre score actuel est: {player_scores[ctx.author.id]}")