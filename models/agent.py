import google.generativeai as genai
import json
from config import Config

class ResumeAgent:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)

    def analyze(self, resume_text, job_description):
        master_prompt = (
            "You are an advanced ATS tracking optimization model and elite technical recruiter. "
            "Cross-examine the raw Resume Text string against the Target Job Description text. "
            "Evaluate gaps, synthesize data, and respond strictly using a valid, raw JSON object matching this schema structure exactly:\n\n"
            "{\n"
            '  "job_title": "Cleaned String Profile Name",\n'
            '  "ats_score": 75,\n'
            '  "skills_found": ["Skill1", "Skill2"],\n'
            '  "missing_skills": ["SkillA", "SkillB"],\n'
            '  "suggestions": "A detailed layout containing bullet points for action items to rewrite lines",\n'
            '  "summary": "Elevated modern profile narrative copy tailored to target description keyword mapping."\n'
            "}\n\n"
            "Do not wrap your output JSON in any markdown code blocks or backticks. Return only the raw JSON object string.\n\n"
            "DATA TO PROCESS:\n"
            f"Resume Text:\n{resume_text}\n\n"
            f"Job Description:\n{job_description}"
        )
        
        try:
            # Using 'gemini-flash-latest' automatically handles rolling production models
            # and prevents 404 API version registry faults.
            model = genai.GenerativeModel("gemini-flash-latest")
            
            response = model.generate_content(
                contents=master_prompt,
                generation_config={
                    "temperature": 0.15
                }
            )
            
            raw_output = response.text.strip()
            
            # Structural Index Trimmer: Isolates and extracts the raw JSON boundary 
            # to prevent accidental markdown formatting from breaking the JSON parser.
            if "{" in raw_output and "}" in raw_output:
                start_idx = raw_output.find("{")
                end_idx = raw_output.rfind("}") + 1
                raw_output = raw_output[start_idx:end_idx]
                
            return json.loads(raw_output)
        except Exception as e:
            raise RuntimeError(f"Agent Engine Parsing Malfunction: {str(e)}")