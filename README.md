# Resume Optimization Agent

A modern, AI-powered web app to optimize your resume and cover letter for specific job descriptions. Built with Streamlit and Google Gemini, it analyzes your materials, tailors them to job requirements, and provides ATS (Applicant Tracking System) compatibility analysis.

## Features
- Upload or paste your resume, cover letter, and job description
- AI-driven optimization of resume and cover letter
- ATS compatibility analysis and interview preparation tips
- Downloadable results
- Modern, responsive UI

## Project Structure

- `app.py` — Main Streamlit app. Handles UI, user input, and result display.
- `ai_services.py` — Contains the `optimize_resume` function, which calls Google Gemini to generate optimized materials.
- `utils.py` — Utility functions for extracting text from files (txt, pdf, docx) and cleaning up resume sections.
- `ui_components.py` — Modular UI components for consistent, modern layout and input handling.
- `styles.css` — Custom CSS for a modern, responsive look (light/dark mode, mobile-friendly).
- `requirements.txt` — Python dependencies for the project.
- `.env` — (Not included in repo) Store your Google Gemini API key as `GEMINI_API_KEY=your_key_here`.
- `output.txt` — (Optional) Example output file for debugging or sample results.

## Setup Instructions

1. **Clone the repository**

```zsh
git clone <your-repo-url>
cd resume-agent
```

2. **Create and activate a virtual environment (recommended)**

```zsh
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```zsh
pip install -r requirements.txt
```

4. **Set up your environment variables**

Create a `.env` file in the project root with your Google Gemini API key:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Running the App

Start the Streamlit app:

```zsh
streamlit run app.py
```

The app will open in your browser. If not, visit the URL shown in your terminal (usually http://localhost:8501).

## Usage
1. Go to the **Data Entry** tab.
2. Upload or paste your resume, cover letter, and job description.
3. Click **Analyze Resume**.
4. View optimized results and ATS analysis in the **Results** tab.
5. Download the generated files as needed.

## File Descriptions
- **app.py**: Orchestrates the app, manages session state, and renders all UI sections.
- **ai_services.py**: Handles communication with Google Gemini, formats prompts, and parses responses.
- **utils.py**: Extracts text from uploaded files and cleans up resume formatting.
- **ui_components.py**: Contains reusable UI elements (input cards, buttons, header, etc.).
- **styles.css**: Customizes the look and feel of the app.
- **requirements.txt**: Lists all required Python packages.
- **.env**: (Not tracked) Stores your API key securely.
- **output.txt**: (Optional) Example output for reference or debugging.

## Notes
- Requires Python 3.8+
- Your API key is required for Gemini integration.
- For best results, provide detailed and accurate input materials.

---

Feel free to customize this README for your needs!