import discord
import os
from discord.ext import commands
from keep_alive import keep_alive
from dotenv import load_dotenv
import random
from events import load_questions

player_scores = {}
player_streaks = {}

def setup(bot, questions):
    @bot.command(name='q', help='Démarre le quiz et commence à poser des questions.')
    async def start_quiz(ctx):
        if ctx.author.id not in player_scores:
            player_scores[ctx.author.id] = 0
        if ctx.author.id not in player_streaks:
            player_streaks[ctx.author.id] = 0

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
                        player_streaks[ctx.author.id] += 1
                        bonus_points = 0

                        if player_streaks[ctx.author.id] >= 3:
                            streak_bonus = min((player_streaks[ctx.author.id] - 2) * 2, 6)
                            bonus_points = streak_bonus

                        player_scores[ctx.author.id] += points_to_add + bonus_points
                        if player_streaks[ctx.author.id] < 3:
                            await interaction.response.send_message(f" ✅ Bonne réponse! Continuez comme ça !  *+**{points_to_add}**LP 🏆*")
                        else:
                            await interaction.response.send_message(f" ✅ Bonne réponse! Continuez comme ça !  *+**{points_to_add}**LP 🏆* *(+**{bonus_points}**LP bonus de streak) 🔥*")
                    else:
                        player_streaks[ctx.author.id] = 0
                        player_scores[ctx.author.id] = max(0, player_scores[ctx.author.id] - points_to_subtract)
                        await interaction.response.send_message(f" ❌ Mauvaise réponse! La bonne réponse était: ||{correct_answer}||  *-**{points_to_subtract}**LP 🏆*")
                    view.stop()

            button.callback = button_callback
            view.add_item(button)

        await ctx.send(f"Question: {question}", view=view)

    @bot.command(name='sc', help='Affiche le score actuel.')
    async def show_score(ctx):
        if ctx.author.id not in player_scores:
            player_scores[ctx.author.id] = 0
        await ctx.send(f"Votre *ELO* actuel cumule : *{player_scores[ctx.author.id]} LP*")

    @bot.command(name='board', help="Affiche le score de tous les joueurs du serveur")
    async def score_board(ctx):
        if not player_scores: 
            await ctx.send("Aucun score disponible pour le moment.")
            return

        sorted_scores = sorted(player_scores.items(), key=lambda item: item[1], reverse=True)

        leaderboard = "**Tableau des scores :**\n"
        for rank, (player_id, score) in enumerate(sorted_scores, start=1):
            member = await ctx.guild.fetch_member(player_id)
            username = member.display_name if member else f"Utilisateur inconnu ({player_id})"
            leaderboard += f"**#{rank}** - {username}: {score} LP\n"

        await ctx.send(leaderboard)

