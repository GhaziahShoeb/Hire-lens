import json
from google import genai

# --- CONFIGURATION ---
MY_API_KEY = "your_api_key"
client = genai.Client(api_key=MY_API_KEY)

def run_gap_analysis():
    # 1. Load your profile and the jobs
    with open("my_profile.json", "r") as f:
        my_data = json.load(f)
    
    with open("processed_jobs.json", "r") as f:
        job_data = json.load(f)

    print("🔍 Analyzing the gap between your skills and the market...")

    # 2. Ask Gemini to summarize the "Missing Pieces"
    prompt = f"""
    I have a candidate with these skills: {my_data['my_skills']}
    
    Here is a list of 7 jobs they are interested in: {json.dumps(job_data)}
    
    Please provide a 'Gap Analysis' report:
    1. Top 3 'Must-Learn' skills appearing most often in these jobs that the candidate lacks.
    2. A 'Match Score' (0-100%) for the candidate against these 7 jobs.
    3. One specific project idea that would help them learn the missing skills.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        print("\n" + "="*30)
        print("📊 HIRE-LENS GAP ANALYSIS REPORT")
        print("="*30)
        print(response.text)
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")

if __name__ == "__main__":
    run_gap_analysis()