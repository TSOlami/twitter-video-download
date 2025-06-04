#!/usr/bin/env python3
"""
Twitter Video Downloader - Main entry point
A simple tool for downloading videos from Twitter posts.
"""

import sys
from cli import parse_arguments, get_twitter_url_from_args
from utils import validate_twitter_url, normalize_twitter_url
from downloader import download_twitter_video
from config import load_config, set_default_output_dir

def main():
    """Main function - handles command line arguments and executes download."""
    args = parse_arguments()
    
    # Handle configuration-related commands
    if args.show_config:
        config = load_config()
        print("Current configuration:")
        for key, value in config.items():
            print(f"  {key}: {value}")
        return
    
    if args.set_default_dir:
        set_default_output_dir(args.set_default_dir)
        print(f"Default output directory set to: {args.set_default_dir}")
        return
    
    # Get URL (prioritize positional argument, then --url flag)
    twitter_url = get_twitter_url_from_args(args)
    
    if not twitter_url:
        print("Error: Please provide a Twitter video URL")
        print("Usage: python3 main.py <twitter_url>")
        print("Or: python3 main.py --url <twitter_url>")
        print("Use --help to see more options")
        sys.exit(1)
    
    # Normalize and validate URL format
    twitter_url = normalize_twitter_url(twitter_url)
    if not validate_twitter_url(twitter_url):
        print(f"Error: Invalid Twitter URL: {twitter_url}")
        print("Please ensure URL contains twitter.com or x.com and includes /status/")
        sys.exit(1)
    
    print(f"Downloading video from: {twitter_url}")
    
    try:
        # Download video, use custom filename if provided
        download_twitter_video(twitter_url, args.output, args.output_dir)
        print("Download completed!")
    except Exception as e:
        print(f"Download failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
