import re
import spacy
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from typing import List

class SensitiveDataRemover:
    def __init__(self):
        # Load spaCy model for NER
        self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize Presidio for PII detection
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        
        # Custom patterns for additional sensitive data
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        }
    
    def clean_text(self, text: str) -> str:
        """Remove sensitive information from text"""
        # Use Presidio for comprehensive PII detection
        results = self.analyzer.analyze(text=text, language='en')
        anonymized_text = self.anonymizer.anonymize(text=text, analyzer_results=results)
        
        # Additional pattern-based cleaning
        cleaned_text = anonymized_text.text
        for pattern_name, pattern in self.patterns.items():
            cleaned_text = re.sub(pattern, f'[{pattern_name.upper()}_REDACTED]', cleaned_text)
        
        # Use spaCy for additional NER-based cleaning
        doc = self.nlp(cleaned_text)
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'ORG', 'GPE']:
                cleaned_text = cleaned_text.replace(ent.text, f'[{ent.label_}_REDACTED]')
        
        return cleaned_text
