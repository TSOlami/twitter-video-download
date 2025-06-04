"""
Video downloader module for Twitter Video Downloader.
Handles the core video downloading functionality.
"""

import os
import requests
import bs4
from tqdm import tqdm
import time
from config import get_default_output_dir, load_config


def download_video(video_url, output_file_name, output_dir=None):
    """
    Download a video from the specified URL to local storage.

    Args:
        video_url (str): URL of the video to download.
        output_file_name (str): Filename or path to save the video.
        output_dir (str, optional): Output directory, defaults to current directory.
        
    Raises:
        requests.RequestException: Network request failed
        IOError: File write failed
    """
    try:
        # Send request and get response
        response = requests.get(video_url, stream=True, timeout=30)
        response.raise_for_status()  # Check for HTTP errors
        
        # Get total content size
        total_size = int(response.headers.get("content-length", 0))
        # Set block size
        block_size = 1024
        # Initialize progress bar
        progress_bar = tqdm(total=total_size, unit="B", unit_scale=True, desc="Downloading")

        # Determine download path
        if output_dir:
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            download_path = os.path.join(output_dir, output_file_name)
        else:
            # Use current working directory as download path
            download_path = os.path.join(os.getcwd(), output_file_name)

        # Open file in binary write mode
        with open(download_path, "wb") as video_file:
            for data_chunk in response.iter_content(block_size):
                if data_chunk:  # Filter empty blocks
                    progress_bar.update(len(data_chunk))
                    video_file.write(data_chunk)

        # Close progress bar
        progress_bar.close()
        print("Video downloaded successfully!")
        print("Video saved to: " + download_path)
        
    except requests.RequestException as e:
        raise requests.RequestException(f"Download failed: {str(e)}")
    except IOError as e:
        raise IOError(f"File write failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Unknown error occurred during download: {str(e)}")


def extract_video_url(twitter_post_url):
    """
    Extract video download link from Twitter post URL.

    Args:
        twitter_post_url (str): Twitter post URL.

    Returns:
        str: Download URL for the highest quality video.
        
    Raises:
        requests.RequestException: Network request failed
        ValueError: URL parsing failed or video not found
    """
    try:
        # Build API URL
        api_request_url = f"https://twitsave.com/info?url={twitter_post_url}"

        # Load configuration
        config = load_config()
        headers = {
            'User-Agent': config.get('user_agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
        }
        timeout = config.get('timeout', 30)

        # Send request and get response
        response = requests.get(api_request_url, timeout=timeout, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        
        page_content = bs4.BeautifulSoup(response.text, "html.parser")
        
        # Find download buttons
        download_sections = page_content.find_all("div", class_="origin-top-right")
        if not download_sections:
            raise ValueError("Unable to find video download links, please check if URL contains video")
            
        download_section = download_sections[0]
        
        # Find quality selection buttons
        quality_links = download_section.find_all("a")
        if not quality_links:
            raise ValueError("Unable to find video download links")
            
        # Get highest quality video URL
        highest_quality_video_url = quality_links[0].get("href")
        if not highest_quality_video_url:
            raise ValueError("Unable to get video download URL")
            
        return highest_quality_video_url
        
    except requests.RequestException as e:
        raise requests.RequestException(f"Network request failed: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to parse video URL: {str(e)}")


def download_twitter_video(twitter_post_url, custom_filename=None, output_dir=None):
    """
    Extract and download the highest quality video from a Twitter post.

    Args:
        twitter_post_url (str): Twitter post URL.
        custom_filename (str, optional): Custom filename. If not provided, uses timestamp.
        output_dir (str, optional): Output directory. If not provided, tries to use configured default directory.
    """
    # Extract video URL
    video_url = extract_video_url(twitter_post_url)
    
    # Generate filename
    if custom_filename:
        # Ensure filename has .mp4 extension
        if not custom_filename.lower().endswith('.mp4'):
            custom_filename += '.mp4'
        filename = custom_filename
    else:
        # Use timestamp to generate video filename
        timestamp = int(time.time())
        filename = f"{timestamp}.mp4"
    
    # Determine output directory
    if not output_dir:
        output_dir = get_default_output_dir()
    
    # Call download video function
    download_video(video_url, filename, output_dir)
