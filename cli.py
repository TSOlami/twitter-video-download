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
    解析命令行参数。
    
    返回:
        argparse.Namespace: 解析后的命令行参数
    """
    parser = argparse.ArgumentParser(
        description="Twitter Video Downloader - 下载Twitter视频的工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
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
    从命令行参数中获取Twitter URL。
    
    参数:
        args: 解析后的命令行参数
        
    返回:
        str or None: Twitter URL，如果未提供则返回None
    """
    return args.url or args.url_flag
