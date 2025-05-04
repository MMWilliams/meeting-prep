from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import datetime
from typing import Dict

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.create_custom_styles()
    
    def create_custom_styles(self):
        """Create custom styles for the PDF"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#2E3440')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        ))
    
    def create_pdf(self, report: Dict, output_path: str):
        """Create a formatted PDF from the report data"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # Title page
        story.append(Paragraph("Engineering Meeting Brief", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(
            f"Generated on: {datetime.datetime.now().strftime('%B %d, %Y %H:%M')}",
            self.styles['Normal']
        ))
        
        if 'metadata' in report:
            if 'source_documents' in report['metadata']:
                story.append(Paragraph(
                    f"Based on {report['metadata']['total_documents']} documents",
                    self.styles['Normal']
                ))
            elif 'topic' in report['metadata']:
                story.append(Paragraph(
                    f"Topic: {report['metadata']['topic']}",
                    self.styles['Normal']
                ))
        
        story.append(PageBreak())
        
        # Add each section from the report
        section_order = [
            'Executive Summary',
            'Topic Overview',
            'Technology Stack Analysis',
            'Architecture Overview',
            'Advantages and Benefits',
            'Limitations and Challenges',
            'Alternative Solutions',
            'Competitive Analysis',
            'Key Recommendations',
            'Action Items and Next Steps'
        ]
        
        for section in section_order:
            if section in report:
                story.append(Paragraph(section, self.styles['SectionHeading']))
                content = report[section]
                
                if isinstance(content, list):
                    for item in content:
                        story.append(Paragraph(f"• {item}", self.styles['CustomBody']))
                else:
                    for paragraph in content.split('\n\n'):
                        if paragraph.strip():
                            story.append(Paragraph(paragraph, self.styles['CustomBody']))
                
                story.append(Spacer(1, 0.25*inch))
        
        # Build PDF
        doc.build(story)
