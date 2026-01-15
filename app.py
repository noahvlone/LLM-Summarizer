"""
LLM Lecture Summarizer & Quiz Generator
Main Streamlit Application
"""
import streamlit as st
from modules.youtube_extractor import get_transcript_from_url
from modules.document_parser import parse_document
from modules.ai_engine import summarize_text, generate_quiz
from components.input_section import render_input_tabs
from components.summary_display import render_summary
from components.quiz_component import render_quiz
from config import AVAILABLE_MODELS, DEFAULT_MODEL, GEMINI_API_KEY, DEEPSEEK_API_KEY


# Page Configuration
st.set_page_config(
    page_title="LLM Lecture Summarizer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for premium look
st.markdown("""
<style>
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        text-align: center;
        color: #a0aec0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #a0aec0;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: white;
        padding: 0.75rem 1rem;
    }
    
    /* File uploader */
    .stFileUploader > div {
        background-color: rgba(255, 255, 255, 0.05);
        border: 2px dashed rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Summary container */
    .summary-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Metric cards */
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    /* Success/Error boxes */
    .stSuccess {
        background: rgba(72, 187, 120, 0.1);
        border: 1px solid rgba(72, 187, 120, 0.3);
        border-radius: 10px;
    }
    
    .stError {
        background: rgba(245, 101, 101, 0.1);
        border: 1px solid rgba(245, 101, 101, 0.3);
        border-radius: 10px;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #667eea transparent transparent transparent;
    }
    
    /* Hide footer */
    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = None
    if 'summary' not in st.session_state:
        st.session_state.summary = None
    if 'quiz' not in st.session_state:
        st.session_state.quiz = None
    if 'source_info' not in st.session_state:
        st.session_state.source_info = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False


def main():
    """Main application function."""
    init_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">📚 LLM Lecture Summarizer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform YouTube lectures and documents into concise summaries and interactive quizzes</p>', unsafe_allow_html=True)
    
    # Input Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        input_type, input_value = render_input_tabs()
        
        # Model Selection
        st.markdown("### 🤖 AI Model")
        
        # Filter available models based on API keys
        available_model_names = []
        for name, config in AVAILABLE_MODELS.items():
            provider = config.get("provider", "")
            if provider == "gemini" and GEMINI_API_KEY:
                available_model_names.append(name)
            elif provider == "deepseek" and DEEPSEEK_API_KEY:
                available_model_names.append(name)
        
        if not available_model_names:
            st.error("No API keys configured. Please add GEMINI_API_KEY or DEEPSEEK_API_KEY to your .env file.")
            return
        
        selected_model = st.selectbox(
            "Select AI Model",
            options=available_model_names,
            index=0,
            help="Choose which AI model to use for summarization and quiz generation"
        )
        
        # Number of quiz questions
        num_questions = st.slider(
            "Number of quiz questions",
            min_value=3,
            max_value=10,
            value=5,
            help="Select how many quiz questions to generate"
        )
        
        # Process button
        if st.button("🚀 Process Content", type="primary", use_container_width=True):
            if input_value:
                process_content(input_type, input_value, num_questions, selected_model)
            else:
                st.warning("Please enter a YouTube URL or upload a document first.")
    
    # Display Results
    if st.session_state.summary:
        render_summary(st.session_state.summary, st.session_state.source_info)
        
        if st.session_state.quiz:
            render_quiz(st.session_state.quiz)
        else:
            st.info("Quiz generation in progress or not available.")


def process_content(input_type: str, input_value, num_questions: int, model_name: str):
    """
    Process the input content (YouTube or Document).
    
    Args:
        input_type: 'youtube' or 'document'
        input_value: URL string or uploaded file
        num_questions: Number of quiz questions to generate
        model_name: Selected AI model name
    """
    # Clear previous results
    st.session_state.extracted_text = None
    st.session_state.summary = None
    st.session_state.quiz = None
    st.session_state.source_info = None
    
    # Step 1: Extract Text
    with st.spinner("📥 Extracting content..."):
        if input_type == 'youtube':
            result = get_transcript_from_url(input_value)
            if result['success']:
                st.session_state.extracted_text = result['text']
                st.session_state.source_info = {
                    'Source': 'YouTube Video',
                    'Language': result.get('language', 'Unknown'),
                    'Text Length': f"{len(result['text']):,} characters"
                }
            else:
                st.error(f"❌ {result.get('error', 'Failed to extract transcript')}")
                return
        else:
            result = parse_document(input_value, input_value.name)
            if result['success']:
                st.session_state.extracted_text = result['text']
                pages_or_slides = result.get('pages') or result.get('slides', 0)
                st.session_state.source_info = {
                    'Source': input_value.name,
                    'Pages/Slides': pages_or_slides,
                    'Text Length': f"{len(result['text']):,} characters"
                }
            else:
                st.error(f"❌ {result.get('error', 'Failed to parse document')}")
                return
    
    st.success("✅ Content extracted successfully!")
    
    # Step 2: Generate Summary
    with st.spinner(f"🧠 Generating summary with {model_name}..."):
        summary_result = summarize_text(st.session_state.extracted_text, model_name)
        if summary_result['success']:
            st.session_state.summary = summary_result['summary']
        else:
            st.error(f"❌ {summary_result.get('error', 'Failed to generate summary')}")
            return
    
    st.success("✅ Summary generated!")
    
    # Step 3: Generate Quiz
    with st.spinner(f"📝 Creating quiz with {model_name}..."):
        quiz_result = generate_quiz(st.session_state.summary, num_questions, model_name)
        if quiz_result['success']:
            st.session_state.quiz = quiz_result['quiz']
        else:
            st.warning(f"⚠️ {quiz_result.get('error', 'Could not generate quiz')}")
    
    st.success("✅ Quiz ready! Scroll down to view results.")
    st.rerun()


if __name__ == "__main__":
    main()
