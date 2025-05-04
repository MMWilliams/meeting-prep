from pathlib import Path
from typing import List, Dict
import PyPDF2
from PIL import Image
import pytesseract
from pptx import Presentation
import docx
from sensitive_data import SensitiveDataRemover
from content_extractor import ContentExtractor

class DocumentProcessor:
    def __init__(self, document_path: Path, verbose: bool = False):
        self.document_path = document_path
        self.verbose = verbose
        self.sensitive_data_remover = SensitiveDataRemover()
        self.content_extractor = ContentExtractor()
        self.supported_extensions = ['.pdf', '.txt', '.png', '.jpg', '.jpeg', '.pptx', '.docx']
    
    def process_all(self) -> List[Dict[str, str]]:
        """Process all documents in the given path"""
        documents = []
        for file_path in self.document_path.glob('**/*'):
            if file_path.suffix.lower() in self.supported_extensions:
                if self.verbose:
                    print(f"Processing: {file_path.name}")
                content = self.extract_content(file_path)
                cleaned_content = self.sensitive_data_remover.clean_text(content)
                documents.append({
                    'filename': file_path.name,
                    'content': cleaned_content,
                    'type': file_path.suffix
                })
        return documents
    
    def extract_content(self, file_path: Path) -> str:
        """Extract content based on file type"""
        return self.content_extractor.extract(file_path)
