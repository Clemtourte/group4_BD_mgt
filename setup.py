from setuptools import setup, find_packages

# Lire les dépendances depuis requirements.txt
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip()]

setup(
    name='bdm_analysis',
    version="0.1.0",  # Ajout de la version
    description="Business Data Management Analysis package",
    packages=find_packages(),  # Recherche automatiquement les sous-packages
    install_requires=requirements
)
