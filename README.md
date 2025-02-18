  # Guide d'Installation et Configuration - BDM Project
  ## Introduction
  Ce guide fournit les informations pour installer et configurer l'environnement de développement.

  ## Petit lexique pour débutants
  - Terminal/CMD : La fenêtre noire où on tape des commandes (peut s'ouvrir directement depuis VScode, je recommande d'utiliser cmd et pas powershell, pour naviguer entre les fichiers utiliser "cd projet" par exemple)
  - Repository (repo) : Le dossier du projet partagé sur GitHub
  - Branch : Une version parallèle du code pour travailler sans affecter le projet principal
  - Pull Request (PR) : Demande pour ajouter vos modifications au projet principal
  - Kernel : L'environnement Python qui exécute votre code
  - Environnement virtuel : Un Python isolé pour le projet
  - WSL : Windows Subsystem for Linux - Permet d'utiliser Linux sur Windows
  - direnv : Outil pour charger automatiquement les variables d'environnement
  - pyenv : Gestionnaire de versions Python

  ## Par où commencer ?

  1. Installez d'abord tous les logiciels nécessaires
  2. Familiarisez-vous avec VS Code (ouvrir des fichiers, le terminal)
  3. Suivez les étapes une par une, ne passez pas à la suivante si la précédente ne fonctionne pas
  4. En cas de problème, demander de l'aide

  ## Installation pas à pas
  ### Installations de base
  ### VS Code

  - Télécharger et installer depuis : https://code.visualstudio.com/
  - Lors de l'installation, cocher "Add to PATH"
  - Installer les extensions (Ctrl+Shift+X) :
    - Python
    - Jupyter
    - Remote - WSL (si Windows)
    - GitLens (recommandé)

  ### Python (si pas encore fait)
    - Télécharger la dernière version depuis : https://www.python.org/downloads/
    - **IMPORTANT** : Lors de l'installation, cocher "Add Python to PATH"
    - Vérifier l'installation en ouvrant un terminal (cmd) et taper :
      python --version

  ### Installation et Configuration Git (!!!)\
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
  git config --global user.name "Prenom Nom" (ex git config --global user.name Toto Tata)\
  git config --global user.email "email@utilisé.surgithub" (ex git config --global user.email toto.tata@gmail.com)
  - Vérifier l'installation dans cmd:
      git --version

  ### Configuration selon votre OS (Windows ou Mac)
  ### Pour Windows uniquement - Installation WSL
  https://github.com/dajuca/edhec/blob/main/Windows_virtualization.md
  se référer à ce tuto

  ### Installation des outils de développement
  - Installer pyenv :
  curl https://pyenv.run | bash
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
  echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
  echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
  echo 'eval "$(pyenv init -)"' >> ~/.bashrc
  source ~/.bashrc
  - Installer direnv :
  curl -sfL https://direnv.net/install.sh | bash
  echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
  source ~/.bashrc

  ### Installation du projet
  Dans le terminal Ubuntu :
  git clone https://github.com/Clemtourte/group4_BD_mgt.git
  cd group4_BD_mgt
  pyenv install 3.12.1
  pyenv local 3.12.1
  direnv allow
  pip install -r requirements.txt
  pip install -e .

  ## Navigation de base dans le terminal
- cd nomDuDossier : entre dans un dossier
- cd .. : remonte d'un dossier
- ls : liste les fichiers du dossier actuel
- ctrl+c : arrête une commande en cours
- Flèche haut : retrouve les commandes précédentes

## Note sur les différents terminaux
- CMD: Le terminal Windows classique
- PowerShell: À éviter pour ce projet
- Terminal Ubuntu (WSL): Celui qu'on utilise, reconnaissable par son prompt qui commence par votre nom d'utilisateur@
- Terminal VS Code: S'assurer qu'il est bien en mode "Ubuntu" (visible en haut à droite du terminal)

  ## Workflow quotidien
  ### Au démarrage
