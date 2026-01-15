"""
YouTube transcript extraction module.
Handles fetching captions/transcripts from YouTube videos.
Compatible with youtube-transcript-api v1.0+
"""
import re
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str | None:
    """
    Extract YouTube video ID from various URL formats.
    
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    
    Args:
        url: YouTube video URL
        
    Returns:
        Video ID string or None if not found
    """
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'  # Direct video ID
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def get_transcript(video_id: str, languages: list[str] = None) -> dict:
    """
    Fetch transcript for a YouTube video.
    
    Args:
        video_id: YouTube video ID
        languages: Preferred languages, defaults to ['en', 'id']
        
    Returns:
        Dictionary with 'success', 'text', and optional 'error' keys
    """
    if languages is None:
        languages = ['en', 'id', 'en-US', 'en-GB']
    
    try:
        # New API in v1.0+: Use fetch() method
        ytt_api = YouTubeTranscriptApi()
        transcript_data = ytt_api.fetch(video_id, languages=languages)
        
        # Combine all text segments
        text = " ".join([segment.text for segment in transcript_data])
        
        return {
            'success': True,
            'text': text,
            'language': 'auto'
        }
        
    except Exception as e:
        error_msg = str(e)
        
        # Try without language preference as fallback
        try:
            ytt_api = YouTubeTranscriptApi()
            transcript_data = ytt_api.fetch(video_id)
            text = " ".join([segment.text for segment in transcript_data])
            
            return {
                'success': True,
                'text': text,
                'language': 'auto'
            }
        except Exception as fallback_error:
            # Provide user-friendly error messages
            fallback_msg = str(fallback_error).lower()
            
            if 'disabled' in fallback_msg:
                return {
                    'success': False,
                    'text': '',
                    'error': 'Transcripts are disabled for this video.'
                }
            elif 'unavailable' in fallback_msg or 'not found' in fallback_msg:
                return {
                    'success': False,
                    'text': '',
                    'error': 'Video is unavailable or no transcript found.'
                }
            else:
                return {
                    'success': False,
                    'text': '',
                    'error': f'Error fetching transcript: {str(fallback_error)}'
                }


def get_transcript_from_url(url: str) -> dict:
    """
    Convenience function to get transcript directly from URL.
    
    Args:
        url: YouTube video URL
        
    Returns:
        Dictionary with transcript data or error
    """
    video_id = extract_video_id(url)
    
    if not video_id:
        return {
            'success': False,
            'text': '',
            'error': 'Invalid YouTube URL. Please provide a valid YouTube video link.'
        }
    
    return get_transcript(video_id)
