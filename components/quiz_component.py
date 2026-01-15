"""
Quiz component for the Streamlit application.
Handles interactive quiz UI with scoring.
"""
import streamlit as st


def init_quiz_state(quiz: list):
    """Initialize quiz state in session."""
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    if 'current_quiz' not in st.session_state or st.session_state.current_quiz != quiz:
        st.session_state.current_quiz = quiz
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False


def render_quiz(quiz: list):
    """
    Render interactive quiz interface.
    
    Args:
        quiz: List of quiz question dictionaries
    """
    init_quiz_state(quiz)
    
    st.markdown("---")
    st.markdown("## 🧪 Practice Quiz")
    st.markdown("Test your understanding of the material!")
    
    if not quiz:
        st.warning("No quiz questions available.")
        return
    
    # Render each question
    for i, q in enumerate(quiz):
        render_question(i, q)
    
    # Submit button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📊 Submit Quiz", type="primary", use_container_width=True):
            st.session_state.quiz_submitted = True
            st.rerun()
    
    # Show results if submitted
    if st.session_state.quiz_submitted:
        render_results(quiz)


def render_question(index: int, question: dict):
    """
    Render a single quiz question.
    
    Args:
        index: Question index
        question: Question dictionary
    """
    q_num = index + 1
    is_submitted = st.session_state.quiz_submitted
    user_answer = st.session_state.quiz_answers.get(index)
    correct_answer = question.get('answer', '')
    
    # Question container
    with st.container():
        st.markdown(f"### Question {q_num}")
        st.markdown(question.get('question', ''))
        
        # Options
        options = question.get('options', {})
        
        if isinstance(options, dict):
            option_list = [f"{k}: {v}" for k, v in options.items()]
            option_keys = list(options.keys())
        else:
            option_list = options
            option_keys = [chr(65 + i) for i in range(len(options))]  # A, B, C, D
        
        if is_submitted:
            # Show results mode
            for opt_key, opt_display in zip(option_keys, option_list):
                if opt_key == correct_answer:
                    st.success(f"✅ {opt_display}")
                elif opt_key == user_answer:
                    st.error(f"❌ {opt_display}")
                else:
                    st.markdown(f"⬜ {opt_display}")
            
            # Show explanation if available
            if question.get('explanation'):
                st.info(f"💡 **Explanation:** {question['explanation']}")
        else:
            # Interactive mode
            selected = st.radio(
                f"Select answer for Q{q_num}",
                options=option_keys,
                format_func=lambda x: f"{x}: {options.get(x, x) if isinstance(options, dict) else options[option_keys.index(x)]}",
                key=f"q_{index}",
                index=None,
                label_visibility="collapsed"
            )
            
            if selected:
                st.session_state.quiz_answers[index] = selected
        
        st.markdown("---")


def render_results(quiz: list):
    """
    Render quiz results with score.
    
    Args:
        quiz: List of quiz question dictionaries
    """
    correct = 0
    total = len(quiz)
    
    for i, q in enumerate(quiz):
        user_answer = st.session_state.quiz_answers.get(i)
        if user_answer == q.get('answer'):
            correct += 1
    
    score_percent = (correct / total) * 100 if total > 0 else 0
    
    # Score display
    st.markdown("## 🏆 Results")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", f"{correct}/{total}")
    with col2:
        st.metric("Percentage", f"{score_percent:.0f}%")
    with col3:
        if score_percent >= 80:
            st.metric("Grade", "Excellent! 🌟")
        elif score_percent >= 60:
            st.metric("Grade", "Good! 👍")
        else:
            st.metric("Grade", "Keep Practicing! 📚")
    
    # Progress bar
    st.progress(score_percent / 100)
    
    # Retry button
    if st.button("🔄 Try Again"):
        st.session_state.quiz_submitted = False
        st.session_state.quiz_answers = {}
        st.rerun()
