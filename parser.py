import os
import json
import time  # <--- Added this to handle timing
from google import genai
from google.genai import types
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
MY_API_KEY = "your_api_key"
client = genai.Client(api_key=MY_API_KEY)

def parse_jobs_with_gemini():
    if not os.path.exists("raw_data"):
        print("Error: 'raw_data' folder not found!")
        return
        
    raw_files = [f for f in os.listdir("raw_data") if f.endswith(".html")]
    processed_data = []

    for index, filename in enumerate(raw_files):
        print(f"[{index+1}/{len(raw_files)}] Gemini is analyzing {filename}...")
        
        with open(f"raw_data/{filename}", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            for tag in soup(["script", "style", "nav", "footer"]):
                tag.decompose()
            text_content = soup.get_text(separator=' ', strip=True)[:10000]

        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"Extract Job Title, Hard Skills (list), and Experience Level from: {text_content}",
                config=types.GenerateContentConfig(
                    response_mime_type='application/json',
                    response_schema={
                        "type": "OBJECT",
                        "properties": {
                            "title": {"type": "STRING"},
                            "skills": {"type": "ARRAY", "items": {"type": "STRING"}},
                            "experience_level": {"type": "STRING"}
                        },
                        "required": ["title", "skills", "experience_level"]
                    }
                )
            )
            
            job_data = json.loads(response.text)
            processed_data.append(job_data)
            print(f"✅ Successfully parsed: {job_data.get('title')}")

            # --- THE FIX: WAIT TO AVOID 429 ERROR ---
            if index < len(raw_files) - 1:  # No need to wait after the very last file
                print("Waiting 35 seconds to stay under free tier limits...")
                time.sleep(35) 

        except Exception as e:
            print(f"❌ Gemini failed on {filename}: {e}")

    with open("processed_jobs.json", "w") as f:
        json.dump(processed_data, f, indent=4)
    print("\nPhase 2 Complete! Check 'processed_jobs.json'")

if __name__ == "__main__":
    parse_jobs_with_gemini()