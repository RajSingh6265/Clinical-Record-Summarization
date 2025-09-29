# Clinical Record Summarization with LLM (Gemini)

## Overview
This project summarizes digitized clinical notes into **structured JSON** using the Google Gemini API.  
Each note is processed into the following fields:

- `Patient`
- `Diagnosis`
- `Treatment`
- `Follow-up`

The pipeline supports batch processing of multiple notes, validates outputs against a strict schema, and includes post-processing normalization to ensure consistency.

---

## Setup Instructions

### 1. Clone or create project folder
```bash
mkdir clinical_summarizer
cd clinical_summarizer
```

2. Create virtual environment
bash
Copy code
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows (PowerShell)
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
Create a requirements.txt file with:

Copy code
google-genai
python-dotenv
jsonschema
4. Configure API key
Option 1: Local .env file (recommended)
Create a .env file in the project root:

ini
Copy code
GEMINI_API_KEY=your_real_api_key_here
Important: Do not commit your .env file. Add .env to .gitignore.

Option 2: Environment variable
You can also set the API key in the terminal:

bash
Copy code
export GEMINI_API_KEY="your_real_api_key_here"   # Mac/Linux
setx GEMINI_API_KEY "your_real_api_key_here"     # Windows
Example placeholder file
Create .env.example in the repo with:

ini
Copy code
GEMINI_API_KEY=your_api_key_here
This shows the format for anyone cloning the repo. The user should copy it to .env and fill in their key:

bash
Copy code
cp .env.example .env
5. Prepare input notes
Create a folder notes/ and add .txt files.

Sample notes for testing:

notes/note1.txt

vbnet
Copy code
Patient: John Doe, 45-year-old male
History: Complains of persistent headaches and dizziness. 
BP: 160/95 on two separate readings.
Plan: Start Lisinopril 10mg daily. Counsel on diet and exercise. 
Follow-up in 2 weeks for BP check.
notes/note2.txt

vbnet
Copy code
Patient: Maria Lopez, 30-year-old female
History: Presents with fever, sore throat, and fatigue. Rapid strep test positive.
Plan: Prescribed Amoxicillin 500mg TID for 10 days. Advise hydration and rest.
Follow-up in 5 days if symptoms persist or worsen.
notes/note3.txt

vbnet
Copy code
Patient: Raj Sharma, 62-year-old male
History: History of Type 2 Diabetes. Today with foot ulcer, mild swelling.
Plan: Clean ulcer, start antibiotics (Cefalexin 500mg QID). Refer to podiatry.
Follow-up in 7 days to assess healing.
notes/note4.txt

makefile
Copy code
Patient: Sarah Mitchell, 25-year-old female
History: Reports anxiety, insomnia, and poor concentration for 3 months.
Plan: Begin CBT referral, consider SSRI (Escitalopram 10mg daily).
Follow-up in 4 weeks for mental health review.
notes/note5.txt

vbnet
Copy code
Patient: Ahmed Khan, 70-year-old male
History: Recent hospital discharge after pneumonia. Now stable, oxygen saturation 97% on room air.
Plan: Continue oral antibiotics (Levofloxacin 500mg OD for 5 days). Encourage breathing exercises.
Follow-up in 1 week with chest X-ray.
6. Run the script
bash
Copy code
python summarize_notes.py
The script will batch process all notes in the notes/ folder.

JSON outputs are saved to output/ folder.

Example JSON output:

json
Copy code
{
  "Patient": "John Doe, 45-year-old male",
  "Diagnosis": "Hypertension",
  "Treatment": "Start Lisinopril 10mg daily; counsel on diet and exercise",
  "Follow-up": "2 weeks for BP check"
}
Deliverables
summarize_notes.py → Main script

notes/ → Input folder with .txt notes

output/ → Folder with structured .json summaries

.env.example → Example API key file

README.md → Setup and run guide

Example .json outputs

Notes for Interviewers
The pipeline currently processes digitized .txt notes.

It can be extended to handle PDFs or images by adding OCR (e.g., AWS Textract, Tesseract).

Ensure .env exists and contains a valid GEMINI_API_KEY.

