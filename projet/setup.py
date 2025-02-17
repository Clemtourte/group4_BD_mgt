from setuptools import setup, find_packages

# list dependencies from file
with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(name='scripts',
      description="package description",
      packages=find_packages(),
      install_requires=requirements)  # Ajout des dépendances