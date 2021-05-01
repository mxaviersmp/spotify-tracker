from setuptools import find_packages, setup

with open('requirements.txt') as f:
    DEPENDENCIES = [d.strip() for d in f.readlines()]

setup(
    name='app',
    version='0.1.1',
    python_requires='>=3.8',
    author='Matheus Xavier',
    author_email='matheus.sampaio011@gmail.com',
    description='Packaging of spotify tracker api',
    packages=find_packages(),
    install_requires=DEPENDENCIES
)
