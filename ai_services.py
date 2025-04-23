# ai_services.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file BEFORE accessing them
load_dotenv()

# Configure the Gemini API with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def optimize_resume(base_resume, base_cover_letter, job_description):
    """
    Generate an optimized resume and tailored cover letter using the Google Gemini API.
    """
    # Clean and preprocess inputs if needed (optional)
    
    prompt = f"""Task: Resume Optimization for Job Application

Objective:
Optimize a base resume and cover letter to align with the provided Job Description. Maximize appeal for both ATS systems and human reviewers.

IMPORTANT: Do NOT include any introductory statements, greetings, or commentary in your output. Start directly with the optimized content in the required format and make sure length of the cover letter is between 200 and 400 words.

Instructions:
1. Review the provided Base Resume and Cover Letter below.
2. Analyze the Job Description thoroughly to identify:
   - Key skills and qualifications required
   - Specific technologies, tools, and methodologies mentioned
   - Company values and culture indicators
   - Industry-specific terminology and keywords
3. Rephrase and prioritize the existing content from the Base Resume to emphasize relevant skills and experiences in order to improve the ATS score to 90% or higher.
4. Only introduce new skills when necessary and maintain the order of existing content.
5. Incorporate relevant keywords from the job description into the resume in a natural way.
6. Adjust job titles for better relevance if needed, clearly noting any changes made.
7. Make sure to quantify achievements where possible (e.g., "improved process efficiency by 30%").
8. Output the optimized resume in plain text (copy-and-paste ready, no formatting).
9. Draft a tailored cover letter that:
   - Addresses specific requirements from the job description
   - Highlights 2-3 most relevant accomplishments from the resume
   - Demonstrates knowledge of the company/industry
   - Explains why the candidate is particularly suited for this role
   - Includes a clear call to action
10. Provide an estimated ATS compatibility percentage and explain 3 specific factors that influenced this score.
11. Include a brief section with 2-3 specific interview talking points the candidate should prepare.

---BASE RESUME---
{base_resume}

---BASE COVER LETTER---
{base_cover_letter}

---JOB DESCRIPTION---
{job_description}

Output the final result in the following format:

RESUME:
[Optimized resume here]

COVER LETTER:
[Optimized cover letter here]

ATS COMPATIBILITY ANALYSIS:
```markdown
## ATS Compatibility Analysis
### Estimated ATS Passing Percentage: XX%

#### Key factors influencing score:
1. [First factor]
2. [Second factor] 
3. [Third factor]

#### Suggested improvements:
* [First suggestion]
* [Second suggestion]
* [Third suggestion if applicable]
```

INTERVIEW PREPARATION:
[2-3 key talking points based on job requirements and resume]
"""
    # Create a Gemini model instance - using newer model
    model = genai.GenerativeModel('models/gemini-2.0-pro-exp')
    
    # Call the Gemini API with system prompt and user prompt in a conversation format
    chat = model.start_chat(history=[])
    response = chat.send_message(
        "You are a skilled resume optimization agent who will help optimize resumes based on job descriptions.\n\n" + prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7
        )
    )
    
    # Clean up the output to remove any introductory text
    output_text = response.text
    
    # Remove any introductory text before the first section header
    # Look for the first occurrence of "RESUME:" and start from there
    if "RESUME:" in output_text:
        output_text = "RESUME:" + output_text.split("RESUME:", 1)[1]
    
    # Return the cleaned response text
    return output_text
