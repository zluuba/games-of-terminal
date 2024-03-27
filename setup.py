#!/usr/bin/env python

from setuptools import setup, find_packages


NAME = 'games-of-terminal'
VERSION = '0.1.0'
DESCRIPTION = 'Classic games collection for Console'
LICENCE = 'MIT'
URL = 'https://github.com/zluuba/games-of-terminal'
AUTHOR = 'Luybov Nikitina'
AUTHOR_EMAIL = 'zluyba.nikitina@gmail.com'
PYTHON_REQUIRES = '>=3.10'

DATA_FILES = [
    ('games_of_terminal', [
        'games_of_terminal/data/achievements.json',
        'games_of_terminal/data/game_statistics.json',
        'games_of_terminal/data/settings.json',
    ]),
]
ENTRY_POINTS = {
    'console_scripts': ['got-games=games_of_terminal.scripts.app:main'],
}
CLASSIFIERS = [
    'Topic :: Games/Entertainment',
    'Topic :: Terminals',
    'Environment :: Console',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
]


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    license=LICENCE,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    include_package_data=True,
    data_files=DATA_FILES,
    entry_points=ENTRY_POINTS,
    python_requires=PYTHON_REQUIRES,
    classifiers=CLASSIFIERS,
)
