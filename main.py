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
    """主函数 - 处理命令行参数并执行下载。"""
    args = parse_arguments()
    
    # 处理配置相关的命令
    if args.show_config:
        config = load_config()
        print("当前配置:")
        for key, value in config.items():
            print(f"  {key}: {value}")
        return
    
    if args.set_default_dir:
        set_default_output_dir(args.set_default_dir)
        print(f"默认输出目录已设置为: {args.set_default_dir}")
        return
    
    # 获取URL（优先使用位置参数，然后是--url标志）
    twitter_url = get_twitter_url_from_args(args)
    
    if not twitter_url:
        print("错误: 请提供Twitter视频URL")
        print("使用方法: python3 main.py <twitter_url>")
        print("或者: python3 main.py --url <twitter_url>")
        print("使用 --help 查看更多选项")
        sys.exit(1)
    
    # 标准化和验证URL格式
    twitter_url = normalize_twitter_url(twitter_url)
    if not validate_twitter_url(twitter_url):
        print(f"错误: 无效的Twitter URL: {twitter_url}")
        print("请确保URL包含 twitter.com 或 x.com 并包含 /status/")
        sys.exit(1)
    
    print(f"正在下载视频来自: {twitter_url}")
    
    try:
        # 下载视频，如果提供了自定义文件名则使用它
        download_twitter_video(twitter_url, args.output, args.output_dir)
        print("下载完成！")
    except Exception as e:
        print(f"下载失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
