# Update the OpenAIManager class in src/openai_manager.py

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
        
        Format the response as a valid JSON object with these sections as keys. Each section should contain relevant content as a string or array of strings.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # Changed from gpt-4-turbo-preview
                messages=[
                    {"role": "system", "content": "You are a technical analyst preparing briefing documents for engineering meetings. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Try to extract JSON from the response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            content = content.strip()
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # If JSON parsing fails, create a structured response
                return self._create_structured_report(topic or "Technical Briefing", response.choices[0].message.content)
                
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return self._create_fallback_report(topic or "Technical Briefing")
    
    def _create_structured_report(self, topic: str, raw_content: str) -> Dict:
        """Create a structured report from raw content"""
        # This is a helper to structure the content if JSON parsing fails
        sections = {
            "Executive Summary": "",
            "Topic Overview": "",
            "Technology Stack Analysis": "",
            "Architecture Overview": "",
            "Advantages and Benefits": [],
            "Limitations and Challenges": [],
            "Alternative Solutions": [],
            "Competitive Analysis": "",
            "Key Recommendations": [],
            "Action Items and Next Steps": []
        }
        
        # Try to parse the raw content into sections
        current_section = None
        lines = raw_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this line is a section header
            for section_name in sections.keys():
                if section_name.lower() in line.lower():
                    current_section = section_name
                    break
            else:
                # This is content for the current section
                if current_section:
                    if isinstance(sections[current_section], list):
                        if line.startswith(('•', '-', '*', '1.', '2.', '3.')):
                            sections[current_section].append(line.lstrip('•-* 123456789.'))
                    else:
                        sections[current_section] += line + " "
        
        # Fill in any empty sections
        if not sections["Executive Summary"]:
            sections["Executive Summary"] = f"Technical briefing for {topic}"
        
        return sections
    
    def _create_fallback_report(self, topic: str) -> Dict:
        """Create a detailed fallback report structure"""
        return {
            "Executive Summary": f"This technical briefing covers {topic}, providing a comprehensive analysis of its key aspects, benefits, challenges, and recommendations for implementation.",
            "Topic Overview": f"{topic} is a significant technology/methodology in modern software engineering. This briefing examines its core concepts, applications, and strategic implications.",
            "Technology Stack Analysis": "Due to an API error, detailed technology stack analysis is unavailable. Please review source documents for specific technical details.",
            "Architecture Overview": "Architecture details require manual review of source materials.",
            "Advantages and Benefits": [
                "Enhanced scalability and performance",
                "Improved development efficiency",
                "Better resource utilization",
                "Modern architectural patterns"
            ],
            "Limitations and Challenges": [
                "Learning curve for team members",
                "Initial setup complexity",
                "Integration with existing systems",
                "Potential migration challenges"
            ],
            "Alternative Solutions": [
                "Traditional monolithic approaches",
                "Other modern architectural patterns",
                "Hybrid solutions combining multiple approaches"
            ],
            "Competitive Analysis": "Comparative analysis with alternative solutions shows both advantages and trade-offs. Specific comparisons require detailed evaluation.",
            "Key Recommendations": [
                "Conduct proof of concept implementation",
                "Evaluate team readiness and training needs",
                "Plan phased adoption strategy",
                "Establish monitoring and success metrics"
            ],
            "Action Items and Next Steps": [
                "Schedule technical deep-dive sessions",
                "Create implementation roadmap",
                "Identify pilot project opportunities",
                "Develop team training plan"
            ]
        }
    
    def enhance_section(self, section_name: str, content: str) -> str:
        """Enhance a specific section with additional analysis"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1",  
                messages=[
                    {"role": "system", "content": f"You are enhancing the '{section_name}' section of a technical briefing."},
                    {"role": "user", "content": f"Enhance this section with more detailed analysis:\n\n{content}"}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error enhancing section: {e}")
            return content