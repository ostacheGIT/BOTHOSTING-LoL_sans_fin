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
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 6:  # Vérifie que la ligne contient bien 6 champs
                    question = parts[0]
                    answers = parts[1:5]
                    correct_answer = answers[int(parts[5]) - 1]  # Index de la bonne réponse
                    weight = int(parts[5])  # Niveau de difficulté (poids)
                    questions.append({
                        'question': question,
                        'answers': answers,
                        'correct_answer': correct_answer,
                        'weight': weight
                    })
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} n'existe pas.")
    except Exception as e:
        print(f"Erreur lors du chargement des questions : {e}")
    
    print(f"{len(questions)} questions chargées.")
    return questions


# Scores des joueurs
player_scores = {}

# Fonction pour calculer les points ELO
def calculate_elo_points(weight, is_correct):
    if is_correct:
        return weight * 10
    else:
        return -weight * 5

async def handle_message(message, bot, questions):
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
