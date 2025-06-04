"""
URL validation utilities for Twitter Video Downloader.
"""


def validate_twitter_url(url):
    """
    Validate Twitter URL format.
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
    """
    if not url:
        return False
    
    valid_domains = ['twitter.com', 'x.com', 'mobile.twitter.com', 'm.twitter.com']
    url_lower = url.lower()
    
    return any(domain in url_lower for domain in valid_domains) and '/status/' in url_lower


def normalize_twitter_url(url):
    """
    Normalize Twitter URL format.
    
    Args:
        url (str): Original URL
        
    Returns:
        str: Normalized URL
    """
    if not url:
        return url
    
    # Remove possible query parameters and fragments
    if '?' in url:
        url = url.split('?')[0]
    if '#' in url:
        url = url.split('#')[0]
    
    # Ensure HTTPS is used
    if url.startswith('http://'):
        url = url.replace('http://', 'https://')
    elif not url.startswith('https://'):
        url = 'https://' + url
    
    return url
