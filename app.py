import os  # Import the os module
from dotenv import load_dotenv  # Import load_dotenv
import streamlit as st
import google.generativeai as genai
import io
import PyPDF2
from docx import Document  # Correctly import Document from python-docx
import re

# Load environment variables from .env file BEFORE accessing them
load_dotenv()

# Configure the Gemini API with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text_from_file(uploaded_file):
    """
    Extract text from various file formats (txt, pdf, docx)
    """
    if uploaded_file is None:
        return ""
        
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    try:
        if file_extension == "txt":
            # For text files, read directly
            return uploaded_file.getvalue().decode("utf-8")
            
        elif file_extension == "pdf":
            # For PDF files, use PyPDF2
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
            
        elif file_extension == "docx":
            # For DOCX files, use python-docx
            doc = Document(io.BytesIO(uploaded_file.getvalue()))
            text = []
            for para in doc.paragraphs:
                text.append(para.text)
            return "\n".join(text)
            
        else:
            return "Unsupported file format"
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def optimize_resume(base_resume, base_cover_letter, job_description):
    """
    Generate an optimized resume and tailored cover letter using the Google Gemini API.
    """
    prompt = f"""Task: Resume Optimization for Job Application

Objective:
Optimize a base resume and cover letter to align with the provided Job Description. Maximize appeal for both ATS systems and human reviewers.

Instructions:
1. Review the provided Base Resume and Cover Letter below.
2. Analyze the Job Description thoroughly to identify:
   - Key skills and qualifications required
   - Specific technologies, tools, and methodologies mentioned
   - Company values and culture indicators
   - Industry-specific terminology and keywords
3. Rephrase and prioritize the existing content from the Base Resume to emphasize relevant skills and experiences.
4. Do not introduce new skills—only reword and reorder existing content.
5. Incorporate relevant keywords from the job description into the resume in a natural way.
6. Adjust job titles for better relevance if needed, clearly noting any changes made.
7. Quantify achievements where possible (e.g., "improved process efficiency by 30%").
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
    
    # Return the response text
    return response.text

# Streamlit Web Interface
st.set_page_config(page_title="Resume Optimization Agent", page_icon="📄", layout="wide")

st.title("Resume Optimization Agent")
st.markdown("### AI-Powered Resume and Cover Letter Tailoring")

# Add information about the app
with st.expander("About this tool"):
    st.markdown("""
    **How this tool works:**
    1. Enter your current resume and cover letter in plain text format
    2. Paste the complete job description you're applying for
    3. The AI will analyze both and optimize your materials to match the job requirements
    4. You'll receive tailored versions plus analysis of ATS compatibility
    
    **Best practices:**
    * Include your complete work history and skills in your base resume
    * Make sure your cover letter contains your general value proposition
    * Provide the full job description with all requirements and company details
    * Review and personalize the AI-generated content before submitting
    """)

# Add model information
st.sidebar.header("Model Information")
st.sidebar.info("This tool uses Google's Gemini 2.0 Pro model to analyze and optimize your resume materials.")

# Example toggle
show_examples = st.sidebar.checkbox("Show examples")

st.markdown("### Provide Your Candidate Materials:")

# Toggle between upload and paste options
col1, col2, col3 = st.columns(3)
with col1:
    resume_input_method = st.radio("Resume Input Method:", ["Upload File", "Paste Text"], key="resume_method")
with col2:
    cover_letter_input_method = st.radio("Cover Letter Input Method:", ["Upload File", "Paste Text"], key="cover_letter_method")
with col3:
    job_desc_input_method = st.radio("Job Description Input Method:", ["Upload File", "Paste Text"], key="job_desc_method")

# Resume input
if resume_input_method == "Upload File":
    resume_file = st.file_uploader("Upload Resume", type=["txt", "docx", "pdf"], key="resume_file")
    if resume_file is not None:
        with st.spinner("Processing resume file..."):
            base_resume = extract_text_from_file(resume_file)
            st.success(f"Successfully processed {resume_file.name}")
            # Show a preview of the extracted text
            with st.expander("Resume Preview"):
                st.text(base_resume[:500] + ("..." if len(base_resume) > 500 else ""))
    else:
        base_resume = ""
else:
    base_resume = st.text_area("Base Resume", height=300, 
                              help="Paste your base resume here (plain text).", key="resume_text")

# Cover letter input
if cover_letter_input_method == "Upload File":
    cover_letter_file = st.file_uploader("Upload Cover Letter", type=["txt", "docx", "pdf"], key="cover_letter_file")
    if cover_letter_file is not None:
        with st.spinner("Processing cover letter file..."):
            base_cover_letter = extract_text_from_file(cover_letter_file)
            st.success(f"Successfully processed {cover_letter_file.name}")
            # Show a preview of the extracted text
            with st.expander("Cover Letter Preview"):
                st.text(base_cover_letter[:500] + ("..." if len(base_cover_letter) > 500 else ""))
    else:
        base_cover_letter = ""
else:
    base_cover_letter = st.text_area("Base Cover Letter", height=200, 
                                    help="Paste your base cover letter here (plain text).", key="cover_letter_text")

# Job description input
if job_desc_input_method == "Upload File":
    job_desc_file = st.file_uploader("Upload Job Description", type=["txt", "docx", "pdf"], key="job_desc_file")
    if job_desc_file is not None:
        with st.spinner("Processing job description file..."):
            job_description = extract_text_from_file(job_desc_file)
            st.success(f"Successfully processed {job_desc_file.name}")
            # Show a preview of the extracted text
            with st.expander("Job Description Preview"):
                st.text(job_description[:500] + ("..." if len(job_description) > 500 else ""))
    else:
        job_description = ""
else:
    job_description = st.text_area("Job Description", height=300, 
                                  help="Paste the job description here (plain text).", key="job_desc_text")

if st.button("Optimize Resume and Cover Letter"):
    if base_resume and base_cover_letter and job_description:
        # Create placeholder for progress updates
        progress_placeholder = st.empty()
        result_placeholder = st.empty()
        
        progress_placeholder.info("Starting optimization process...")
        
        try:
            with st.spinner("Generating optimized materials..."):
                progress_placeholder.info("Analyzing job description and optimizing materials...")
                output = optimize_resume(base_resume, base_cover_letter, job_description)
                progress_placeholder.success("Optimization complete!")
            
            # Display results in tabs for better organization
            tab1, tab2, tab3, tab4 = st.tabs(["Complete Output", "Resume", "Cover Letter", "ATS Analysis"])
            
            with tab1:
                st.text_area("Complete Results", value=output, height=600)
                
                # Add download button for the complete output
                st.download_button(
                    label="Download Complete Results",
                    data=output,
                    file_name="optimized_materials.txt",
                    mime="text/plain"
                )
            
            # Extract sections for individual tabs (basic extraction - can be improved)
            try:
                resume_section = output.split("RESUME:")[1].split("COVER LETTER:")[0].strip()
                with tab2:
                    st.text_area("Optimized Resume", value=resume_section, height=500)
                    st.download_button(
                        label="Download Resume",
                        data=resume_section,
                        file_name="optimized_resume.txt",
                        mime="text/plain"
                    )
                    
                cover_letter_section = output.split("COVER LETTER:")[1].split("ATS COMPATIBILITY ANALYSIS:")[0].strip()
                with tab3:
                    st.text_area("Optimized Cover Letter", value=cover_letter_section, height=500)
                    st.download_button(
                        label="Download Cover Letter",
                        data=cover_letter_section,
                        file_name="optimized_cover_letter.txt",
                        mime="text/plain"
                    )
                    
                ats_section = ""
                if "ATS COMPATIBILITY ANALYSIS:" in output:
                    ats_section = output.split("ATS COMPATIBILITY ANALYSIS:")[1].strip()
                    if "INTERVIEW PREPARATION:" in ats_section:
                        ats_section = ats_section.split("INTERVIEW PREPARATION:")[0].strip()
                    
                    # Extract the markdown content if it exists
                    markdown_content = ""
                    if "```markdown" in ats_section and "```" in ats_section.split("```markdown")[1]:
                        markdown_content = ats_section.split("```markdown")[1].split("```")[0].strip()
                    else:
                        # Fallback if the AI doesn't format it correctly
                        markdown_content = ats_section
                with tab4:
                    # Display ATS analysis as rendered markdown instead of plain text
                    st.markdown(markdown_content)
                    
                    # Still provide download option
                    st.download_button(
                        label="Download ATS Analysis",
                        data=ats_section,
                        file_name="ats_analysis.md",
                        mime="text/markdown"
                    )
            except:
                st.warning("Couldn't parse sections properly. Please use the Complete Output tab.")
                
        except Exception as e:
            progress_placeholder.error(f"An error occurred: {str(e)}")
            st.exception(e)
            
    else:
        st.error("Please fill in all text areas before running optimization.")
