"""
AI Engine module.
Handles LLM integration with Google Gemini and DeepSeek for summarization and quiz generation.
"""
import json
import re
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import GEMINI_API_KEY, DEEPSEEK_API_KEY, AVAILABLE_MODELS, DEFAULT_NUM_QUESTIONS
from modules.text_processor import chunk_text


def get_llm(model_name: str = None):
    """
    Get configured LLM instance based on selected model.
    
    Args:
        model_name: Key from AVAILABLE_MODELS dict (e.g., "Gemini 2.5 Pro", "DeepSeek Chat")
        
    Returns:
        Configured LLM instance
    """
    if model_name is None:
        model_name = "Gemini 2.5 Pro"
    
    if model_name not in AVAILABLE_MODELS:
        raise ValueError(f"Unknown model: {model_name}")
    
    model_config = AVAILABLE_MODELS[model_name]
    provider = model_config["provider"]
    model_id = model_config["model_name"]
    
    if provider == "gemini":
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
        
        return ChatGoogleGenerativeAI(
            model=model_id,
            google_api_key=GEMINI_API_KEY,
            temperature=0.3
        )
    
    elif provider == "deepseek":
        if not DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY not found. Please set it in your .env file.")
        
        return ChatOpenAI(
            model=model_id,
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com",
            temperature=0.3
        )
    
    else:
        raise ValueError(f"Unknown provider: {provider}")


# Prompt Templates
SUMMARY_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="""You are an expert educational content summarizer. Analyze the following lecture material and create a comprehensive summary.

LECTURE MATERIAL:
{text}

Create a well-structured summary that includes:
1. **Main Topic**: A brief one-line description of what this lecture is about
2. **Key Concepts**: List the 3-5 most important concepts covered
3. **Detailed Summary**: A thorough but concise summary of the main points
4. **Key Takeaways**: 3-5 bullet points that students should remember

Format your response in Markdown for clear readability."""
)

CHUNK_SUMMARY_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="""Summarize the following section of lecture material concisely, capturing all key points:

{text}

Provide a concise summary that preserves the main ideas and important details."""
)

COMBINE_SUMMARY_PROMPT = PromptTemplate(
    input_variables=["summaries"],
    template="""You are an expert educational content summarizer. Combine the following partial summaries into one comprehensive, well-structured summary.

PARTIAL SUMMARIES:
{summaries}

Create a unified summary that includes:
1. **Main Topic**: A brief one-line description of what this lecture is about
2. **Key Concepts**: List the 3-5 most important concepts covered
3. **Detailed Summary**: A thorough but concise summary of the main points
4. **Key Takeaways**: 3-5 bullet points that students should remember

Format your response in Markdown for clear readability."""
)

QUIZ_PROMPT = PromptTemplate(
    input_variables=["summary", "num_questions"],
    template="""Based on the following lecture summary, create {num_questions} multiple-choice quiz questions to test student understanding.

LECTURE SUMMARY:
{summary}

Requirements:
- Each question should test a key concept from the material
- Provide 4 answer options (A, B, C, D) for each question
- Ensure only one option is correct
- Make incorrect options plausible but clearly wrong
- Vary the difficulty from basic recall to application

IMPORTANT: Respond ONLY with a valid JSON array. No additional text before or after.

Format:
[
    {{
        "question": "Your question here?",
        "options": {{
            "A": "First option",
            "B": "Second option", 
            "C": "Third option",
            "D": "Fourth option"
        }},
        "answer": "A",
        "explanation": "Brief explanation of why this is correct"
    }}
]"""
)


def summarize_text(text: str, model_name: str = None) -> dict:
    """
    Generate a summary of the provided text.
    Automatically handles chunking for long texts.
    
    Args:
        text: Text content to summarize
        model_name: LLM model to use
        
    Returns:
        Dictionary with 'success', 'summary', and optional 'error'
    """
    try:
        llm = get_llm(model_name)
        
        # Check if text needs chunking (rough estimate: 1 token ≈ 4 chars)
        if len(text) > 30000:  # ~7500 tokens
            return summarize_long_text(text, model_name)
        
        chain = SUMMARY_PROMPT | llm | StrOutputParser()
        result = chain.invoke({"text": text})
        
        return {
            'success': True,
            'summary': result
        }
        
    except Exception as e:
        return {
            'success': False,
            'summary': '',
            'error': f'Error generating summary: {str(e)}'
        }


def summarize_long_text(text: str, model_name: str = None) -> dict:
    """
    Summarize long text using map-reduce approach.
    Chunks the text, summarizes each chunk, then combines.
    
    Args:
        text: Long text content
        model_name: LLM model to use
        
    Returns:
        Dictionary with 'success', 'summary', and optional 'error'
    """
    try:
        llm = get_llm(model_name)
        
        # Chunk the text
        chunks = chunk_text(text, chunk_size=8000, chunk_overlap=500)
        
        # Summarize each chunk
        chunk_chain = CHUNK_SUMMARY_PROMPT | llm | StrOutputParser()
        chunk_summaries = []
        
        for chunk in chunks:
            summary = chunk_chain.invoke({"text": chunk})
            chunk_summaries.append(summary)
        
        # Combine all summaries
        combined_text = "\n\n---\n\n".join(chunk_summaries)
        
        combine_chain = COMBINE_SUMMARY_PROMPT | llm | StrOutputParser()
        final_summary = combine_chain.invoke({"summaries": combined_text})
        
        return {
            'success': True,
            'summary': final_summary,
            'chunks_processed': len(chunks)
        }
        
    except Exception as e:
        return {
            'success': False,
            'summary': '',
            'error': f'Error summarizing long text: {str(e)}'
        }


def generate_quiz(summary: str, num_questions: int = None, model_name: str = None) -> dict:
    """
    Generate a multiple-choice quiz based on the summary.
    
    Args:
        summary: Summary text to generate quiz from
        num_questions: Number of questions to generate
        model_name: LLM model to use
        
    Returns:
        Dictionary with 'success', 'quiz', and optional 'error'
    """
    if num_questions is None:
        num_questions = DEFAULT_NUM_QUESTIONS
    
    try:
        llm = get_llm(model_name)
        chain = QUIZ_PROMPT | llm | StrOutputParser()
        
        result = chain.invoke({"summary": summary, "num_questions": num_questions})
        
        # Parse JSON response
        quiz = parse_quiz_response(result)
        
        if quiz:
            return {
                'success': True,
                'quiz': quiz
            }
        else:
            return {
                'success': False,
                'quiz': [],
                'error': 'Failed to parse quiz response. Please try again.'
            }
        
    except Exception as e:
        return {
            'success': False,
            'quiz': [],
            'error': f'Error generating quiz: {str(e)}'
        }


def parse_quiz_response(response: str) -> list:
    """
    Parse the LLM response to extract quiz JSON.
    
    Args:
        response: Raw LLM response string
        
    Returns:
        List of quiz question dictionaries or None
    """
    try:
        # Try direct JSON parse
        return json.loads(response)
    except json.JSONDecodeError:
        pass
    
    # Try to extract JSON from response
    try:
        # Find JSON array in response
        match = re.search(r'\[[\s\S]*\]', response)
        if match:
            return json.loads(match.group())
    except (json.JSONDecodeError, AttributeError):
        pass
    
    return None
