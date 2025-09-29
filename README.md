# 🏥 Clinical Note Summarizer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Gemini AI](https://img.shields.io/badge/Powered%20by-Gemini%20AI-orange.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-black.svg)](https://black.readthedocs.io/)

> 🚀 **Transform unstructured clinical notes into structured, actionable medical summaries using Google's Gemini AI**

An intelligent clinical documentation tool that leverages advanced AI to extract key medical information from free-text clinical notes and convert them into standardized JSON format for better data management and analysis.

## ✨ Features

- 🤖 **AI-Powered Summarization**: Uses Google Gemini 2.5 Flash for intelligent text processing
- 📋 **Structured Output**: Converts notes to standardized JSON schema
- 🔄 **Batch Processing**: Process multiple clinical notes simultaneously
- ✅ **Data Validation**: Built-in JSON schema validation for data integrity
- 🛡️ **Error Handling**: Robust error handling with retry mechanisms
- 🔐 **Secure Configuration**: Environment-based API key management
- 📊 **Processing Reports**: Detailed success/failure reporting for each file

## 🏗️ Project Structure

```
clinical-summarizer/
├── 📁 notes/                 # Input clinical notes (*.txt)
│   ├── note1.txt
│   └── note2.txt
├── 📁 output/                # Generated JSON summaries
│   ├── note1.json
│   └── note2.json
├── 📄 summarize_notes.py     # Main application script
├── 📄 requirements.txt       # Python dependencies
├── 📄 .env                   # Environment variables (API keys)
└── 📄 README.md             # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd clinical-summarizer
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env  # Create .env file
   # Edit .env and add your Gemini API key
   ```

5. **Set up your API key**
   
   Edit the `.env` file:
   ```env
   # Gemini API Configuration
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

### Usage

1. **Add clinical notes**
   
   Place your clinical notes (`.txt` files) in the `notes/` directory:
   ```
   notes/
   ├── patient_001.txt
   ├── patient_002.txt
   └── discharge_summary.txt
   ```

2. **Run the summarizer**
   ```bash
   python summarize_notes.py
   ```

3. **View results**
   
   Check the `output/` directory for generated JSON summaries with structured medical data.

## 📋 Output Schema

Each processed clinical note generates a JSON file with the following structure:

```json
{
  "Patient": "John A. Doe, 54 yo male",
  "Diagnosis": "ST-elevation myocardial infarction (STEMI)",
  "Treatment": "Left heart catheterization with stent to LAD. Medications: aspirin 81 mg daily, clopidogrel 75 mg daily, atorvastatin 40 mg nightly, metoprolol tartrate 25 mg BID.",
  "Follow-up": "Follow-up with cardiology in 2 weeks."
}
```

### Schema Fields

| Field | Type | Description |
|-------|------|-------------|
| `Patient` | string | Patient identifier and basic demographics |
| `Diagnosis` | string | Primary diagnosis or condition |
| `Treatment` | string | Treatment plan, medications, and procedures |
| `Follow-up` | string | Follow-up instructions and appointments |

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key | ✅ Yes |

### Model Configuration

The application uses `gemini-2.5-flash` by default. You can modify the model in the `call_gemini_for_json()` function:

```python
def call_gemini_for_json(note_text, model="gemini-2.5-flash"):
    # Function implementation
```

## 🛠️ Advanced Usage

### Custom Processing Directories

```python
# Process notes from custom directories
results = batch_process(
    notes_dir="custom_notes", 
    out_dir="custom_output"
)
```

### Single File Processing

```python
# Process a single clinical note
success, message = summarize_file(
    "path/to/input.txt", 
    "path/to/output.json"
)
```

## 📊 Processing Reports

The application provides detailed processing reports:

```json
{
  "notes/patient_001.txt": {
    "success": true,
    "message": null
  },
  "notes/patient_002.txt": {
    "success": false,
    "message": "Validation error: 'Patient' is a required property"
  }
}
```

## 🐛 Troubleshooting

### Common Issues

**503 Service Unavailable Error**
```
google.genai.errors.ServerError: 503 UNAVAILABLE
```
- **Solution**: The Gemini API service is temporarily unavailable. Wait a few minutes and retry.

**Missing API Key**
```
ValueError: GEMINI_API_KEY not found in environment variables
```
- **Solution**: Ensure your `.env` file contains a valid `GEMINI_API_KEY`.

**JSON Validation Errors**
- **Solution**: The AI response didn't match the expected schema. Check the clinical note content and retry.

### Debug Mode

For detailed error information, you can add logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests: `python -m pytest`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google Gemini AI](https://ai.google.dev/) for providing powerful language models
- [JSONSchema](https://json-schema.org/) for data validation
- The healthcare informatics community for inspiration and best practices

## 📞 Support

- 📧 **Email**: [your-email@example.com](mailto:your-email@example.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-username/clinical-summarizer/issues)
- 📖 **Documentation**: [Wiki](https://github.com/your-username/clinical-summarizer/wiki)

---

<div align="center">

**⭐ If this project helped you, please consider giving it a star! ⭐**

Made with ❤️ for healthcare professionals and developers

[🔝 Back to top](#-clinical-note-summarizer)

</div>
