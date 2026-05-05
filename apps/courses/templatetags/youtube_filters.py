from django import template

register = template.Library()

@register.filter
def youtube_embed(url):
    """Convert YouTube URL to embed format"""
    if not url:
        return ''
    
    # Handle different YouTube URL formats
    if 'youtube.com/watch?v=' in url:
        video_id = url.split('v=')[1].split('&')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    elif 'youtu.be/' in url:
        video_id = url.split('youtu.be/')[1].split('?')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    elif 'youtube.com/embed/' in url:
        return url
    else:
        return url
