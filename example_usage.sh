#!/bin/bash
# Example usage of the Meeting Prep CLI Tool

# Create example documents directory
mkdir -p example_docs
echo "This is a sample document about cloud architecture" > example_docs/cloud_architecture.txt

# Run the tool with documents
python meeting_prep_cli.py --path ./example_docs --output cloud_brief.pdf --verbose

# Run the tool with a topic
python meeting_prep_cli.py --topic "microservices architecture" --output microservices_brief.pdf

# Run in interactive mode
python meeting_prep_cli.py
