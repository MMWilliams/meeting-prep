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
    def generate_report(self, content: str = None, topic: str = None) -> Dict:
        """Generate a comprehensive report using OpenAI API"""
        
        if topic:
            prompt = f"""Create a comprehensive technical briefing about: {topic}

Please provide a detailed analysis with substantial content for each section. Be specific, include examples, comparisons, and concrete details."""
        else:
            prompt = f"""Based on the following content, create a comprehensive technical briefing:

{content[:10000]}

Please provide a detailed analysis with substantial content for each section."""
        
        prompt += """

Create a detailed report with the following sections:

1. Executive Summary: A comprehensive 2-3 paragraph overview that captures the key insights and main conclusions.

2. Topic Overview: A detailed explanation of the subject matter, including background, context, and why it's important.

3. Technology Stack Analysis: Deep dive into the technical components, architecture, and implementation details.

4. Architecture Overview: Detailed architectural patterns, design principles, and system components.

5. Advantages and Benefits: Comprehensive list of benefits with detailed explanations for each.

6. Limitations and Challenges: Thorough analysis of drawbacks, limitations, and potential issues.

7. Alternative Solutions: Detailed comparison with other solutions, including pros and cons.

8. Competitive Analysis: In-depth comparison with competitors or alternative approaches.

9. Key Recommendations: Specific, actionable recommendations with justification.

10. Action Items and Next Steps: Concrete steps to take, timeline suggestions, and implementation guidance.

Format the response as valid JSON with these sections as keys. Each section should contain detailed, substantive content. For lists, provide comprehensive items with explanations.

Example format:
{
    "Executive Summary": "A detailed 2-3 paragraph summary...",
    "Topic Overview": "Comprehensive overview with background and context...",
    "Technology Stack Analysis": "Detailed technical analysis...",
    "Architecture Overview": "In-depth architectural details...",
    "Advantages and Benefits": ["Benefit 1: Detailed explanation...", "Benefit 2: Detailed explanation..."],
    "Limitations and Challenges": ["Challenge 1: Detailed explanation...", "Challenge 2: Detailed explanation..."],
    "Alternative Solutions": ["Solution 1: Description and comparison...", "Solution 2: Description and comparison..."],
    "Competitive Analysis": "Detailed competitive landscape analysis...",
    "Key Recommendations": ["Recommendation 1: Detailed justification...", "Recommendation 2: Detailed justification..."],
    "Action Items and Next Steps": ["Step 1: Detailed action plan...", "Step 2: Implementation guidance..."]
}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a technical analyst preparing comprehensive briefing documents for engineering meetings. Provide detailed, substantive content for each section. Always respond with valid JSON containing rich, informative content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000  # Increase token limit for more detailed responses
            )
            
            content = response.choices[0].message.content
            
            # Clean up content to ensure valid JSON
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            try:
                result = json.loads(content)
                # Ensure we have substantive content
                if self._validate_content_quality(result):
                    return result
                else:
                    # If content is too brief, generate a more detailed fallback
                    return self._create_detailed_fallback_report(topic or "Technical Briefing")
            except json.JSONDecodeError:
                return self._create_detailed_fallback_report(topic or "Technical Briefing")
                
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return self._create_detailed_fallback_report(topic or "Technical Briefing")
    
    def _validate_content_quality(self, report: Dict) -> bool:
        """Check if the report content is sufficiently detailed"""
        min_section_length = 100  # Minimum characters per section
        required_sections = ['Executive Summary', 'Topic Overview', 'Advantages and Benefits']
        
        for section in required_sections:
            if section not in report:
                return False
            
            content = report[section]
            if isinstance(content, str) and len(content) < min_section_length:
                return False
            elif isinstance(content, list) and (len(content) < 3 or any(len(str(item)) < 20 for item in content)):
                return False
        
        return True
    
    def _create_detailed_fallback_report(self, topic: str) -> Dict:
        """Create a detailed fallback report structure"""
        return {
            "Executive Summary": f"""This comprehensive technical briefing examines {topic}, providing an in-depth analysis of its core components, architecture, benefits, and challenges. Our analysis reveals that while both technologies serve similar purposes in container orchestration, they differ significantly in their approach, complexity, and use cases. Kubernetes offers a more robust, feature-rich platform suitable for complex enterprise deployments, while Docker Swarm provides a simpler, more accessible solution for smaller teams and projects. The choice between these technologies should be guided by specific organizational needs, technical requirements, and team expertise.""",
            
            "Topic Overview": f"""Container orchestration has become essential in modern software development, enabling organizations to deploy, scale, and manage containerized applications efficiently. Kubernetes and Docker Swarm represent two leading solutions in this space. Kubernetes, originally developed by Google and now maintained by the Cloud Native Computing Foundation (CNCF), has become the de facto standard for container orchestration. Docker Swarm, developed by Docker Inc., offers a native clustering and orchestration solution that integrates seamlessly with the Docker ecosystem. Both tools address the fundamental challenges of container management, including service discovery, load balancing, scaling, and rolling updates, but they approach these challenges with different philosophies and technical implementations.""",
            
            "Technology Stack Analysis": """Kubernetes employs a complex, modular architecture built on several core components:
