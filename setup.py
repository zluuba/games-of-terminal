#!/usr/bin/env python

from setuptools import setup


NAME = 'Games Of Terminal'
DESCRIPTION = 'Classic games collection for Console'
URL = 'https://github.com/zluuba/games-of-terminal'
EMAIL = 'zluyba.nikitina@gmail.com'
AUTHOR = 'Luybov Nikitina'
REQUIRES_PYTHON = '>=3.11'
VERSION = '0.1.0'

REQUIRED = []
EXTRAS = {}


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    py_modules=['games_of_terminal'],
    entry_points={'got-games': ['games_of_terminal.scripts.app:main']},
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Topic :: Games/Entertainment',
        'Topic :: Terminals',
        'Environment :: Console',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
    ],
)
