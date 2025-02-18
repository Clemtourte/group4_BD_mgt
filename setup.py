from setuptools import setup

# Lire les dépendances depuis requirements.txt
with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(
    name='bdm_analysis',
    description="Business Data Management Analysis package",
    packages=["bdm_analysis"],
    install_requires=requirements
)