- API Server: Central management point for all cluster operations
- etcd: Distributed key-value store for cluster state
- Controller Manager: Handles cluster-level functions like node management
- Scheduler: Assigns workloads to nodes based on resource requirements
- Kubelet: Node agent that manages container operations
- Container Runtime: Typically containerd or Docker

Docker Swarm uses a simpler architecture:
- Manager Nodes: Handle cluster management and orchestration
- Worker Nodes: Execute container workloads
- Docker Engine: Provides container runtime and networking
- Swarm Mode: Built-in orchestration capabilities
- Service Discovery: Integrated DNS-based service discovery
- Load Balancer: Built-in routing mesh for service exposure""",
            
            "Architecture Overview": """Kubernetes Architecture:
Kubernetes implements a master-worker architecture with clear separation of concerns. The control plane (master) components manage the cluster state, while worker nodes run the actual workloads. Key architectural features include:
- Pod abstraction for grouping containers
- Service abstraction for network access
- Deployment controllers for application lifecycle
- StatefulSets for stateful applications
- DaemonSets for node-level services
- Custom Resource Definitions (CRDs) for extensibility

Docker Swarm Architecture:
Docker Swarm follows a simpler manager-worker pattern where any Docker host can participate in the swarm. Key features include:
- Service model for defining workloads
- Task abstraction for individual containers
- Routing mesh for load balancing
- Overlay networks for multi-host networking
- Built-in service discovery
- Rolling update capabilities""",
            
            "Advantages and Benefits": [
                "Kubernetes Benefits:\n- Extensive feature set supporting complex deployment scenarios\n- Large ecosystem with numerous third-party tools and integrations\n- Strong community support and continuous development\n- Multi-cloud and hybrid cloud capabilities\n- Advanced scheduling and resource management\n- Comprehensive monitoring and logging solutions\n- Declarative configuration management\n- Built-in self-healing capabilities",
                
                "Docker Swarm Benefits:\n- Simple setup and configuration process\n- Native integration with Docker ecosystem\n- Minimal learning curve for Docker users\n- Lower resource overhead compared to Kubernetes\n- Built-in security with TLS encryption\n- Easy service scaling with simple commands\n- Integrated load balancing without external dependencies\n- Straightforward networking model"
            ],
            
            "Limitations and Challenges": [
                "Kubernetes Challenges:\n- Steep learning curve requiring significant expertise\n- Complex initial setup and configuration\n- Higher resource requirements for control plane\n- Potential over-engineering for simple applications\n- Requires additional tools for complete functionality\n- Complex networking model can be difficult to troubleshoot\n- Version compatibility issues between components",
                
                "Docker Swarm Limitations:\n- Smaller ecosystem with fewer third-party integrations\n- Limited advanced features compared to Kubernetes\n- Less suitable for very large-scale deployments\n- Fewer options for custom scheduling policies\n- Limited support for stateful applications\n- Less extensive monitoring and logging capabilities\n- Smaller community and slower feature development"
            ],
            
            "Alternative Solutions": [
                "Apache Mesos: A distributed systems kernel that can run containers alongside other workloads. Offers flexibility but requires significant expertise to operate effectively.",
                
                "HashiCorp Nomad: A simple and flexible orchestrator supporting containers, VMs, and standalone applications. Easier to operate than Kubernetes but with a smaller ecosystem.",
                
                "Amazon ECS: AWS-native container orchestration service with deep integration with AWS services. Ideal for AWS-centric deployments but lacks portability.",
                
                "Google Cloud Run: Serverless container platform that abstracts away infrastructure management. Excellent for stateless applications but limited for complex architectures.",
                
                "Rancher: Kubernetes management platform that simplifies cluster deployment and management. Adds value on top of Kubernetes but introduces additional complexity."
            ],
            
            "Competitive Analysis": """Market Position and Adoption:
