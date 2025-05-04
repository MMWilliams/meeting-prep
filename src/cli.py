#!/usr/bin/env python3
"""Main CLI entry point for the Meeting Prep Tool"""

import argparse
import os
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from document_processor import DocumentProcessor
from report_generator import ReportGenerator

console = Console()

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Meeting Preparation Tool")
    parser.add_argument("--path", "-p", type=str, help="Path to documents folder")
    parser.add_argument("--topic", "-t", type=str, help="Topic for direct query (no documents)")
    parser.add_argument("--output", "-o", type=str, default="meeting_brief.pdf", help="Output PDF filename")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.path and args.topic:
        console.print("[red]Error:[/red] Please provide either --path or --topic, not both.")
        return
    
    if not args.path and not args.topic:
        # Interactive mode
        choice = Prompt.ask("Choose input method", choices=["documents", "topic"])
        if choice == "documents":
            args.path = Prompt.ask("Enter path to documents folder")
        else:
            args.topic = Prompt.ask("Enter the topic for briefing")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        if args.path:
            # Document-based processing
            task = progress.add_task("Processing documents...", total=100)
            processor = DocumentProcessor(Path(args.path), verbose=args.verbose)
            content = processor.process_all()
            progress.update(task, advance=50)
            
            task2 = progress.add_task("Generating report...", total=100)
            generator = ReportGenerator()
            report = generator.generate_from_content(content)
            progress.update(task2, advance=100)
        else:
            # Topic-based processing
            task = progress.add_task("Generating report from topic...", total=100)
            generator = ReportGenerator()
            report = generator.generate_from_topic(args.topic)
            progress.update(task, advance=100)
        
        # Generate PDF
        task3 = progress.add_task("Creating PDF...", total=100)
        from pdf_generator import PDFGenerator
        pdf_gen = PDFGenerator()
        pdf_gen.create_pdf(report, args.output)
        progress.update(task3, advance=100)
    
    console.print(f"[green]✓[/green] Report generated: {args.output}")

if __name__ == "__main__":
    main()
