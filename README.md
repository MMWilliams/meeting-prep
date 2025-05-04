# Meeting Prep CLI Tool

A powerful command-line tool designed to help engineers prepare for meetings by automatically analyzing documents and generating comprehensive technical briefings.

## 🚀 Key Benefits

- **Time Savings**: Reduce preparation time from hours to minutes
- **Comprehensive Analysis**: Get detailed technical briefings covering all critical aspects
- **Privacy-First**: Automatic removal of sensitive information before processing
- **Flexible Input**: Process documents or generate reports from topic queries
- **Professional Output**: Receive well-formatted PDF reports ready for review

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Testing](#testing)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The Meeting Prep CLI Tool addresses a common challenge faced by engineers: preparing for technical meetings effectively. Whether you need to review multiple documents about a new technology stack or quickly understand a complex architectural proposal, this tool automates the process of extracting, analyzing, and summarizing technical information.

## ✨ Features

### Document Processing
- **Multi-format Support**: PDF, TXT, DOC/DOCX, PPT/PPTX, and images (JPG, PNG)
- **OCR Capability**: Extract text from images using Tesseract OCR
- **Batch Processing**: Handle multiple documents simultaneously
- **Smart Encoding Detection**: Automatically detect and handle various text encodings

### Privacy & Security
- **PII Detection**: Advanced personal information detection using Presidio
- **NER-based Cleaning**: Named Entity Recognition for identifying sensitive entities
- **Pattern Matching**: Custom regex patterns for common sensitive data formats
- **Local Processing**: Sensitive data removal happens before any external API calls

### AI-Powered Analysis
- **OpenAI Integration**: Leverages GPT-4 for intelligent content analysis
- **Structured Reports**: Generates reports with consistent, professional formatting
- **Context-Aware**: Understands technical content and provides relevant insights
- **Fallback Mechanisms**: Graceful degradation if AI services are unavailable

### Output Generation
- **Professional PDFs**: Clean, well-formatted PDF reports
- **Customizable Sections**: Standard sections for comprehensive coverage
- **Metadata Tracking**: Document sources and generation timestamps
- **Interactive Mode**: User-friendly prompts for easy operation

## 💻 Prerequisites

### System Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Tesseract OCR
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space

### External Dependencies
- OpenAI API key (for AI analysis)
- Internet connection (for API calls)

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/meeting-prep.git
cd meeting-prep
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Unix/macOS:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

### 4. Install Tesseract OCR

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

#### macOS
```bash
brew install tesseract
```

#### Windows
Download from: [Tesseract GitHub Wiki](https://github.com/UB-Mannheim/tesseract/wiki)
Or use: `choco install tesseract` (if using Chocolatey)

### 5. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env  # or use your preferred editor
```

### 6. Install Package (Optional)
```bash
# Install as a development package
pip install -e .

# Now you can run from anywhere
meeting-prep --help
```

## 📖 Usage

### Basic Commands

#### Process Documents
```bash
# Analyze documents in a folder
python meeting_prep_cli.py --path ./documents --output tech_brief.pdf

# With verbose output
python meeting_prep_cli.py --path ./docs --output brief.pdf --verbose
```

#### Generate from Topic
```bash
# Generate report from a topic query
python meeting_prep_cli.py --topic "kubernetes vs docker swarm" --output comparison.pdf
```

#### Interactive Mode
```bash
# Run without arguments for interactive prompts
python meeting_prep_cli.py
```

### Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--path` | `-p` | Path to documents folder | None |
| `--topic` | `-t` | Topic for direct query | None |
| `--output` | `-o` | Output PDF filename | meeting_brief.pdf |
| `--verbose` | `-v` | Enable verbose output | False |
| `--help` | `-h` | Show help message | - |

### Examples

#### 1. Prepare for Architecture Review
```bash
# Process architecture documents
python meeting_prep_cli.py --path ./architecture_docs --output architecture_review.pdf
```

#### 2. Research New Technology
```bash
# Generate briefing on a specific technology
python meeting_prep_cli.py --topic "gRPC vs REST API comparison" --output api_comparison.pdf
```

#### 3. Quick Meeting Prep
```bash
# Interactive mode for quick preparation
python meeting_prep_cli.py
# Then follow the prompts
```

## 🏗️ Architecture

### Project Structure
```
meeting-prep/
├── src/
│   ├── __init__.py
│   ├── cli.py                 # Main CLI interface
│   ├── document_processor.py  # Document handling logic
│   ├── sensitive_data.py      # PII detection and removal
│   ├── content_extractor.py   # Text extraction from various formats
│   ├── openai_manager.py      # OpenAI API integration
│   ├── report_generator.py    # Report generation logic
│   └── pdf_generator.py       # PDF output creation
├── tests/
│   └── test_*.py              # Unit tests
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── README.md                 # This file
└── setup.py                  # Package setup configuration
```

### Core Components

#### 1. ContentExtractor
Handles extraction of text content from various file formats:
- PDF files using PyPDF2
- Word documents using python-docx
- PowerPoint presentations using python-pptx
- Images using Tesseract OCR
- Plain text files with encoding detection

#### 2. SensitiveDataRemover
Implements multi-layer privacy protection:
- Presidio for comprehensive PII detection
- spaCy NER for entity recognition
- Custom regex patterns for specific formats
- Configurable sensitivity levels

#### 3. DocumentProcessor
Orchestrates the document processing pipeline:
- File discovery and validation
- Content extraction
- Sensitive data removal
- Progress tracking

#### 4. OpenAIManager
Manages AI interactions:
- API key management
- Request formatting
- Response parsing
- Error handling and retries
- Fallback mechanisms

#### 5. ReportGenerator
Creates structured reports:
- Content aggregation
- Section organization
- Metadata management
- Topic-based generation

#### 6. PDFGenerator
Produces professional PDF output:
- Custom styling
- Section formatting
- Table of contents
- Page layout management

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_document_processor.py

# Run with coverage
python -m pytest --cov=src tests/
```

### Manual Testing

#### 1. Test Document Processing
```bash
# Create test documents
mkdir test_docs
echo "This is a test document with email: test@example.com" > test_docs/test.txt
echo "Technical content about cloud architecture" > test_docs/tech.txt

# Run the tool
python meeting_prep_cli.py --path ./test_docs --output test_output.pdf --verbose
```

#### 2. Test PII Removal
```bash
# Create document with PII
echo "John Doe, SSN: 123-45-6789, Phone: 555-123-4567" > test_docs/pii_test.txt

# Process and verify PII removal
python meeting_prep_cli.py --path ./test_docs --output pii_test.pdf --verbose
```

#### 3. Test Different File Formats
```bash
# Test with various file types
# Place PDF, DOCX, PPTX files in test directory
python meeting_prep_cli.py --path ./mixed_docs --output format_test.pdf
```

### Integration Testing
```bash
# Test OpenAI integration
python meeting_prep_cli.py --topic "test query" --output api_test.pdf

# Verify PDF generation
python meeting_prep_cli.py --topic "simple test" --output pdf_test.pdf
ls -la pdf_test.pdf  # Verify file creation
```

## ⚙️ Configuration

### Environment Variables
Create a `.env` file with the following variables:
```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
DEBUG=false
LOG_LEVEL=INFO
MAX_CONTENT_LENGTH=10000
PDF_STYLE=professional
```

### Advanced Configuration

#### Custom PII Patterns
Edit `src/sensitive_data.py` to add custom patterns:
```python
self.patterns = {
    'custom_id': r'CUSTOM-\d{8}',
    # Add more patterns as needed
}
```

#### Report Sections
Modify `src/report_generator.py` to customize report sections:
```python
section_order = [
    'Executive Summary',
    'Custom Section',
    # Add or reorder sections
]
```

## 📚 API Documentation

### DocumentProcessor
```python
class DocumentProcessor:
    def __init__(self, document_path: Path, verbose: bool = False)
    def process_all(self) -> List[Dict[str, str]]
```

### ReportGenerator
```python
class ReportGenerator:
    def generate_from_content(self, documents: List[Dict[str, str]]) -> Dict
    def generate_from_topic(self, topic: str) -> Dict
```

### PDFGenerator
```python
class PDFGenerator:
    def create_pdf(self, report: Dict, output_path: str)
```

## 🔍 Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
```

#### 2. SpaCy Model Not Found
```bash
# Download the required model
python -m spacy download en_core_web_sm
```

#### 3. Tesseract Not Found
```bash
# Verify Tesseract installation
tesseract --version

# Install if missing (see Installation section)
```

#### 4. OpenAI API Errors
```bash
# Check API key is set
echo $OPENAI_API_KEY

# Verify .env file
cat .env | grep OPENAI_API_KEY
```

#### 5. PDF Generation Fails
```bash
# Check ReportLab installation
pip install --upgrade reportlab

# Verify write permissions
touch test.pdf && rm test.pdf
```

### Debug Mode
Run with verbose output for debugging:
```bash
python meeting_prep_cli.py --path ./docs --verbose
```

### Log Files
Enable logging by setting environment variables:
```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
python meeting_prep_cli.py --path ./docs
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add unit tests for new features
- Update documentation as needed
- Use type hints where possible
- Add docstrings to all functions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Microsoft Presidio for PII detection
- spaCy for NLP capabilities
- Tesseract OCR for image text extraction
- ReportLab for PDF generation

## 💬 Support

For support, please:
1. Check the [Troubleshooting](#troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/yourusername/meeting-prep/issues)
3. Create a new issue with detailed information

## 🗺️ Roadmap

### Upcoming Features
- [ ] Web interface for easier access
- [ ] Support for additional file formats
- [ ] Custom report templates
- [ ] Integration with calendar systems
- [ ] Automatic meeting notes generation
- [ ] Team collaboration features

### Version History
- v0.1.0 - Initial release with core functionality
- v0.2.0 - Added interactive mode and improved error handling
- v0.3.0 - Enhanced PII detection and custom patterns

---

Made with ❤️ by engineers, for engineers. Happy meeting prep!