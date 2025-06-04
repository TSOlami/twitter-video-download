#!/usr/bin/env python3
"""
Test script for Twitter Video Downloader
Tests various components and functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import validate_twitter_url, normalize_twitter_url
from config import load_config, get_default_output_dir, set_default_output_dir
from cli import parse_arguments
import tempfile
import shutil


def test_url_validation():
    """Test URL validation functionality"""
    print("🧪 Testing URL validation...")
    
    # Valid URLs
    valid_urls = [
        "https://twitter.com/user/status/123456789",
        "https://x.com/user/status/123456789",
        "https://mobile.twitter.com/user/status/123456789",
        "https://m.twitter.com/user/status/123456789"
    ]
    
    # Invalid URLs
    invalid_urls = [
        "https://facebook.com/post/123",
        "https://youtube.com/watch?v=123",
        "https://twitter.com/user",  # Missing status
        "not-a-url",
        ""
    ]
    
    # Test valid URLs
    for url in valid_urls:
        if not validate_twitter_url(url):
            print(f"❌ Failed: {url} should be valid")
            return False
    
    # Test invalid URLs
    for url in invalid_urls:
        if validate_twitter_url(url):
            print(f"❌ Failed: {url} should be invalid")
            return False
    
    print("✅ URL validation tests passed")
    return True


def test_url_normalization():
    """Test URL normalization functionality"""
    print("🧪 Testing URL normalization...")
    
    test_cases = [
        ("twitter.com/user/status/123", "https://twitter.com/user/status/123"),
        ("http://twitter.com/user/status/123", "https://twitter.com/user/status/123"),
        ("https://twitter.com/user/status/123?ref=src", "https://twitter.com/user/status/123"),
        ("https://twitter.com/user/status/123#replies", "https://twitter.com/user/status/123")
    ]
    
    for input_url, expected in test_cases:
        result = normalize_twitter_url(input_url)
        if result != expected:
            print(f"❌ Failed: {input_url} -> {result}, expected {expected}")
            return False
    
    print("✅ URL normalization tests passed")
    return True


def test_config_functionality():
    """Test configuration management"""
    print("🧪 Testing configuration functionality...")
    
    # Test loading default config
    config = load_config()
    expected_keys = ["default_output_dir", "user_agent", "timeout", "max_retries"]
    
    for key in expected_keys:
        if key not in config:
            print(f"❌ Failed: Missing config key {key}")
            return False
    
    # Test setting and getting default output dir
    test_dir = tempfile.mkdtemp()
    try:
        set_default_output_dir(test_dir)
        retrieved_dir = get_default_output_dir()
        
        if retrieved_dir != test_dir:
            print(f"❌ Failed: Set {test_dir}, got {retrieved_dir}")
            return False
    finally:
        # Clean up
        shutil.rmtree(test_dir, ignore_errors=True)
    
    print("✅ Configuration tests passed")
    return True


def test_cli_parsing():
    """Test command-line argument parsing"""
    print("🧪 Testing CLI argument parsing...")
    
    # Mock sys.argv for testing
    original_argv = sys.argv
    
    try:
        # Test basic URL parsing
        sys.argv = ["main.py", "https://twitter.com/user/status/123"]
        args = parse_arguments()
        
        if args.url != "https://twitter.com/user/status/123":
            print(f"❌ Failed: Expected URL not parsed correctly")
            return False
        
        # Test with flags
        sys.argv = ["main.py", "-u", "https://x.com/user/status/456", "-o", "test.mp4"]
        args = parse_arguments()
        
        if args.url_flag != "https://x.com/user/status/456" or args.output != "test.mp4":
            print(f"❌ Failed: Flags not parsed correctly")
            return False
            
    finally:
        sys.argv = original_argv
    
    print("✅ CLI parsing tests passed")
    return True


def run_all_tests():
    """Run all tests"""
    print("🚀 Running Twitter Video Downloader Tests\n")
    
    tests = [
        test_url_validation,
        test_url_normalization,
        test_config_functionality,
        test_cli_parsing
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print()
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            print()
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
