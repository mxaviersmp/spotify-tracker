from setuptools import find_packages, setup

setup(
    name='utils',
    version='1.0.0',
    python_requires='>=3.6',
    author='Matheus Xavier',
    description='Utility functions',
    packages=find_packages(),
    install_requires=[
        'psutil',
        'requests',
        'loguru'
    ]
)
