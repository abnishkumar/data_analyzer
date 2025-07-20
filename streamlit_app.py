import streamlit as st
import asyncio
import tempfile
import os
from data_analysis_runner import DataAnalysisRunner
from autogen_agentchat.messages import TextMessage
import time

from config.constants import WORK_DIR_DOCKER

# Set page config with a modern theme
st.set_page_config(
    page_title="Data Analyzer Pro",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/abnishkumar/',
        'Report a bug': "https://www.linkedin.com/in/abnishkumar/",
        'About': "# Intelligent Data Analysis Platform"
    }
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 2rem 3rem;
        min-height: 100vh;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 6px rgba(99, 102, 241, 0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(99, 102, 241, 0.3);
        background: linear-gradient(135deg, #5a5fef 0%, #7c4df6 100%);
    }
    
    .stFileUploader {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }
    
    .stTextArea textarea {
        border-radius: 12px;
        border: 1px solid #e2e8f0 !important;
        padding: 1.25rem;
        background: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
    }
    
    .card {
        background: white;
        padding: 1.75rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        border-left: 4px solid #6366f1;
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-3px);
    }
    
    .title {
        color: #1e293b;
        font-size: 2.75rem;
        font-weight: 800;
        margin-bottom: 2rem;
        text-align: center;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .sidebar {
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        padding: 1.5rem;
        border-right: 1px solid #e2e8f0;
    }
    
    .sidebar-title {
        color: #1e293b;
        font-weight: 700;
        font-size: 1.25rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .progress-bar {
        height: 6px;
        background: #e2e8f0;
        border-radius: 3px;
        margin-top: 1rem;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        border-radius: 3px;
        transition: width 0.4s ease;
    }
    
    .file-info {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem;
        background: #f8fafc;
        border-radius: 12px;
        margin-top: 1rem;
    }
    
    .file-icon {
        font-size: 1.5rem;
        color: #6366f1;
    }
    
    .file-details {
        flex: 1;
    }
    
    .file-name {
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    .file-size {
        font-size: 0.85rem;
        color: #64748b;
    }
    
    .success-message {
        background: #f0fdf4;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    
    .warning-message {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        border-left: 4px solid #8b5cf6;
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .result-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .result-icon {
        font-size: 1.5rem;
        color: #8b5cf6;
    }
    
    .result-title {
        font-weight: 700;
        font-size: 1.1rem;
        color: #1e293b;
    }
    
    .result-content {
        line-height: 1.6;
        color: #334155;
    }
    
    .floating-chat {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: white;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        cursor: pointer;
        z-index: 100;
        transition: all 0.3s ease;
    }
    
    .floating-chat:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2);
    }
    
    .chat-icon {
        font-size: 1.5rem;
        color: #6366f1;
    }
    
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #1e293b;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 8px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.85rem;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# ===== ERROR MESSAGES ===== #
ERROR_MESSAGES = {
    "no_file": {
        "title": "File Required",
        "message": "Please upload a file first to begin analysis.",
        "icon": "exclamation-circle",
        "color": "#ef4444"
    },
    "no_question": {
        "title": "Question Required",
        "message": "Please enter a question or select an example question.",
        "icon": "question-circle",
        "color": "#ef4444"
    },
    "invalid_file": {
        "title": "Invalid File",
        "message": "The uploaded file appears to be corrupted or empty.",
        "icon": "file-excel",
        "color": "#f59e0b"
    },
    "file_too_large": {
        "title": "File Too Large",
        "message": "Maximum file size is 50MB. Please upload a smaller file.",
        "icon": "file-archive",
        "color": "#f59e0b"
    }
}

def show_error(error_key):
    """Display consistent error messages"""
    error = ERROR_MESSAGES.get(error_key, ERROR_MESSAGES["no_file"])
    st.markdown(
        f"""
        <div class="error-message">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <i class="fas fa-{error['icon']}" style="color: {error['color']};"></i>
                <strong>{error['title']}</strong>
            </div>
            <p style="margin-top: 0.5rem; margin-bottom: 0;">{error['message']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def save_uploaded_file(uploaded_file):
    """Safely handle file uploads with validation"""
    try:
        # Validate file size (max 50MB)
        max_size = 50 * 1024 * 1024
        if uploaded_file.size > max_size:
            show_error("file_too_large")
            return None
        SAVE_DIR = WORK_DIR_DOCKER
        if uploaded_file:
            #os.makedirs(SAVE_DIR, exist_ok=True)
            save_path = os.path.join(SAVE_DIR, uploaded_file.name)
            with open(save_path, "wb") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
            return uploaded_file.name
    except Exception as e:
        st.error(f"File handling error: {str(e)}")
        return None

def update_progress(progress_bar, status_text, percent, message):
    """Update progress bar with actual progress"""
    progress_bar.progress(percent)
    status_text.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 0.5rem; color: #64748b;">
            <i class="fas {'fa-spinner fa-spin' if percent < 100 else 'fa-check-circle'}"></i>
            {message} ({percent}%)
        </div>
        """,
        unsafe_allow_html=True
    )

async def run_analysis_wrapper(file_path, question, depth, progress_bar, status_text, result_placeholder):
    """Wrapper for the analysis process with real progress updates"""
    try:
        update_progress(progress_bar, status_text, 10, "Initializing analysis")
        
        async with DataAnalysisRunner() as runner:
            update_progress(progress_bar, status_text, 30, "Processing data")
            progress = 10  # Initialize progress variable
            async for message in runner.analyze_data(f"File path: {file_path}\nQuestion: {question}\nDepth: {depth}"):
                if isinstance(message, TextMessage):
                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="result-header">
                                <div class="result-icon">
                                    <i class="fas fa-chart-line"></i>
                                </div>
                                <div class="result-title">Analysis Results</div>
                            </div>
                            <div class="result-content">
                                {message.content}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                update_progress(progress_bar, status_text, min(90, progress + 20), "Generating insights")
        
        update_progress(progress_bar, status_text, 100, "Analysis complete")
        
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        update_progress(progress_bar, status_text, 0, "Analysis failed")

# ===== MAIN APP ===== #
# Sidebar for file upload and settings
with st.sidebar:
    st.markdown('<div class="sidebar-title"><i class="fas fa-cog"></i> Settings & Upload</div>', unsafe_allow_html=True)
    
    # File upload section
    uploaded_file = st.file_uploader(
        "📤 Upload your data file",
        type=["csv", "txt", "pdf", "xlsx", "json"],
        help="Supported formats: CSV, TXT, PDF, Excel, JSON"
    )
    
    if uploaded_file:
        # Display file info
        file_size = len(uploaded_file.getvalue()) / 1024  # in KB
        st.markdown(
            f"""
            <div class="file-info">
                <div class="file-icon">
                    <i class="fas fa-file-alt"></i>
                </div>
                <div class="file-details">
                    <div class="file-name">{uploaded_file.name}</div>
                    <div class="file-size">{file_size:.2f} KB</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Analysis options
    st.markdown("---")
    st.markdown('<div class="sidebar-title"><i class="fas fa-sliders-h"></i> Analysis Options</div>', unsafe_allow_html=True)
    analysis_depth = st.select_slider(
        "Analysis Depth",
        options=["Basic", "Standard", "Detailed", "Comprehensive"],
        value="Standard"
    )
    
    show_intermediate = st.checkbox("Show intermediate steps", value=True)
    enable_visuals = st.checkbox("Enable visualizations", value=True)

# Main content
st.markdown('<div class="title">🔍 Data Analyzer Pro</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 2rem; color: #64748b; font-size: 1.1rem;">
        Upload your data file and ask questions to extract powerful insights with AI-powered analysis.
    </div>
    """,
    unsafe_allow_html=True
)

# Question input card
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    user_question = st.text_area(
        "💡 What would you like to know about your data?",
        height=150,
        placeholder="e.g., What are the key trends in this dataset?\nWhat anomalies can you detect?\nSummarize the main findings...",
        help="Ask specific questions to get the most relevant insights"
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        example_questions = st.selectbox(
            "Or select an example question:",
            [
                "Select an example...",
                "What are the key patterns in this data?",
                "Are there any outliers or anomalies?",
                "Can you summarize the main findings?",
                "What correlations exist between variables?",
                "Generate a detailed statistical analysis"
            ],
            index=0
        )
        if example_questions != "Select an example...":
            user_question = example_questions
    
    with col2:
        analyze_button = st.button("Analyze Now", key="analyze", help="Click to start analysis")
    st.markdown('</div>', unsafe_allow_html=True)

# Analysis results section
results_container = st.container()

if analyze_button:
    if not uploaded_file:
        with results_container:
            show_error("no_file")
    elif not user_question.strip():
        with results_container:
            show_error("no_question")
    else:
        with results_container:
            # Initialize progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            result_placeholder = st.empty()
            
            # Process file and run analysis
            file_path = save_uploaded_file(uploaded_file)
            if file_path:
                try:
                    asyncio.run(run_analysis_wrapper(
                        file_path, 
                        user_question, 
                        analysis_depth,
                        progress_bar,
                        status_text,
                        result_placeholder
                    ))
                finally:
                    # Clean up the temporary file
                    if os.path.exists(file_path):
                        try:
                            os.unlink(file_path)
                        except Exception as e:
                            st.warning(f"Failed to delete temporary file: {str(e)}")

# Floating help button
st.markdown(
    """
    <div class="floating-chat tooltip">
        <div class="chat-icon">
            <i class="fas fa-question"></i>
        </div>
        <span class="tooltiptext">Need help? Click to chat with support</span>
    </div>
    """,
    unsafe_allow_html=True
)