"""
Twitter Video Downloader

A Python tool for downloading videos from Twitter posts.
Fork of XiaomingX/twitter-video-download with enhanced features.
"""

__version__ = "1.0.0"
__author__ = "TSOlami"

from .downloader import download_twitter_video, download_video, extract_video_url
from .utils import validate_twitter_url, normalize_twitter_url
from .cli import parse_arguments, get_twitter_url_from_args

__all__ = [
    'download_twitter_video',
    'download_video', 
    'extract_video_url',
    'validate_twitter_url',
    'normalize_twitter_url',
    'parse_arguments',
    'get_twitter_url_from_args'
]
