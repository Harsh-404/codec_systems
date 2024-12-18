from setuptools import setup, find_packages

setup(
    name='encoding-project',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'typing_extensions',
    ],
    extras_require={
        'dev': [
            'pytest',
            'mypy',
        ],
    },
)