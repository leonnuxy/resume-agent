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

# Import utility functions from utils.py
from utils import extract_text_from_file, remove_bullet_points_from_sections

# Import the optimize_resume function from ai_services.py
from ai_services import optimize_resume

# Import UI components from ui_components.py
from ui_components import load_css, apply_custom_css, render_header, render_input_cards, render_action_button

# Streamlit Web Interface configuration
st.set_page_config(page_title="Resume Optimization Agent", page_icon="📄", layout="wide")

# Load and apply custom CSS
css = load_css("styles.css")
apply_custom_css(css)

# Simple mobile detection - could be enhanced with more sophisticated methods
if 'is_mobile' not in st.session_state:
    user_agent = st.query_params.get('ua', [''])[0].lower()
    is_mobile = any(device in user_agent for device in ['mobile', 'android', 'iphone', 'ipad'])
    viewport_width = st.query_params.get('vw', [1200])[0]
    try:
        viewport_width = int(viewport_width)
        if viewport_width < 768:
            is_mobile = True
    except ValueError:
        pass
    st.session_state['is_mobile'] = is_mobile
else:
    is_mobile = st.session_state['is_mobile']

# Set the default active tab in session state if not set yet.
if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = "Data Entry"  # Options: "Data Entry" or "Results"

# Render the header with logo and navigation
render_header()

# Add information about the app in a modern expander
with st.expander("About this tool"):
    st.markdown("""
    **How this tool works:**
    1. Enter your current resume and cover letter in plain text format
    2. Paste the complete job description you're applying for
    3. The tool will analyze both and optimize your materials to match the job requirements
    4. You'll receive tailored versions plus analysis of ATS compatibility
    
    **Best practices:**
    * Include your complete work history and skills in your base resume
    * Make sure your cover letter contains your general value proposition
    * Provide the full job description with all requirements and company details
    * Review and personalize the AI-generated content before submitting
    """)

# Use st.radio to replicate tab switching for main sections
selected_tab = st.radio(
    "Go to:",
    ["Data Entry", "Results"],
    index=0 if st.session_state["active_tab"] == "Data Entry" else 1,
    horizontal=True
)

# --------------------------
# Data Entry Section
# --------------------------
if selected_tab == "Data Entry":
    inputs = render_input_cards(is_mobile=is_mobile)
    
    # Extract inputs from the rendered cards
    base_resume = inputs.get("resume_content", "")
    base_cover_letter = inputs.get("cover_letter_content", "")
    job_description = inputs.get("job_desc_content", "")
    
    # Validate inputs to enable/disable the Analyze button
    all_inputs_provided = (
        base_resume and base_resume.strip() and
        base_cover_letter and base_cover_letter.strip() and
        job_description and job_description.strip()
    )
    
    # Render the action button; it is disabled if not all inputs are provided
    optimize_clicked = render_action_button(disabled=not all_inputs_provided)
    
    # Process optimization when the Analyze button is clicked
    if optimize_clicked:
        if all_inputs_provided:
            progress_placeholder = st.empty()
            progress_placeholder.info("Starting optimization process...")
            try:
                with st.spinner("Generating optimized materials..."):
                    progress_placeholder.info("Analyzing job description and optimizing materials...")
                    optimization_output = optimize_resume(
                        base_resume=base_resume,
                        base_cover_letter=base_cover_letter,
                        job_description=job_description
                    )
                    # Log the output for debugging purposes
                    print("Optimization Output:", optimization_output)
                    progress_placeholder.success("Optimization complete!")
                
                # Save the optimization output and the original user input
                st.session_state['optimization_output'] = optimization_output
                st.session_state['user_input'] = {
                    "base_resume": base_resume,
                    "base_cover_letter": base_cover_letter,
                    "job_description": job_description
                }
                
                # Update the session state to switch to the Results view
                st.session_state["active_tab"] = "Results"
                st.rerun()  # Re-run the app so the UI immediately shows the Results
            except Exception as e:
                progress_placeholder.error(f"An error occurred: {str(e)}")
                st.exception(e)
        else:
            st.error("Please fill in all text areas before running optimization.")

# --------------------------
# Results Section
# --------------------------
elif selected_tab == "Results":
    st.markdown('<h2 class="section-heading">Optimized Results</h2>', unsafe_allow_html=True)
    
    if 'optimization_output' in st.session_state:
        output = st.session_state['optimization_output']
        # Using nested tabs for splitting up the results details
        tab1, tab2, tab3, tab4 = st.tabs(["Complete Output", "Resume", "Cover Letter", "ATS Analysis"])

        with tab1:
            st.markdown('<div class="results-card">', unsafe_allow_html=True)
            result_height = 400 if is_mobile else 600
            st.text_area("Complete Results", value=output, height=result_height)
            st.markdown('<div class="download-button-container">', unsafe_allow_html=True)
            st.download_button(
                label="Download Complete Results",
                data=output,
                file_name="optimized_materials.txt",
                mime="text/plain"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        try:
            # Process and render sections from the optimization output
            resume_section = output.split("RESUME:")[1].split("COVER LETTER:")[0].strip()
            processed_resume = remove_bullet_points_from_sections(resume_section)

            with tab2:
                st.markdown('<div class="results-card">', unsafe_allow_html=True)
                st.text_area("Optimized Resume", value=processed_resume, height=500)
                st.markdown('<div class="download-button-container">', unsafe_allow_html=True)
                st.download_button(
                    label="Download Resume",
                    data=processed_resume,
                    file_name="optimized_resume.txt",
                    mime="text/plain"
                )
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            cover_letter_section = output.split("COVER LETTER:")[1].split("ATS COMPATIBILITY ANALYSIS:")[0].strip()
            with tab3:
                st.markdown('<div class="results-card">', unsafe_allow_html=True)
                st.text_area("Optimized Cover Letter", value=cover_letter_section, height=500)
                st.markdown('<div class="download-button-container">', unsafe_allow_html=True)
                st.download_button(
                    label="Download Cover Letter",
                    data=cover_letter_section,
                    file_name="optimized_cover_letter.txt",
                    mime="text/plain"
                )
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            ats_section = ""
            if "ATS COMPATIBILITY ANALYSIS:" in output:
                ats_section = output.split("ATS COMPATIBILITY ANALYSIS:")[1].strip()
                if "INTERVIEW PREPARATION:" in ats_section:
                    ats_section = ats_section.split("INTERVIEW PREPARATION:")[0].strip()

                markdown_content = ""
                if "```markdown" in ats_section and "```" in ats_section.split("```markdown")[1]:
                    markdown_content = ats_section.split("```markdown")[1].split("```")[0].strip()
                else:
                    markdown_content = ats_section
            with tab4:
                st.markdown('<div class="results-card ats-analysis">', unsafe_allow_html=True)
                st.markdown(markdown_content)
                st.markdown('<div class="download-button-container">', unsafe_allow_html=True)
                st.download_button(
                    label="Download ATS Analysis",
                    data=ats_section,
                    file_name="ats_analysis.txt",
                    mime="text/plain"
                )
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error parsing optimization output: {str(e)}")
    else:
        st.info("No results to display yet. Please enter your resume, cover letter, and job description in the Data Entry view and click Analyze.")
