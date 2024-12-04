# QuizBot LoL - Documentation

## Description du projet
**QuizBot LoL** est un bot Discord conçu pour poser des questions à choix multiples sur le lore de *League of Legends*. Ce quiz sans fin permet aux joueurs de tester leurs connaissances tout en accumulant des points ELO. Ce système reflète leur expertise : plus un joueur a d’ELO, plus il est censé connaître le lore.

## Fonctionnalités principales
- **Quiz sans fin** : le bot pose des questions de manière continue jusqu'à ce que l'utilisateur décide d'arrêter.
- **Questions à choix multiples** : chaque question propose 4 réponses possibles, dont une seule est correcte.
- **Système de points ELO** : les joueurs gagnent ou perdent de l'ELO en fonction de la difficulté de chaque question.
- **Base de données externe** : les questions sont stockées dans un fichier `.txt` pour une gestion simple et une mise à jour rapide.
- **Suivi des scores** : le bot enregistre l’ELO de chaque joueur, affichable à tout moment.

## Prérequis
Avant de commencer, assurez-vous d'avoir :
1. Un compte Discord et un serveur où vous pouvez ajouter le bot.
2. Node.js installé sur votre machine.
3. Une clé d'API Discord récupérée depuis le [portail développeur Discord](https://discord.com/developers/applications).
4. Un fichier `questions.txt` contenant les questions et leurs poids (niveau de difficulté).


### Exemple de `questions.txt`
Chaque ligne contient une question suivie des réponses possibles et d’un poids (de 1 à 5, où 5 est le plus difficile) séparés par un délimiteur (`|`). La bonne réponse est marquée par un astérisque (`*`).

Pour ajouter de nouvelles questions, éditez le fichier questions.txt et suivez le format. Assurez-vous que chaque question est bien formattée avec un poids de difficulté.

### Fonctionnement du système ELO
Le système ELO est utilisé pour refléter la connaissance d’un joueur sur le lore. 
Voici comment cela fonctionne :

*Gain de points :* Le joueur gagne des points en fonction de la difficulté de la question. Une bonne réponse à une question de poids 5 rapporte beaucoup plus qu’une question de poids 1.

*Perte de points :* Le joueur perd des points en cas de mauvaise réponse, également proportionnellement au poids de la question.

### Commandes principales 

Commandes | Description 
 --- | --- 
!d | Démarre le quiz et commence à poser des questions. 
!s | Arrête le quiz en cours.
!s | Affiche le score ELO actuel du joueur.
!lb | Affiche le classement des joueurs.
!help | Affiche une liste des commandes disponibles.
