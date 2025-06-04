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
    从指定的URL下载视频到本地。

    参数:
        video_url (str): 要下载的视频的URL。
        output_file_name (str): 保存视频的文件名或路径。
        output_dir (str, optional): 输出目录，默认为当前目录。
        
    异常:
        requests.RequestException: 网络请求失败
        IOError: 文件写入失败
    """
    try:
        # 发起请求，获取响应
        response = requests.get(video_url, stream=True, timeout=30)
        response.raise_for_status()  # 检查HTTP错误
        
        # 获取内容的总大小
        total_size = int(response.headers.get("content-length", 0))
        # 设置块大小
        block_size = 1024
        # 初始化进度条
        progress_bar = tqdm(total=total_size, unit="B", unit_scale=True, desc="下载中")

        # 确定下载路径
        if output_dir:
            # 确保输出目录存在
            os.makedirs(output_dir, exist_ok=True)
            download_path = os.path.join(output_dir, output_file_name)
        else:
            # 使用当前运行路径为下载路径
            download_path = os.path.join(os.getcwd(), output_file_name)

        # 以二进制写模式打开文件
        with open(download_path, "wb") as video_file:
            for data_chunk in response.iter_content(block_size):
                if data_chunk:  # 过滤空块
                    progress_bar.update(len(data_chunk))
                    video_file.write(data_chunk)

        # 关闭进度条
        progress_bar.close()
        print("视频成功下载！")
        print("视频保存路径：" + download_path)
        
    except requests.RequestException as e:
        raise requests.RequestException(f"下载失败: {str(e)}")
    except IOError as e:
        raise IOError(f"文件写入失败: {str(e)}")
    except Exception as e:
        raise Exception(f"下载过程中发生未知错误: {str(e)}")


def extract_video_url(twitter_post_url):
    """
    从Twitter帖子URL提取视频下载链接。

    参数:
        twitter_post_url (str): Twitter帖子URL。

    返回:
        str: 最高质量视频的下载URL。
        
    异常:
        requests.RequestException: 网络请求失败
        ValueError: URL解析失败或找不到视频
    """
    try:
        # 构建API URL
        api_request_url = f"https://twitsave.com/info?url={twitter_post_url}"

        # 加载配置
        config = load_config()
        headers = {
            'User-Agent': config.get('user_agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
        }
        timeout = config.get('timeout', 30)

        # 发起请求，获取响应
        response = requests.get(api_request_url, timeout=timeout, headers=headers)
        response.raise_for_status()  # 检查HTTP错误
        
        page_content = bs4.BeautifulSoup(response.text, "html.parser")
        
        # 查找下载按钮
        download_sections = page_content.find_all("div", class_="origin-top-right")
        if not download_sections:
            raise ValueError("无法找到视频下载链接，请检查URL是否包含视频")
            
        download_section = download_sections[0]
        
        # 查找质量选择按钮
        quality_links = download_section.find_all("a")
        if not quality_links:
            raise ValueError("无法找到视频下载链接")
            
        # 获取最高质量视频的URL
        highest_quality_video_url = quality_links[0].get("href")
        if not highest_quality_video_url:
            raise ValueError("无法获取视频下载URL")
            
        return highest_quality_video_url
        
    except requests.RequestException as e:
        raise requests.RequestException(f"网络请求失败: {str(e)}")
    except Exception as e:
        raise ValueError(f"解析视频URL失败: {str(e)}")


def download_twitter_video(twitter_post_url, custom_filename=None, output_dir=None):
    """
    提取并下载Twitter帖子中的最高质量视频。

    参数:
        twitter_post_url (str): Twitter帖子URL。
        custom_filename (str, optional): 自定义文件名。如果未提供，使用时间戳。
        output_dir (str, optional): 输出目录。如果未提供，尝试使用配置的默认目录。
    """
    # 提取视频URL
    video_url = extract_video_url(twitter_post_url)
    
    # 生成文件名
    if custom_filename:
        # 确保文件名有.mp4扩展名
        if not custom_filename.lower().endswith('.mp4'):
            custom_filename += '.mp4'
        filename = custom_filename
    else:
        # 使用时间戳生成视频文件名
        timestamp = int(time.time())
        filename = f"{timestamp}.mp4"
    
    # 确定输出目录
    if not output_dir:
        output_dir = get_default_output_dir()
    
    # 调用下载视频函数
    download_video(video_url, filename, output_dir)
