from setuptools import find_packages, setup

with open('requirements.txt') as f:
    DEPENDENCIES = [d.strip() for d in f.readlines()]

setup(
    name='app',
    version='1.0.0',
    python_requires='>=3.6',
    author='Matheus Xavier',
    description='Utility functions',
    packages=find_packages(),
    install_requires=DEPENDENCIES
)
