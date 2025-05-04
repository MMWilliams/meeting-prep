#!/bin/bash
# Complete project setup script

echo "Setting up Meeting Prep CLI Tool..."

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Copy example .env file
cp .env.example .env
echo "Please edit .env file and add your OpenAI API key"

# Install package in development mode
pip install -e .

echo "Setup complete! Run with: meeting-prep --help"