- Ouvrir VS Code et un terminal Ubuntu
- Vérifier que vous êtes dans le bon dossier: cd group4_BD_mgt
- Si pas déjà activé (le terminal ne montre pas (env) ou le nom de votre environnement au début) :
  source env/bin/activate    # Le terminal devrait maintenant afficher (env) au début
- Mettre à jour le projet : git checkout main PUIS git pull origin main
- Vérifier que tout fonctionne : make run

### Comment savoir si tout est bien configuré
- Dans le terminal Ubuntu :
  - (env) est visible au début de la ligne
  - direnv: loading .envrc apparaît quand vous entrez dans le dossier
  - pyenv local montre 3.12.1
- Dans VS Code :
  - L'interpréteur Python sélectionné correspond à votre env
  - Pas de soulignements rouges dans les imports

  ### Pourquoi make run ?
  make run est essentiel au début de chaque session de travail car il :
  - Charge les données depuis BigQuery (via load_data.py)
  - Nettoie et prépare les données (via clean_data.py)
  - Exécute toutes les analyses (via main.py)

  C'est important car :
  - Vérifie que votre environnement est bien configuré
  - Assure que vous avez les dernières données
  - Confirme que le pipeline complet fonctionne

  Si make run échoue :
  1. Vérifier que vous êtes dans le bon dossier (cd group4_BD_mgt)
  2. Vérifier que direnv est actif (le terminal doit l'indiquer)
  3. Vérifier les credentials BigQuery (.env bien configuré)
  4. Si l'erreur persiste, regarder la section "Problèmes courants"

  ### Pour travailler
  1. Créer une nouvelle branche :
  - Ouvrir Source Control dans VS Code (Ctrl+Shift+G)
  - Cliquer sur les "..." (trois points)
  - Branch > Create Branch
  - Nommer votre branche selon votre tâche (exemple : "modif_requete_BQ")
  2. Pendant le travail
  - Les fichiers modifiés apparaîtront dans Source Control
  - Pour ajouter des modifications : Cliquer sur le + à côté du fichier
  - Pour commit : Écrire un message décrivant vos modifications puis cliquer sur "Commit"
  - Pour envoyer vos modifications : Cliquer sur "Sync Changes"
  - Si modifs qu'on ne veut pas garder, cliquer sur "stash changes", entrez un message de stash puis appuyez sur entrée 

  ## Structure du projet
  group4_BD_mgt/
  ├── bdm_analysis/           # Package principal
  │   ├── notebooks/         # Notebooks Jupyter
  │   ├── init.py
  │   ├── clean_data.py      # Nettoyage des données
  │   ├── lib.py             # Fonctions utilitaires
  │   ├── load_data.py       # Chargement données BigQuery
  │   └── main.py            # Point d'entrée principal
  ├── .direnv/               # Configuration direnv
  ├── .env                   # Variables d'environnement
  ├── .envrc                # Configuration direnv
  ├── Makefile
  └── setup.py

  ## Configuration BigQuery

  Placer le fichier de credentials dans le projet
  Dans .env, ajouter :
  GOOGLE_APPLICATION_CREDENTIALS="chemin/vers/fichier-credentials.json"

  ## Utilisation du Makefile
  Le plus important :
  make run    # Lance le pipeline complet
  make clean  # Nettoie les fichiers temporaires
  Autres commandes disponibles :

  make install : Installe le package
  make clean : Nettoie les fichiers temporaires
  make load_data : Charge uniquement les données
  make clean_data : Nettoie uniquement les données

  ## Configuration VS Code pour le projet

  1. Sélection de l'interpréteur:
  - Ctrl+Shift+P dans un fichier .py
  - Taper "Python: Select Interpreter"
  - Choisir le python en accord avec l'environnement virtuel


  2. Pour les notebooks :
  - Sélectionner le même kernel que l'interpréteur

  ## Problèmes courants

  - Si erreur WSL : Vérifier que WSL2 est installé
  - Si erreur direnv : Exécuter direnv allow
  - Si erreur BigQuery : Vérifier le chemin du fichier credentials
  - Si imports ne fonctionnent pas : Vérifier que pip install -e . a été exécuté