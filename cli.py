"""
Command-line interface for Twitter Video Downloader.
"""

import argparse
import os
import sys

# Get version from __init__.py
def get_version():
    try:
        with open(os.path.join(os.path.dirname(__file__), "__init__.py"), "r") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip("\"'")
    except:
        pass
    return "1.0.0"

__version__ = get_version()


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Twitter Video Downloader - Tool for downloading Twitter videos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  python3 main.py https://twitter.com/username/status/1234567890
  python3 main.py -u https://x.com/username/status/1234567890
  python3 main.py --url "https://twitter.com/username/status/1234567890"
  python3 main.py https://twitter.com/username/status/1234567890 -o my_video.mp4
  python3 main.py https://twitter.com/username/status/1234567890 -d downloads/
  python3 main.py https://twitter.com/username/status/1234567890 -o video.mp4 -d ~/Videos/
        """
    )
    
    parser.add_argument(
        "url",
        nargs="?",
        help="Twitter post URL to download video from"
    )
    
    parser.add_argument(
        "-u", "--url",
        dest="url_flag",
        help="Twitter post URL to download video from (alternative way)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output filename (optional, defaults to timestamp-based name)"
    )
    
    parser.add_argument(
        "-d", "--output-dir",
        help="Output directory (optional, defaults to current directory or configured default)"
    )
    
    parser.add_argument(
        "--set-default-dir",
        help="Set default output directory for future downloads"
    )
    
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Show current configuration"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"Twitter Video Downloader {__version__}"
    )
    
    return parser.parse_args()


def get_twitter_url_from_args(args):
    """
    Get Twitter URL from command line arguments.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        str or None: Twitter URL, or None if not provided
    """
    return args.url or args.url_flag
