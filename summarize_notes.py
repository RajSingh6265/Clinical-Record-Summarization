import os, glob, json, re, time
from pathlib import Path
from google import genai
from google.genai.errors import ServerError, APIError
from jsonschema import validate, ValidationError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SCHEMA = {
    "type": "object",
    "properties": {
        "Patient": {"type": "string"},
        "Diagnosis": {"type": "string"},
        "Treatment": {"type": "string"},
        "Follow-up": {"type": "string"}
    },
    "required": ["Patient", "Diagnosis", "Treatment", "Follow-up"],
    "additionalProperties": False
}

# Configure Gemini API with API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")

client = genai.Client(api_key=api_key)

def call_gemini_for_json(note_text, model="gemini-2.5-flash", max_retries=3):
    prompt = (
        "You are a clinical note summarizer. Given the clinical note below, return "
        "STRICT valid JSON (no explanation, no markdown, no backticks) that exactly "
        "matches this schema: {Patient, Diagnosis, Treatment, Follow-up}.\n\n"
        f"Clinical note:\n'''{note_text}'''"
    )
    
    for attempt in range(max_retries):
        try:
            resp = client.models.generate_content(model=model, contents=prompt)
            return getattr(resp, "text", "")
        except ServerError as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Server error - {e}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5  # Exponential backoff: 5, 10, 15 seconds
                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                raise e
        except APIError as e:
            print(f"API Error: {e}")
            raise e
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise e

def extract_json_from_text(text):
    try:
        return json.loads(text)
    except:
        m = re.search(r'\{[\s\S]*\}', text)
        if m:
            try:
                return json.loads(m.group(0))
            except:
                return None
        return None

def validate_output(obj):
    try:
        validate(instance=obj, schema=SCHEMA)
        return True, None
    except ValidationError as e:
        return False, str(e)

def normalize_output(parsed):
    """Ensure consistent style across all notes"""
    def clean_text(t):
        return t.strip().rstrip(".")
    parsed["Patient"] = parsed["Patient"].replace("yo", "year-old").replace("Y/O", "year-old")
    parsed["Diagnosis"] = clean_text(parsed["Diagnosis"])
    parsed["Treatment"] = clean_text(parsed["Treatment"])
    parsed["Follow-up"] = clean_text(parsed["Follow-up"])
    # Normalize gender casing
    parsed["Patient"] = parsed["Patient"].replace("Male", "male").replace("Female", "female")
    return parsed

def summarize_file(in_path, out_path):
    try:
        with open(in_path, 'r') as f:
            note = f.read().strip()
        
        raw = call_gemini_for_json(note)
        parsed = extract_json_from_text(raw)
        if not parsed:
            return False, f"Parse failed. Raw:\n{raw}"
        
        ok, err = validate_output(parsed)
        if not ok:
            return False, f"Validation error: {err}"
        
        parsed = normalize_output(parsed)
        with open(out_path, 'w') as f:
            json.dump(parsed, f, indent=2)
        return True, None
        
    except (ServerError, APIError) as e:
        return False, f"API Error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def batch_process(notes_dir="notes", out_dir="output"):
    Path(out_dir).mkdir(exist_ok=True)
    results = {}
    total_files = len(glob.glob(os.path.join(notes_dir, "*.txt")))
    
    print(f"Processing {total_files} clinical notes...")
    
    for i, fp in enumerate(glob.glob(os.path.join(notes_dir, "*.txt")), 1):
        print(f"\nProcessing file {i}/{total_files}: {os.path.basename(fp)}")
        out_fp = os.path.join(out_dir, os.path.basename(fp).replace(".txt", ".json"))
        
        success, msg = summarize_file(fp, out_fp)
        results[fp] = {"success": success, "message": msg}
        
        if success:
            print(f"✅ Successfully processed {os.path.basename(fp)}")
        else:
            print(f"❌ Failed to process {os.path.basename(fp)}: {msg}")
        
        # Small delay between requests to be respectful to the API
        if i < total_files:  # Don't sleep after the last file
            time.sleep(1)
    
    return results

if __name__ == "__main__":
    res = batch_process()
    print(json.dumps(res, indent=2))
