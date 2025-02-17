# group4_BD_mgt

# Guide d'Installation et Configuration - BDM Project

## Petit lexique pour débutants
- Terminal/CMD : La fenêtre noire où on tape des commandes (peut s'ouvrir directement depuis VScode, je recommande d'utiliser cmd et pas powershell, pour naviguer entre les fichiers utiliser "cd projet" par exemple)
- Repository (repo) : Le dossier du projet partagé sur GitHub
- Branch : Une version parallèle du code pour travailler sans affecter le projet principal
- Pull Request (PR) : Demande pour ajouter vos modifications au projet principal
- Kernel : L'environnement Python qui exécute votre code
- Environnement virtuel : Un Python isolé pour le projet

## Par où commencer ?
1. Installez d'abord tous les logiciels nécessaires
2. Familiarisez-vous avec VS Code (ouvrir des fichiers, le terminal)
3. Suivez les étapes une par une, ne passez pas à la suivante si la précédente ne fonctionne pas
4. En cas de problème, contactez l'équipe !

## Prérequis - À installer avant tout
1. Visual Studio Code (VS Code)
  - Télécharger et installer depuis : https://code.visualstudio.com/
  - Lors de l'installation, cocher "Add to PATH"

2. Python (si pas encore fait)
  - Télécharger la dernière version depuis : https://www.python.org/downloads/
  - **IMPORTANT** : Lors de l'installation, cocher "Add Python to PATH"
  - Vérifier l'installation en ouvrant un terminal (cmd) et taper :
    python --version

3. Installation et Configuration Git (!!!)\
Télécharger et installer depuis : https://git-scm.com/downloads
Pendant l'installation :
   - Cliquer "Next" sur toutes les options par défaut
   - À la fin, cocher "Launch Git Bash" 
   - Cliquer "Finish"
Vérifier l'installation :
   - Ouvrir CMD (touche Windows, taper "cmd", Enter)
   - Taper : git --version
   - Si vous voyez une version, l'installation est réussie !
Connexion à votre compte GitHub
- Créer un compte sur github.com si pas déjà fait
- Dans CMD, configurer Git avec votre compte :\
git config --global user.name "Votre Nom" (ex git config --global user.name Toto Tata)\
git config --global user.email "email@utilisé.surgithub" (ex git config --global user.email toto.tata@gmail.com)
- Vérifier l'installation dans cmd:
    git --version

4. Installer virtualenv
   - Ouvrir un terminal
   - Exécuter :
     pip install virtualenv
   - Vérifier l'installation :
     virtualenv --version

5. Extensions VS Code requises
  - Ouvrir VS Code
  - Aller dans Extensions (Ctrl+Shift+X)
  - Installer :
    - Python
    - Jupyter
    - GitLens (optionnel mais plus que recommandé)
    - Github copilot (gratuit quand étudiant)

## Collaboration avec Git/GitHub

### Configuration initiale
#### Configuration de base (à faire une seule fois)
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"

git clone https://github.com/Clemtourte/group4_BD_mgt/
cd group4_BD_mgt/projet

## Workflow en travaillant
1. Avant de commencer à travailler
   - Ouvrir Source Control dans VS Code (Ctrl+Shift+G) sur le coté gauche de vscode
   - Cliquer sur les "..." (trois points)
   - Sélectionner "Checkout to..." > "main"
   - Cliquer sur "Sync Changes" (↻) pour récupérer les dernières modifications
   - Cliquer sur les "..." > "Branch" > "Create Branch" pour créer votre branche de travail
   - Nommer votre branche selon votre tâche (exemple : "modif_requete_BQ")

2. Pendant le travail
   - Les fichiers modifiés apparaîtront dans Source Control
   - Pour voir les modifications : cliquer sur le fichier
   - Pour ajouter des modifications (équivalent git add) :
     * Cliquer sur le + à côté du fichier pour l'ajouter
     * Ou cliquer sur le + à côté de "Changes" pour tout ajouter
   - Pour commit :
     * Écrire un message décrivant vos modifications dans la zone de texte en haut
     * Cliquer sur Commit au-dessus
   - Pour envoyer vos modifications :
     * Cliquer sur "Sync Changes"

3. Pour créer une Pull Request
   - Dans Source Control
   - Cliquer sur "Create Pull Request" (apparaît après le push)
   - Suivre les instructions pour créer la PR sur GitHub

## Environnement Python
### Création de l'environnement virtuel
Dans cmd :
python -m venv env

Puis pour l'activer (sur windows dans cmd de VSCode, pas dans powershell):
env\scripts\activate.bat

## Installation des dépendances
Dans cmd (avec env activé):
pip install -r requirements.txt
pip install -e .  # Pour installer le package en mode développement

## Config BQ
1. Créer fichier .env à la racine
Ecrire dedans :
GOOGLE_APPLICATION_CREDENTIALS="chemin/vers/votre/fichier-credentials.json"

2. Ajouter au .gitignore si pas déja fait au clone du repo: (!!)
.env
*.json
env/
__pycache__/

## Structure du projet
projet/
├── scripts/
│   ├── __init__.py
│   └── lib.py
├── notebooks/
├── env/
├── setup.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

## Config VSCode
1. Sélection de l'interpréteur:
-Ctrl+Shift+P
-"Python: Select Interpreter"
-Choisir l'environnement du projet (env)

2. Config des notebooks
Sélectionner le meme kernel qui correpond a l'environnement virtuel (env)

### Vérification finale
Après installation, vous devriez voir :
- (env) au début de votre ligne de terminal
- Le bon interpréteur sélectionné dans VS Code
- Tous les imports qui fonctionnent dans le notebook test

## Tests d'installation
### Tests des imports
Dans le notebook test run:
from scripts.lib import who_am_i
who_am_i()

### Test BigQuery
Dans le notebook test vérifier que la requête run

## Problèmes courants
- Si imports ne fonctionnent pas : vérifier que pip install -e . a bien été exécuté
- Si kernel non trouvé : redémarrer VS Code
- Si erreur BigQuery : vérifier le chemin dans .env
