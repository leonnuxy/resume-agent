import streamlit as st

def load_css(file_path):
    """
    Load and apply custom CSS from a file.
    """
    with open(file_path, "r") as f:
        return f.read()

def apply_custom_css(css):
    """
    Apply custom CSS to the Streamlit app.
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def render_header():
    """
    Render the header bar with logo/brand name and navigation.
    """
    col1 = st.columns([3, 1])[0]
    
    with col1:
        st.markdown('<div class="header-logo">📄 Resume Agent</div>', unsafe_allow_html=True)
    
def render_input_card(title, icon, key_prefix, is_mobile=False):
    """
    Render a single input card with a title, icon, and toggle between upload and paste text.
    
    Returns:
    - input_method: "Upload File" or "Paste Text"
    - input_content: The content (file or text) provided by the user
    """
    st.markdown(f'<div class="card-title">{icon} {title}</div>', unsafe_allow_html=True)
    
    # Input method toggle
    input_method = st.radio(
        f"{title} Input Method:", 
        ["Upload File", "Paste Text"], 
        key=f"{key_prefix}_method",
        horizontal=not is_mobile
    )
    
    input_content = None
    
    # Input area based on selected method
    if input_method == "Upload File":
        uploaded_file = st.file_uploader(
            f"Upload your {title}", 
            type=["txt", "docx", "pdf"], 
            key=f"{key_prefix}_file"
        )
        
        if uploaded_file is not None:
            from utils import extract_text_from_file
            with st.spinner(f"Processing {title.lower()} file..."):
                input_content = extract_text_from_file(uploaded_file)
                st.success(f"Successfully processed {uploaded_file.name}")
                with st.expander(f"{title} Preview"):
                    st.text(input_content[:500] + ("..." if len(input_content) > 500 else ""))
    else:
        # For Paste Text input, check if a value is stored in session_state for pre-population
        default_value = ""
        if "user_input" in st.session_state:
            if key_prefix == "resume":
                default_value = st.session_state["user_input"].get("base_resume", "")
            elif key_prefix == "cover_letter":
                default_value = st.session_state["user_input"].get("base_cover_letter", "")
            elif key_prefix == "job_desc":
                default_value = st.session_state["user_input"].get("job_description", "")
        height = 150 if is_mobile else 250
        input_content = st.text_area(
            f"Enter your {title}", 
            value=default_value,
            height=height,
            key=f"{key_prefix}_text"
        )
    
    return input_method, input_content

def render_input_cards(is_mobile=False):
    """
    Render all three input cards with appropriate layout based on device type.
    
    Returns:
    - A dictionary with all input methods and contents
    """
    st.markdown('<h2 class="section-heading">Provide Your Candidate Materials</h2>', unsafe_allow_html=True)
    
    inputs = {}
    
    if is_mobile:
        # Stack cards vertically on mobile
        with st.container():
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            inputs["resume_method"], inputs["resume_content"] = render_input_card("Resume", "📄", "resume", is_mobile)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with st.container():
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            inputs["cover_letter_method"], inputs["cover_letter_content"] = render_input_card("Cover Letter", "✉️", "cover_letter", is_mobile)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with st.container():
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            inputs["job_desc_method"], inputs["job_desc_content"] = render_input_card("Job Description", "🔍", "job_desc", is_mobile)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Use columns for desktop layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            inputs["resume_method"], inputs["resume_content"] = render_input_card("Resume", "📄", "resume")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            inputs["cover_letter_method"], inputs["cover_letter_content"] = render_input_card("Cover Letter", "✉️", "cover_letter")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col3:
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            inputs["job_desc_method"], inputs["job_desc_content"] = render_input_card("Job Description", "🔍", "job_desc")
            st.markdown('</div>', unsafe_allow_html=True)
    
    return inputs

def render_action_button(disabled=True):
    """
    Render the call to action button.
    
    Returns:
    - clicked: Boolean indicating if the button was clicked
    """
    st.markdown('<div class="action-button-container">', unsafe_allow_html=True)
    
    # Use a container to apply custom classes
    button_container = st.container()
    with button_container:
        clicked = st.button(
            "Analyze Resume", 
            disabled=disabled,
            key="analyze_button",
            use_container_width=False
        )
        st.markdown('</div>', unsafe_allow_html=True)
    return clicked

def render_input_method_selection(is_mobile):
    """
    Legacy function to render input method selection for resume, cover letter, and job description.
    (Deprecated: Use render_input_cards instead.)
    """
    if is_mobile:
        resume_input_method = st.radio("Resume Input Method:", ["Upload File", "Paste Text"], key="resume_method", horizontal=True)
        cover_letter_input_method = st.radio("Cover Letter Input Method:", ["Upload File", "Paste Text"], key="cover_letter_method", horizontal=True)
        job_desc_input_method = st.radio("Job Description Input Method:", ["Paste Text", "Upload File"], key="job_desc_method", horizontal=True)
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            resume_input_method = st.radio("Resume Input Method:", ["Upload File", "Paste Text"], key="resume_method")
        with col2:
            cover_letter_input_method = st.radio("Cover Letter Input Method:", ["Upload File", "Paste Text"], key="cover_letter_method")
        with col3:
            job_desc_input_method = st.radio("Job Description Input Method:", ["Paste Text", "Upload File"], key="job_desc_method")

    return resume_input_method, cover_letter_input_method, job_desc_input_method
