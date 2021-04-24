from setuptools import find_packages, setup

setup(
    name='app',
    version='0.1.0',
    python_requires='>=3.6',
    author='Matheus Xavier',
    description='Utility functions',
    packages=find_packages(),
    install_requires=[
        'psutil',
        'requests',
        'loguru',
        'ormar[postgresql]'
    ]
)
