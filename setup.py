from setuptools import setup, find_packages
import os

# Read the README file for long description
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# Read requirements.txt for install_requires
with open('requirements.txt', 'r', encoding='utf-8') as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith('#')]

setup(
    name="meeting-prep",
    version="0.1.0",
    packages=find_packages(),
    py_modules=['meeting_prep_cli'],  # Include the CLI module
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'meeting-prep=meeting_prep_cli:main',  # Main executable command
        ],
    },
    author="Maureese Williams",
    author_email="maureesewilliams@gmail.com",
    description="A CLI tool for engineers to prepare for meetings by analyzing documents and generating technical briefings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mmwilliams/meeting-prep",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
    ],
    python_requires='>=3.8',
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.md'],
    },
)