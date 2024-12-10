import discord
import os
from discord.ext import commands
from keep_alive import keep_alive
from dotenv import load_dotenv
import random
from events import load_questions
import asyncio
from db import get_player_data, update_player_data, get_leaderboard 

player_scores = {}
player_streaks = {}

def setup(bot, questions):
    @bot.command(name='q', help='Démarre le quiz et commence à poser des questions.')
    async def start_quiz(ctx):
        player_id = ctx.author.id

        score, streak = get_player_data(player_id)

        if not questions:
            await ctx.send("Aucune question disponible.")
            return

        def generate_question():
            """Génère une nouvelle question aléatoire."""
            question_data = random.choice(questions)
            question = question_data['question']
            answers = question_data['answers']
            random.shuffle(answers)
            correct_answer = question_data['correct_answer']
            difficulty = question_data['difficulty']
            return question, answers, correct_answer, difficulty

        question, answers, correct_answer, difficulty = generate_question()

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
        quiz_message = await ctx.send("Initialisation du quiz...")

        async def ask_next_question():
            """Met à jour le message avec une nouvelle question."""
            nonlocal question, answers, correct_answer, difficulty
            question, answers, correct_answer, difficulty = generate_question()

            for child in view.children:
                view.remove_item(child)

            for i, answer in enumerate(answers):
                button = discord.ui.Button(label=answer, style=discord.ButtonStyle.primary)

                async def button_callback(interaction, selected_answer=answer):
                    nonlocal streak, score
                    if interaction.user.id == ctx.author.id:
                        if selected_answer == correct_answer:
                            streak += 1
                            bonus_points = 0

                            if streak >= 3:
                                streak_bonus = min((streak - 2) * 2, 6)
                                bonus_points = streak_bonus

                            score += points_to_add + bonus_points
                            feedback = f"✅ Bonne réponse! *+**{points_to_add}**LP 🏆*"
                            if streak >= 3:
                                feedback += f" *(+**{bonus_points}**LP bonus de streak 🔥)*"
                            
                            await interaction.response.edit_message(content=feedback)
                            await asyncio.sleep(2)
                        else:
                            streak = 0
                            score = max(0, score - points_to_subtract)
                            feedback = f"❌ Mauvaise réponse! La bonne réponse était: ||{correct_answer}|| *-**{points_to_subtract}**LP 🏆*"

                            await interaction.response.edit_message(content=feedback)
                            await asyncio.sleep(5)
    
                        # Mettre à jour les scores et streaks dans la base de données
                        update_player_data(player_id, score, streak)

                        await ask_next_question()

                button.callback = button_callback
                view.add_item(button)

            await quiz_message.edit(content=f"Question: {question}", view=view)

        await ask_next_question()

    @bot.command(name='s', help='Affiche le score actuel.')
    async def show_score(ctx):
        player_id = ctx.author.id
        # Récupérer le score du joueur depuis la base de données
        score, _ = get_player_data(player_id)
        await ctx.send(f"Votre *ELO* actuel cumule : *{score} LP*")

    @bot.command(name='b', help="Affiche le score de tous les joueurs du serveur")
    async def score_board(ctx):
        leaderboard = get_leaderboard()

        if not leaderboard: 
            await ctx.send("Aucun score disponible pour le moment.")
            return

        leaderboard_text = "**Tableau des scores :**\n"
        for rank, (player_id, score) in enumerate(leaderboard, start=1):
            member = await ctx.guild.fetch_member(player_id)
            username = member.display_name if member else f"Utilisateur inconnu ({player_id})"
            leaderboard_text += f"**#{rank}** - {username}: {score} LP\n"

        await ctx.send(leaderboard_text)

    @bot.command(name='h', help='Affiche une liste des commandes disponibles.')
    async def show_help(ctx):
        help_text = """
        ```
        Commandes disponibles:
        !h - (Help) Affiche cette liste.
        !q - (Question) Démarre le quiz et commence à poser des questions.
        !s - (Score) Affiche le score ELO actuel du joueur.
        !b - (Board) Affiche le classement des joueurs.
        ```
        """
        await ctx.send(help_text)

