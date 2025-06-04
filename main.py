import os
import requests
import bs4
from tqdm import tqdm
from pathlib import Path
import time
import argparse
import sys

# 定义一个函数，用于下载视频
def download_video(video_url, output_file_name) -> None:
    """
    从指定的URL下载视频到本地。

    参数:
        video_url (str): 要下载的视频的URL。
        output_file_name (str): 保存视频的文件名或路径。
    """

    # 发起请求，获取响应
    response = requests.get(video_url, stream=True)
    # 获取内容的总大小
    total_size = int(response.headers.get("content-length", 0))
    # 设置块大小
    block_size = 1024
    # 初始化进度条
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

    # 使用当前运行路径为下载路径
    download_path = os.path.join(os.getcwd(), output_file_name)

    # 以二进制写模式打开文件
    with open(download_path, "wb") as video_file:
        for data_chunk in response.iter_content(block_size):
            progress_bar.update(len(data_chunk))
            video_file.write(data_chunk)

    # 关闭进度条
    progress_bar.close()
    print("视频成功下载！")
    print("视频保存路径：" + download_path)

# 定义一个函数，用于下载Twitter视频
def download_twitter_video(twitter_post_url):
    """
    提取并下载Twitter帖子中的最高质量视频。

    参数:
        twitter_post_url (str): Twitter帖子URL。
    """

    # 构建API URL
    api_request_url = f"https://twitsave.com/info?url={twitter_post_url}"

    # 发起请求，获取响应
    response = requests.get(api_request_url)
    page_content = bs4.BeautifulSoup(response.text, "html.parser")
    # 查找下载按钮
    download_section = page_content.find_all("div", class_="origin-top-right")[0]
    # 查找质量选择按钮
    quality_links = download_section.find_all("a")
    # 获取最高质量视频的URL
    highest_quality_video_url = quality_links[0].get("href")
    
    # 使用时间戳生成视频文件名
    timestamp = int(time.time())
    video_file_name = f"{timestamp}.mp4"
    
    # 调用下载视频函数
    download_video(highest_quality_video_url, video_file_name)

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
        "--version",
        action="version",
        version="Twitter Video Downloader 1.0.0"
    )
    
    return parser.parse_args()

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

def main():
    args = parse_arguments()
    
    # 获取URL（优先使用位置参数，然后是--url标志）
    twitter_url = args.url or args.url_flag
    
    if not twitter_url:
        print("错误: 请提供Twitter视频URL")
        print("使用方法: python3 main.py <twitter_url>")
        print("或者: python3 main.py --url <twitter_url>")
        print("使用 --help 查看更多选项")
        sys.exit(1)
    
    # 验证URL格式
    if not validate_twitter_url(twitter_url):
        print(f"错误: 无效的Twitter URL: {twitter_url}")
        print("请确保URL包含 twitter.com 或 x.com 并包含 /status/")
        sys.exit(1)
    
    print(f"正在下载视频来自: {twitter_url}")
    
    try:
        # 如果提供了自定义输出文件名，修改download_twitter_video函数调用
        if args.output:
            download_twitter_video_with_custom_name(twitter_url, args.output)
        else:
            download_twitter_video(twitter_url)
    except Exception as e:
        print(f"下载失败: {str(e)}")
        sys.exit(1)

def download_twitter_video_with_custom_name(twitter_post_url, custom_filename):
    """
    提取并下载Twitter帖子中的最高质量视频，使用自定义文件名。

    参数:
        twitter_post_url (str): Twitter帖子URL。
        custom_filename (str): 自定义文件名。
    """

    # 构建API URL
    api_request_url = f"https://twitsave.com/info?url={twitter_post_url}"

    # 发起请求，获取响应
    response = requests.get(api_request_url)
    page_content = bs4.BeautifulSoup(response.text, "html.parser")
    # 查找下载按钮
    download_section = page_content.find_all("div", class_="origin-top-right")[0]
    # 查找质量选择按钮
    quality_links = download_section.find_all("a")
    # 获取最高质量视频的URL
    highest_quality_video_url = quality_links[0].get("href")
    
    # 确保文件名有.mp4扩展名
    if not custom_filename.lower().endswith('.mp4'):
        custom_filename += '.mp4'
    
    # 调用下载视频函数
    download_video(highest_quality_video_url, custom_filename)

if __name__ == "__main__":
    main()
