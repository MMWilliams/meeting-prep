from setuptools import setup, find_packages

setup(
    name="meeting-prep",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv",
        "spacy>=3.0.0",
        "presidio-analyzer",
        "presidio-anonymizer",
        "PyPDF2",
        "Pillow",
        "pytesseract",
        "python-pptx",
        "python-docx",
        "chardet",
        "reportlab",
        "rich",
        "tenacity"
    ],
    entry_points={
        'console_scripts': [
            'meeting-prep=src.cli:main',
        ],
    },
    author="Maureese Williamse",
    author_email="maureesewilliams@gmail.com",
    description="A CLI tool for engineers to prepare for meetings by analyzing documents and generating technical briefings",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mmwilliams/meeting-prep",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
