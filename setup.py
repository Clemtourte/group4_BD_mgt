from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("bdm_analysis")]

setup(
    name='bdm_analysis',
    version="0.1.0",
    description="Business Data Management Analysis package",
    packages=find_packages(),
    install_requires=requirements,
)