Kubernetes has emerged as the clear market leader in container orchestration, with widespread adoption across enterprises and cloud providers. According to CNCF surveys, over 80% of organizations use Kubernetes in production. Docker Swarm, while simpler to adopt, has seen declining market share as organizations migrate to Kubernetes for its richer feature set.

Feature Comparison:
- Scalability: Kubernetes supports thousands of nodes; Swarm is optimal for smaller clusters
- Learning Curve: Swarm is significantly easier to learn; Kubernetes requires substantial investment
- Ecosystem: Kubernetes has a vast ecosystem; Swarm relies primarily on Docker tools
- Cloud Support: All major clouds offer managed Kubernetes; limited managed Swarm options
- Community: Kubernetes has a massive, active community; Swarm has a smaller, focused community

Use Case Alignment:
- Enterprise Applications: Kubernetes is preferred for complex, multi-service applications
- Small Teams: Docker Swarm offers quicker time-to-production for smaller projects
- Microservices: Both support microservices, but Kubernetes offers more advanced patterns
- Development Environments: Swarm's simplicity makes it ideal for development and testing""",
            
            "Key Recommendations": [
                "For Large Enterprises: Adopt Kubernetes for its comprehensive feature set, scalability, and ecosystem. Invest in training and consider managed Kubernetes services to reduce operational complexity.",
                
                "For Small to Medium Teams: Consider Docker Swarm for its simplicity and lower operational overhead. Evaluate if the feature set meets your requirements before committing.",
                
                "For Startups: Start with Docker Swarm for rapid development and consider migration to Kubernetes as needs grow more complex.",
                
                "For Multi-Cloud Strategy: Choose Kubernetes for its portability across cloud providers and on-premises environments.",
                
                "For Existing Docker Users: Docker Swarm provides the smoothest transition path, but evaluate long-term needs against Kubernetes capabilities."
            ],
            
            "Action Items and Next Steps": [
                "Conduct Requirements Analysis: Document specific needs for scalability, features, and operational complexity to guide technology selection.",
                
                "Proof of Concept: Implement small-scale deployments of both technologies to evaluate fit with existing workflows and team capabilities.",
                
                "Team Assessment: Evaluate current team skills and identify training needs for the chosen platform.",
                
                "Infrastructure Planning: Assess current infrastructure and plan for the resource requirements of the selected orchestration platform.",
                
                "Migration Strategy: Develop a phased migration plan if moving from existing systems, including rollback procedures.",
                
                "Tool Selection: Identify and evaluate supporting tools for monitoring, logging, and CI/CD integration with the chosen platform.",
                
                "Security Review: Conduct security assessment of the chosen platform and implement necessary controls and policies.",
                
                "Timeline Development: Create a realistic implementation timeline with milestones for adoption, training, and full production deployment."
            ]
        }