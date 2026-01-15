"""
Summary display component for the Streamlit application.
"""
import streamlit as st


def render_summary(summary: str, source_info: dict = None):
    """
    Render the summary display section.
    
    Args:
        summary: The generated summary text
        source_info: Optional dict with source information
    """
    st.markdown("---")
    st.markdown("## 📝 Summary")
    
    if source_info:
        with st.expander("📊 Source Information", expanded=False):
            for key, value in source_info.items():
                st.markdown(f"**{key}:** {value}")
    
    # Display summary in a nice container
    st.markdown(
        f"""
        <div class="summary-container">
            {summary}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Copy button
    st.download_button(
        label="📥 Download Summary",
        data=summary,
        file_name="summary.md",
        mime="text/markdown"
    )


def render_loading_summary():
    """Render loading state for summary."""
    with st.spinner("🧠 Generating summary... This may take a moment."):
        return st.empty()
