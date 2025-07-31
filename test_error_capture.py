#!/usr/bin/env python3
"""
Test script to verify enhanced console error capture functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui_ux_tester import run_ui_ux_test

def test_error_capture():
    """Test the enhanced error capture functionality"""
    print("Testing enhanced console error capture...")
    
    # Test with a URL that might have JavaScript errors
    test_url = "https://httpstat.us/500"  # This will likely generate some errors
    
    print(f"Testing URL: {test_url}")
    results = run_ui_ux_test(test_url)
    
    print("\n" + "="*60)
    print("CONSOLE ERRORS CAPTURED:")
    print("="*60)
    
    if results["console_errors"]:
        print(f"Found {len(results['console_errors'])} console errors:")
        for i, error in enumerate(results["console_errors"], 1):
            print(f"\n{i}. {error['level']}: {error['message']}")
            print(f"   Source: {error.get('source', 'Unknown')}")
            if error.get('filename') and error.get('filename') != 'Unknown file':
                print(f"   File: {error['filename']}")
            if error.get('line') and error.get('line') != 'Unknown':
                print(f"   Line: {error['line']}, Column: {error.get('column', 'Unknown')}")
            if error.get('stack') and error.get('stack') != 'No stack trace available':
                print(f"   Stack: {error['stack'][:200]}...")
            print(f"   URL: {error['url']}")
    else:
        print("No console errors captured.")
    
    print("\n" + "="*60)
    print("TEST COMPLETED")
    print("="*60)

if __name__ == "__main__":
    test_error_capture() 