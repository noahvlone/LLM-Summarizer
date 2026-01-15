"""
Text processing utilities.
Handles chunking of long text content for LLM processing.
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text: str, chunk_size: int = None, chunk_overlap: int = None) -> list[str]:
    """
    Split long text into manageable chunks.
    
    Uses RecursiveCharacterTextSplitter for intelligent splitting
    that respects sentence and paragraph boundaries.
    
    Args:
        text: The text to split
        chunk_size: Maximum size of each chunk (default from config)
        chunk_overlap: Overlap between chunks (default from config)
        
    Returns:
        List of text chunks
    """
    if chunk_size is None:
        chunk_size = CHUNK_SIZE
    if chunk_overlap is None:
        chunk_overlap = CHUNK_OVERLAP
    
    # If text is short enough, return as single chunk
    if len(text) <= chunk_size:
        return [text]
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = splitter.split_text(text)
    
    return chunks


def estimate_tokens(text: str) -> int:
    """
    Estimate the number of tokens in a text.
    Rough estimation: ~4 characters per token for English.
    
    Args:
        text: Input text
        
    Returns:
        Estimated token count
    """
    return len(text) // 4


def clean_text(text: str) -> str:
    """
    Clean and normalize text content.
    
    Args:
        text: Raw text content
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    import re
    text = re.sub(r'\s+', ' ', text)
    
    # Remove excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()
