# Twitter Video Downloader

A Python tool for downloading videos from Twitter posts. The application uses the TwitSave service to extract video URLs and downloads the highest quality version available.

*This project is a fork of [XiaomingX/twitter-video-download](https://github.com/XiaomingX/twitter-video-download) with enhanced features, modular architecture, and comprehensive CLI support.*

## Features

- 🎥 Download videos from Twitter posts
- 📱 Automatically selects the highest quality video available
- 📊 Real-time download progress bar
- 💾 Saves videos with timestamp-based filenames
- 📁 Custom output directory support
- ⚙️ Configuration file support
- 🔧 Command-line interface with multiple options
- 🚀 Simple and easy to use
- 🏗️ Modular code structure

## How It Works

1. **URL Processing**: Takes a Twitter post URL as input
2. **Video Extraction**: Uses TwitSave.com API to extract available video download links
3. **Quality Selection**: Automatically selects the highest quality video available
4. **Download**: Downloads the video with a progress bar showing download status
5. **File Naming**: Saves the video with a timestamp-based filename (e.g., `1683738905.mp4`)

## Installation

### Quick Setup (Recommended)

1. Clone this repository:
```bash
git clone https://github.com/TSOlami/twitter-video-download.git
cd twitter-video-download
```

2. Run the setup script:
```bash
./setup.sh
```

This will automatically create a virtual environment and install all dependencies.

### Manual Setup

1. Clone this repository:
```bash
git clone https://github.com/TSOlami/twitter-video-download.git
cd twitter-video-download
```

2. Create and activate a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Usage

Make sure to activate your virtual environment first:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

You can now use the tool directly from the command line with any Twitter URL:

```bash
# Basic usage with URL as positional argument
python3 main.py https://twitter.com/username/status/1234567890

# Using the --url flag
python3 main.py --url https://twitter.com/username/status/1234567890

# Using short flag
python3 main.py -u https://x.com/username/status/1234567890

# With custom output filename
python3 main.py https://twitter.com/username/status/1234567890 -o my_video.mp4

# With custom output directory
python3 main.py https://twitter.com/username/status/1234567890 -d downloads/

# With both custom filename and directory
python3 main.py https://twitter.com/username/status/1234567890 -o video.mp4 -d ~/Videos/

# Set default output directory for future downloads
python3 main.py --set-default-dir ~/Downloads/Twitter-Videos

# Show current configuration
python3 main.py --show-config

# Get help
python3 main.py --help

# Check version
python3 main.py --version
```

### Supported URL formats
- `https://twitter.com/username/status/1234567890`
- `https://x.com/username/status/1234567890`
- `https://mobile.twitter.com/username/status/1234567890`
- `https://m.twitter.com/username/status/1234567890`

### Programmatic Usage
You can also use the functions directly in your Python code:

```python
# Import the main functions
from downloader import download_twitter_video, extract_video_url
from utils import validate_twitter_url

# Download a video from a Twitter post
download_twitter_video("https://twitter.com/username/status/1234567890")

# Download with custom filename
download_twitter_video("https://twitter.com/username/status/1234567890", "my_video.mp4")

# Just extract the video URL without downloading
video_url = extract_video_url("https://twitter.com/username/status/1234567890")

# Validate a Twitter URL
is_valid = validate_twitter_url("https://twitter.com/username/status/1234567890")
```

## Dependencies

- **requests**: For making HTTP requests to TwitSave API
- **beautifulsoup4**: For parsing HTML responses and extracting download links
- **tqdm**: For displaying download progress bars

## Project Structure

The project is now organized in a modular way:

```
twitter-video-download/
├── main.py              # Main entry point and CLI interface
├── downloader.py        # Core video downloading functionality
├── utils.py            # URL validation and utility functions
├── cli.py              # Command-line argument parsing
├── config.py           # Configuration management
├── __init__.py         # Package initialization
├── requirements.txt    # Python dependencies
├── setup.py            # Package setup script
├── setup.sh            # Automated setup script
├── README.md          # This file
├── LICENSE            # Apache 2.0 license
└── venv/              # Virtual environment (created after setup)
```

### Module Descriptions

- **`main.py`**: Entry point that orchestrates the CLI and delegates to other modules
- **`downloader.py`**: Contains video downloading logic and TwitSave API interaction
- **`utils.py`**: URL validation and normalization utilities
- **`cli.py`**: Command-line argument parsing and help text
- **`config.py`**: Configuration file management and default settings
- **`__init__.py`**: Package initialization and public API exports

## Code Structure

### Core Functions

- `download_video(video_url, output_file_name, output_dir=None)`: Downloads a video from a direct URL with progress tracking
- `download_twitter_video(twitter_post_url, custom_filename=None, output_dir=None)`: Extracts video URL from Twitter post and initiates download
- `extract_video_url(twitter_post_url)`: Extracts the video download URL without downloading
- `validate_twitter_url(url)`: Validates Twitter URL format
- `normalize_twitter_url(url)`: Standardizes Twitter URL format
- `parse_arguments()`: Handles command-line argument parsing
- `load_config()`: Loads user configuration from file
- `get_default_output_dir()`: Gets the configured default output directory
- `set_default_output_dir(output_dir)`: Sets the default output directory
- `main()`: Entry point with command-line interface

## Configuration

The application supports a configuration file located at `~/.twitter-video-download/config.json`. You can:

- Set a default output directory that will be used for all downloads
- Configure request timeout and retry settings
- Set a custom User-Agent string
- Configure default filename patterns

Use `python3 main.py --show-config` to see current settings and `python3 main.py --set-default-dir <directory>` to set a default output directory.

## Output

Downloaded videos are saved in the current working directory with filenames based on Unix timestamps (e.g., `1683738905.mp4`).

## Contributing

Contributions are welcome! Some potential improvements:
- [x] Add command-line argument support for custom URLs
- [x] Modular code structure
- [x] Better error handling
- [x] Custom output directory options
- [x] Configuration file support
- [ ] Support for multiple video quality options
- [ ] Support for downloading multiple videos from a list
- [ ] Progress saving for interrupted downloads
- [ ] Batch download from URL list file
- [ ] GUI interface

## Acknowledgments

This project is a fork of [XiaomingX/twitter-video-download](https://github.com/XiaomingX/twitter-video-download). Major enhancements include:
- Modular code architecture
- Comprehensive CLI interface with multiple options
- Configuration file support with persistent settings
- Enhanced error handling and validation
- Custom output directory support
- Detailed documentation and setup automation

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational purposes. Please respect Twitter's Terms of Service and copyright laws when downloading content.
