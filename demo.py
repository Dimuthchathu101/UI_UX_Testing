#!/usr/bin/env python3
"""
Demo script for the UI/UX Testing Tool
This script demonstrates how to use the comprehensive UI/UX testing tool
"""

import sys
import os
from ui_ux_tester import run_ui_ux_test, generate_report, export_results

def run_demo():
    """Run a demo test on a sample website"""
    
    print("🎯 UI/UX Testing Tool Demo")
    print("=" * 50)
    print("This demo will test a sample website against all 10 UI/UX design principles:")
    print()
    print("1. Simplicity - Easy to use and navigate")
    print("2. User-Centered Design - Focus on user needs")
    print("3. Visibility - Clear interface highlighting important tasks")
    print("4. Consistency - Consistent design elements")
    print("5. Feedback - Visual cues and success messages")
    print("6. Clarity - Clear content and interface elements")
    print("7. Accessibility - Usable by everyone")
    print("8. Usability - Easy to use and navigate")
    print("9. Efficiency - Optimized for speed and performance")
    print("10. Delight - Positive user emotions and engagement")
    print()
    
    # Demo URL - using a well-known website for testing
    demo_url = "https://www.google.com"
    
    print(f"Testing: {demo_url}")
    print("This will take a few moments...")
    print()
    
    try:
        # Run the comprehensive test
        results = run_ui_ux_test(demo_url)
        
        # Generate the report
        generate_report(results)
        
        # Export results for demonstration
        export_filename = export_results(results, "demo_results.json")
        
        print("\n" + "=" * 50)
        print("🎉 Demo completed successfully!")
        print(f"📄 Results exported to: {export_filename}")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("Please check your internet connection and try again.")
        return False

def show_usage_examples():
    """Show usage examples for the tool"""
    
    print("\n📚 Usage Examples:")
    print("=" * 30)
    print()
    print("1. Basic test (interactive):")
    print("   python ui_ux_tester.py")
    print()
    print("2. Test specific website:")
    print("   python ui_ux_tester.py --url https://example.com")
    print()
    print("3. Export results to JSON:")
    print("   python ui_ux_tester.py --url https://example.com --export")
    print()
    print("4. Custom output filename:")
    print("   python ui_ux_tester.py --url https://example.com --export --output my_results.json")
    print()

if __name__ == "__main__":
    print("🚀 Starting UI/UX Testing Tool Demo...")
    print()
    
    success = run_demo()
    
    if success:
        show_usage_examples()
        
        print("💡 Tips:")
        print("- The tool works best with public websites")
        print("- Some websites may block automated testing")
        print("- Results are scored from 0-100 for each principle")
        print("- Use the --export flag to save results for analysis")
        print()
        print("🎯 Ready to test your own websites!")
    else:
        print("\n🔧 Troubleshooting:")
        print("- Ensure you have Chrome browser installed")
        print("- Check your internet connection")
        print("- Try running: pip install -r requirements.txt")
        print("- Make sure you're in the correct directory") 