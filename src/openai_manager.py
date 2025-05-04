import openai
import os
from typing import List, Dict
import json
from tenacity import retry, stop_after_attempt, wait_exponential

class OpenAIManager:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        openai.api_key = self.api_key
        self.client = openai.OpenAI()
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_report(self, content: str, topic: str = None) -> Dict:
        """Generate a comprehensive report using OpenAI API"""
        
        if topic:
            prompt = f"Create a comprehensive technical briefing about: {topic}"
        else:
            prompt = f"Based on the following content, create a comprehensive technical briefing:\n\n{content}"
        
        prompt += """
        
        Please provide a detailed report with the following sections:
        1. Executive Summary
        2. Topic Overview
        3. Technology Stack Analysis
        4. Architecture Overview (if applicable)
        5. Advantages and Benefits
        6. Limitations and Challenges
        7. Alternative Solutions
        8. Competitive Analysis
        9. Key Recommendations
        10. Action Items and Next Steps
        
        Format the response as JSON with these sections as keys.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a technical analyst preparing briefing documents for engineering meetings."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def enhance_section(self, section_name: str, content: str) -> str:
        """Enhance a specific section with additional analysis"""
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": f"You are enhancing the '{section_name}' section of a technical briefing."},
                {"role": "user", "content": f"Enhance this section with more detailed analysis:\n\n{content}"}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content
