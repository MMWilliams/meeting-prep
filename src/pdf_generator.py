from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import datetime
from typing import Dict, List, Union

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.create_custom_styles()
    
    def create_custom_styles(self):
        """Create custom styles for the PDF"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1a5276'),
            spaceAfter=30,
            alignment=TA_CENTER,
            leading=32
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubTitle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=20,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#2471a3'),
            spaceBefore=24,
            spaceAfter=12,
            leftIndent=0,
            borderWidth=1,
            borderColor=colors.HexColor('#2471a3'),
            borderPadding=5,
            leading=22
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubSectionHeading',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#2471a3'),
            spaceBefore=16,
            spaceAfter=8,
            leftIndent=10,
            leading=18
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=16
        ))
        
        self.styles.add(ParagraphStyle(
            name='BulletItem',
            parent=self.styles['Normal'],
            fontSize=12,
            leftIndent=20,
            spaceAfter=8,
            leading=16
        ))
        
        self.styles.add(ParagraphStyle(
            name='DictKeyStyle',
            parent=self.styles['Normal'],
            fontSize=13,
            textColor=colors.HexColor('#2471a3'),
            spaceBefore=10,
            spaceAfter=5,
            leftIndent=10,
            leading=16
        ))
    
    def format_content(self, content: Union[str, List, Dict], indent_level: int = 0) -> List:
        """Format different content types into proper PDF elements"""
        story = []
        
        if isinstance(content, dict):
            # Handle dictionary content
            for key, value in content.items():
                if indent_level == 0:
                    story.append(Paragraph(f"<b>{key}</b>", self.styles['SubSectionHeading']))
                else:
                    story.append(Paragraph(f"<b>{key}:</b>", self.styles['DictKeyStyle']))
                
                if isinstance(value, (list, dict)):
                    story.extend(self.format_content(value, indent_level + 1))
                else:
                    story.append(Paragraph(str(value), self.styles['CustomBody']))
        
        elif isinstance(content, list):
            # Handle list content
            for item in content:
                if isinstance(item, (dict, list)):
                    story.extend(self.format_content(item, indent_level + 1))
                else:
                    bullet = "•" if indent_level == 0 else "◦"
                    story.append(Paragraph(f"{bullet} {str(item)}", self.styles['BulletItem']))
        
        else:
            # Handle string/other content
            if not content or str(content).strip() == "":
                return story
            
            # Split by paragraphs for better formatting
            paragraphs = str(content).split('\n\n')
            for paragraph in paragraphs:
                if paragraph.strip():
                    story.append(Paragraph(paragraph, self.styles['CustomBody']))
        
        return story
    
    def create_title_page(self, report: Dict) -> List:
        """Create an attractive title page"""
        story = []
        
        # Title
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("Engineering Meeting Brief", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.25*inch))
        
        # Date
        story.append(Paragraph(
            f"Generated on: {datetime.datetime.now().strftime('%B %d, %Y at %H:%M')}",
            self.styles['SubTitle']
        ))
        
        # Source information
        if 'metadata' in report:
            story.append(Spacer(1, 0.25*inch))
            if 'source_documents' in report['metadata']:
                source_text = f"Based on {report['metadata']['total_documents']} documents"
                story.append(Paragraph(source_text, self.styles['SubTitle']))
            elif 'topic' in report['metadata']:
                topic_text = f"Topic: {report['metadata']['topic']}"
                story.append(Paragraph(topic_text, self.styles['SubTitle']))
        
        # Horizontal line
        story.append(Spacer(1, 0.5*inch))
        line_data = [['']]
        line_table = Table(line_data, colWidths=[6.5*inch])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#2471a3')),
        ]))
        story.append(line_table)
        
        story.append(PageBreak())
        return story
    
    def create_table_of_contents(self, sections: List[str]) -> List:
        """Create a table of contents"""
        story = []
        story.append(Paragraph("Table of Contents", self.styles['SectionHeading']))
        story.append(Spacer(1, 0.25*inch))
        
        for i, section in enumerate(sections, 1):
            toc_item = Paragraph(f"{i}. {section}", self.styles['CustomBody'])
            story.append(toc_item)
        
        story.append(PageBreak())
        return story
    
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
        story.extend(self.create_title_page(report))
        
        # Section order and actual sections present
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
        
        # Filter to only include sections that exist in the report
        available_sections = [section for section in section_order if section in report and report[section]]
        
        # Table of contents
        if len(available_sections) > 3:  # Only add TOC if we have enough sections
            story.extend(self.create_table_of_contents(available_sections))
        
        # Main content
        for section in available_sections:
            story.append(Paragraph(section, self.styles['SectionHeading']))
            content = report[section]
            story.extend(self.format_content(content))
            story.append(Spacer(1, 0.25*inch))
        
        # Footer information
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(
            "This document was automatically generated by the Meeting Prep CLI Tool",
            ParagraphStyle(
                'Footer',
                parent=self.styles['Normal'],
                fontSize=10,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
        ))
        
        # Build PDF
        try:
            doc.build(story)
        except Exception as e:
            print(f"Error creating PDF: {e}")
            raise