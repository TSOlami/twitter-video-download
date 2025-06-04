"""
Configuration management for Twitter Video Downloader.
"""

import os
import json
from pathlib import Path


def get_config_file_path():
    """获取配置文件路径。"""
    config_dir = Path.home() / ".twitter-video-download"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "config.json"


def load_config():
    """加载配置文件。"""
    config_file = get_config_file_path()
    default_config = {
        "default_output_dir": None,
        "default_filename_pattern": "{timestamp}.mp4",
        "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "timeout": 30,
        "max_retries": 3
    }
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except (json.JSONDecodeError, IOError):
            pass
    
    return default_config


def save_config(config):
    """保存配置到文件。"""
    config_file = get_config_file_path()
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"警告: 无法保存配置文件: {str(e)}")


def get_default_output_dir():
    """获取默认输出目录。"""
    config = load_config()
    default_dir = config.get("default_output_dir")
    
    if default_dir:
        return os.path.expanduser(default_dir)
    
    return None


def set_default_output_dir(output_dir):
    """设置默认输出目录。"""
    config = load_config()
    config["default_output_dir"] = output_dir
    save_config(config)
