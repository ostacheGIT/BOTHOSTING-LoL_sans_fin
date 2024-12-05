import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from keep_alive import keep_alive
import re
import random

# Charger les questions depuis le fichier questions.txt
def load_questions(file_path):
    questions = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) == 6:
                question = parts[0]
                answers = parts[1:5]
                correct_answer = answers[int(parts[5]) - 1]
                weight = int(parts[5])
                questions.append({
                    'question': question,
                    'answers': answers,
                    'correct_answer': correct_answer,
                    'weight': weight
                })
    return questions

# Scores des joueurs
player_scores = {}

# Fonction pour calculer les points ELO
def calculate_elo_points(weight, is_correct):
    if is_correct:
        return weight * 10
    else:
        return -weight * 5

async def on_message(message, bot, questions):
    if message.author.bot:
        return
    if message.content.isdigit() and 1 <= int(message.content) <= 4:
        user_answer = int(message.content) - 1
        question = random.choice(questions)
        if question['answers'][user_answer] == question['correct_answer']:
            points = calculate_elo_points(question['weight'], True)
            player_scores[message.author.id] += points
            await message.channel.send(f"Bonne réponse! Vous gagnez {points} points.")
        else:
            points = calculate_elo_points(question['weight'], False)
            player_scores[message.author.id] += points
            await message.channel.send(f"Mauvaise réponse! Vous perdez {-points} points.")
    await bot.process_commands(message)