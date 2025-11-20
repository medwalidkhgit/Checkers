# 🎮 Jeu de Dames Multiplateforme

Un jeu de dames moderne développé en Python avec Pygame, offrant une expérience de jeu complète avec plusieurs modes de jeu et une interface utilisateur intuitive.

## ✨ Fonctionnalités

- 🎯 **Multiples modes de jeu**
  - Mode solo contre l'IA
  - Mode multijoueur local
  - Mode en ligne (multijoueur réseau)
  
- 🤖 **IA avec différents niveaux de difficulté**
  - Débutant
  - Intermédiaire
  - Expert
  
- 🎨 **Interface utilisateur moderne**
  - Menu principal intuitif
  - Menu de pause
  - Affichage des coups valides
  - Indicateurs de tour
  - Système de score
  
- 🔊 **Effets sonores**
  - Sons de déplacement
  - Sons d'erreur
  - Retour audio pour une meilleure expérience utilisateur

- 🌐 **Fonctionnalités réseau**
  - Serveur dédié pour le mode en ligne
  - Synchronisation en temps réel
  - Gestion des connexions/déconnexions
  - Système de noms de joueurs

## 🛠️ Technologies utilisées

- Python 3
- Pygame
- Socket (pour le mode en ligne)
- Threading (pour la gestion des connexions réseau)

## 📋 Prérequis

- Python 3
- Pygame
- WebSocket
- Une connexion Internet (pour le mode en ligne)

## 🚀 Installation

### Windows
1. Téléchargez et installez Python 3 depuis [python.org](https://www.python.org/downloads/)
2. Ouvrez l'invite de commande (cmd) et exécutez :
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Mac/Linux
1. Ouvrez le terminal et installez Python 3 si ce n'est pas déjà fait :
```bash
# Pour Mac avec Homebrew
brew install python3

# Pour Linux (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3 python3-pip
```

2. Installez les dépendances :
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## 🎮 Comment jouer

1. Lancez le jeu :
```bash
# Windows
python main.py

# Mac/Linux
python3 main.py
```

2. Dans le menu principal, choisissez votre mode de jeu :
   - Solo vs IA
   - Multijoueur local
   - Mode en ligne

3. Pour le mode en ligne :
   - Lancez d'abord le serveur :
   ```bash
   # Windows
   python server.py

   # Mac/Linux
   python3 server.py
   ```
   - Connectez-vous ensuite avec le client

## 🎯 Contrôles

- **Clic gauche** : Sélectionner/déplacer une pièce
- **Échap** : Menu pause
- **V** : Afficher/masquer les coups valides (aide visuelle pour voir les mouvements possibles)

## 🏗️ Structure du projet

```
├── main.py           # Point d'entrée du jeu
├── server.py         # Serveur pour le mode en ligne
├── classes/          # Classes du jeu
│   ├── ai.py        # Intelligence artificielle
│   ├── board.py     # Plateau de jeu
│   ├── constants.py # Constantes du jeu
│   ├── game.py      # Logique principale du jeu
│   ├── menu.py      # Menus du jeu
│   ├── network.py   # Gestion réseau
│   └── piece.py     # Pièces du jeu
└── assets/          # Ressources (images, sons)
```