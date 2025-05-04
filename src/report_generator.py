from typing import List, Dict
from openai_manager import OpenAIManager
import datetime

class ReportGenerator:
    def __init__(self):
        self.openai_manager = OpenAIManager()
    
    def generate_from_content(self, documents: List[Dict[str, str]]) -> Dict:
        """Generate report from document content"""
        # Combine all document content
        combined_content = "\n\n".join([
            f"Document: {doc['filename']}\nContent: {doc['content']}"
            for doc in documents
        ])
        
        # Generate report using OpenAI
        report = self.openai_manager.generate_report(combined_content)
        
        # Add metadata
        report['metadata'] = {
            'generated_at': datetime.datetime.now().isoformat(),
            'source_documents': [doc['filename'] for doc in documents],
            'total_documents': len(documents)
        }
        
        return report
    
    def generate_from_topic(self, topic: str) -> Dict:
        """Generate report from a topic query"""
        report = self.openai_manager.generate_report(None, topic)
        
        # Add metadata
        report['metadata'] = {
            'generated_at': datetime.datetime.now().isoformat(),
            'source_type': 'topic_query',
            'topic': topic
        }
        
        return report
