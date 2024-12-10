import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from keep_alive import keep_alive
import re
import random

def load_questions(file_path):
    questions = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 7:  
                    question = parts[0]
                    answers = parts[1:5]
                    try:
                        correct_answer_index = int(parts[5]) - 1  
                        difficulty = int(parts[6])
                        if not (1 <= difficulty <= 5): 
                            raise ValueError(f"Difficulté invalide: {difficulty}")
                        questions.append({
                            'question': question,
                            'answers': answers,
                            'correct_answer': answers[correct_answer_index],
                            'difficulty': difficulty 
                        }) 
                    except ValueError as e:
                        print(f"Erreur de conversion : {e} pour la ligne : {line.strip()}")
                else:
                    print(f"Ligne incorrecte : {line.strip()}")
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} n'existe pas.")
    except Exception as e:
        print(f"Erreur lors du chargement des questions : {e}")

    print(f"{len(questions)} questions chargées.")
    return questions