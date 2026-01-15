"""
Input section component for the Streamlit application.
Handles YouTube URL input and file upload UI.
"""
import streamlit as st


def render_youtube_input():
    """
    Render YouTube URL input section.
    
    Returns:
        str: YouTube URL or None
    """
    st.markdown("### 🎬 YouTube Video")
    st.markdown("Enter a YouTube video URL to extract and summarize its transcript.")
    
    url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        key="youtube_url",
        label_visibility="collapsed"
    )
    
    if url:
        st.caption("✓ URL entered. Click 'Process Content' to continue.")
    
    return url if url else None


def render_file_upload():
    """
    Render file upload section.
    
    Returns:
        UploadedFile or None
    """
    st.markdown("### 📄 Document Upload")
    st.markdown("Upload a PDF or PowerPoint file to extract and summarize its content.")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'pptx'],
        key="file_upload",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        file_size = len(uploaded_file.getvalue()) / 1024  # KB
        st.caption(f"✓ {uploaded_file.name} ({file_size:.1f} KB)")
    
    return uploaded_file


def render_input_tabs():
    """
    Render tabbed input interface.
    
    Returns:
        tuple: (input_type, input_value) - either ('youtube', url) or ('document', file)
    """
    tab1, tab2 = st.tabs(["🎬 YouTube", "📄 Document"])
    
    with tab1:
        youtube_url = render_youtube_input()
        if youtube_url:
            return ('youtube', youtube_url)
    
    with tab2:
        uploaded_file = render_file_upload()
        if uploaded_file:
            return ('document', uploaded_file)
    
    return (None, None)
