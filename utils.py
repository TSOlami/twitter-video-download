"""
URL validation utilities for Twitter Video Downloader.
"""


def validate_twitter_url(url):
    """
    验证Twitter URL格式。
    
    参数:
        url (str): 要验证的URL
        
    返回:
        bool: 如果URL有效返回True，否则返回False
    """
    if not url:
        return False
    
    valid_domains = ['twitter.com', 'x.com', 'mobile.twitter.com', 'm.twitter.com']
    url_lower = url.lower()
    
    return any(domain in url_lower for domain in valid_domains) and '/status/' in url_lower


def normalize_twitter_url(url):
    """
    标准化Twitter URL格式。
    
    参数:
        url (str): 原始URL
        
    返回:
        str: 标准化后的URL
    """
    if not url:
        return url
    
    # 移除可能的查询参数和片段
    if '?' in url:
        url = url.split('?')[0]
    if '#' in url:
        url = url.split('#')[0]
    
    # 确保使用HTTPS
    if url.startswith('http://'):
        url = url.replace('http://', 'https://')
    elif not url.startswith('https://'):
        url = 'https://' + url
    
    return url
