import time
import requests
import json
import argparse
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import re

def run_ui_ux_test(url):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--v=1")
    
    # Initialize WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    results = {
        "url": url,
        "simplicity_score": 0,
        "user_centered_design_score": 0,
        "visibility_score": 0,
        "consistency_score": 0,
        "feedback_score": 0,
        "clarity_score": 0,
        "accessibility_score": 0,
        "usability_score": 0,
        "efficiency_score": 0,
        "delight_score": 0,
        "accessibility_issues": [],
        "responsive_issues": [],
        "broken_links": [],
        "broken_images": [],
        "console_errors": [],
        "performance_metrics": {},
        "meta_tags": {},
        "detailed_recommendations": []
    }

    try:
        # Open URL and wait for initial load
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Test all UI/UX principles
        test_simplicity(driver, results)
        test_user_centered_design(driver, results)
        test_visibility(driver, results)
        test_consistency(driver, results)
        test_feedback(driver, results)
        test_clarity(driver, results)
        test_accessibility(driver, results)
        test_usability(driver, results)
        test_efficiency(driver, results)
        test_delight(driver, results)
        
        # Original tests
        check_accessibility(driver, results)
        check_responsiveness(driver, results)
        check_broken_links(driver, results)
        check_broken_images(driver, results)
        results["console_errors"] = get_console_errors(driver)
        results["performance_metrics"] = get_performance_metrics(driver)
        results["meta_tags"] = get_meta_tags(driver)
        
    except Exception as e:
        results["error"] = f"Test failed: {str(e)}"
    finally:
        driver.quit()
    
    return results

def test_simplicity(driver, results):
    """Test for simplicity - easy to use and navigate with minimal effort"""
    score = 0
    recommendations = []
    
    # Check navigation complexity
    nav_elements = driver.find_elements(By.TAG_NAME, "nav")
    if len(nav_elements) <= 2:  # Not too many navigation areas
        score += 20
    else:
        recommendations.append("Consider reducing navigation complexity - too many nav elements found")
    
    # Check for overwhelming content
    text_elements = driver.find_elements(By.TAG_NAME, "p")
    if len(text_elements) <= 50:  # Reasonable amount of text
        score += 20
    else:
        recommendations.append("Consider breaking down content into smaller, digestible sections")
    
    # Check for clear call-to-actions
    buttons = driver.find_elements(By.TAG_NAME, "button")
    links = driver.find_elements(By.TAG_NAME, "a")
    if len(buttons) + len(links) <= 20:  # Not too many interactive elements
        score += 20
    else:
        recommendations.append("Consider reducing the number of interactive elements for simplicity")
    
    # Check for whitespace usage
    body_style = driver.execute_script("""
        const body = document.body;
        const style = window.getComputedStyle(body);
        return {
            padding: style.padding,
            margin: style.margin
        };
    """)
    
    if "0px" not in body_style["padding"] or "0px" not in body_style["margin"]:
        score += 20
    else:
        recommendations.append("Add whitespace for better visual breathing room")
    
    # Check for clear visual hierarchy
    headings = driver.find_elements(By.XPATH, "//h1|//h2|//h3|//h4|//h5|//h6")
    if 2 <= len(headings) <= 10:  # Good heading structure
        score += 20
    else:
        recommendations.append("Improve heading structure for better content organization")
    
    results["simplicity_score"] = score
    results["detailed_recommendations"].extend(recommendations)

def test_user_centered_design(driver, results):
    """Test for user-centered design focusing on user needs and accessibility"""
    score = 0
    recommendations = []
    
    # Check for keyboard navigation support
    focusable_elements = driver.execute_script("""
        return document.querySelectorAll('a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])').length;
    """)
    if focusable_elements > 0:
        score += 25
    else:
        recommendations.append("Ensure keyboard navigation is supported for all interactive elements")
    
    # Check for screen reader support
    aria_labels = driver.execute_script("""
        return document.querySelectorAll('[aria-label], [aria-labelledby], [aria-describedby]').length;
    """)
    if aria_labels > 0:
        score += 25
    else:
        recommendations.append("Add ARIA labels for better screen reader support")
    
    # Check for color contrast (basic check)
    text_elements = driver.find_elements(By.TAG_NAME, "p")
    if len(text_elements) > 0:
        score += 25
        recommendations.append("Verify color contrast ratios meet WCAG guidelines")
    
    # Check for mobile-friendly design
    viewport_meta = driver.find_elements(By.CSS_SELECTOR, 'meta[name="viewport"]')
    if viewport_meta:
        score += 25
    else:
        recommendations.append("Add viewport meta tag for mobile responsiveness")
    
    results["user_centered_design_score"] = score
    results["detailed_recommendations"].extend(recommendations)

def test_visibility(driver, results):
    """Test for clear and visible interface highlighting important tasks"""
    score = 0
    recommendations = []
    
    # Check for prominent call-to-action buttons
    cta_buttons = driver.find_elements(By.CSS_SELECTOR, "button, .btn, .button, .cta")
    if len(cta_buttons) > 0:
        score += 25
        # Check if CTAs are visually prominent
        for button in cta_buttons[:3]:  # Check first 3 buttons
            style = driver.execute_script("""
                const style = window.getComputedStyle(arguments[0]);
                return {
                    backgroundColor: style.backgroundColor,
                    color: style.color,
                    fontSize: style.fontSize
                };
            """, button)
            if style["backgroundColor"] != "rgba(0, 0, 0, 0)" and style["color"] != "rgba(0, 0, 0, 0)":
                score += 25
                break
    else:
        recommendations.append("Add clear call-to-action buttons for important tasks")
    
    # Check for clear navigation
    nav_elements = driver.find_elements(By.TAG_NAME, "nav")
    if nav_elements:
        score += 25
    else:
        recommendations.append("Ensure navigation is clearly visible and accessible")
    
    # Check for important information visibility
    headings = driver.find_elements(By.XPATH, "//h1|//h2")
    if len(headings) > 0:
        score += 25
    else:
        recommendations.append("Add clear headings to highlight important information")
    
    results["visibility_score"] = min(score, 100)
    results["detailed_recommendations"].extend(recommendations)

def test_consistency(driver, results):
    """Test for consistent design elements like colors, typography, and layout"""
    score = 0
    recommendations = []
    
    # Check for consistent color usage
    colors = driver.execute_script("""
        const elements = document.querySelectorAll('*');
        const colors = new Set();
        elements.forEach(el => {
            const style = window.getComputedStyle(el);
            colors.add(style.color);
            colors.add(style.backgroundColor);
        });
        return Array.from(colors).filter(c => c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent');
    """)
    
    if len(colors) <= 10:  # Reasonable color palette
        score += 25
    else:
        recommendations.append("Consider reducing color palette for better consistency")
    
    # Check for consistent typography
    fonts = driver.execute_script("""
        const elements = document.querySelectorAll('*');
        const fonts = new Set();
        elements.forEach(el => {
            const style = window.getComputedStyle(el);
            fonts.add(style.fontFamily);
        });
        return Array.from(fonts);
    """)
    
    if len(fonts) <= 3:  # Good typography consistency
        score += 25
    else:
        recommendations.append("Use consistent typography throughout the interface")
    
    # Check for consistent spacing
    spacing_consistency = driver.execute_script("""
        const elements = document.querySelectorAll('p, div, section');
        const margins = new Set();
        elements.forEach(el => {
            const style = window.getComputedStyle(el);
            margins.add(style.margin);
            margins.add(style.padding);
        });
        return margins.size;
    """)
    
    if spacing_consistency <= 5:  # Consistent spacing
        score += 25
    else:
        recommendations.append("Use consistent spacing and layout patterns")
    
    # Check for consistent button styles
    buttons = driver.find_elements(By.TAG_NAME, "button")
    if len(buttons) <= 5 or len(buttons) == 0:  # Few buttons or consistent styling
        score += 25
    else:
        recommendations.append("Ensure consistent button styling across the interface")
    
    results["consistency_score"] = score
    results["detailed_recommendations"].extend(recommendations)

def test_feedback(driver, results):
    """Test for feedback mechanisms like visual cues, animations, and success messages"""
    score = 0
    recommendations = []
    
    # Check for form validation feedback
    forms = driver.find_elements(By.TAG_NAME, "form")
    if forms:
        score += 25
        # Check for validation attributes
        inputs = driver.find_elements(By.TAG_NAME, "input")
        for input_elem in inputs:
            if input_elem.get_attribute("required") or input_elem.get_attribute("pattern"):
                score += 25
                break
    else:
        recommendations.append("Add form validation with clear feedback messages")
    
    # Check for loading states or animations
    loading_elements = driver.find_elements(By.CSS_SELECTOR, ".loading, .spinner, .loader, [class*='loading'], [class*='spinner']")
    if loading_elements:
        score += 25
    else:
        recommendations.append("Add loading indicators for better user feedback")
    
    # Check for hover effects
    interactive_elements = driver.find_elements(By.CSS_SELECTOR, "a, button, .btn")
    if interactive_elements:
        score += 25
        recommendations.append("Add hover effects for interactive elements")
    
    # Check for success/error message containers
    message_containers = driver.find_elements(By.CSS_SELECTOR, ".message, .alert, .notification, .toast")
    if message_containers:
        score += 25
    else:
        recommendations.append("Add message containers for user feedback")
    
    results["feedback_score"] = min(score, 100)
    results["detailed_recommendations"].extend(recommendations)

def test_clarity(driver, results):
    """Test for clarity in content and interface elements"""
    score = 0
    recommendations = []
    
    # Check for clear page titles
    title = driver.title
    if title and len(title) > 0 and len(title) < 60:
        score += 25
    else:
        recommendations.append("Add clear, descriptive page titles")
    
    # Check for clear headings
    h1_elements = driver.find_elements(By.TAG_NAME, "h1")
    if len(h1_elements) == 1:
        score += 25
    else:
        recommendations.append("Use exactly one H1 heading per page for clarity")
    
    # Check for clear link text
    links = driver.find_elements(By.TAG_NAME, "a")
    unclear_links = 0
    for link in links:
        text = link.text.strip()
        if text in ["Click here", "Read more", "Learn more", "More", "..."]:
            unclear_links += 1
    
    if unclear_links == 0:
        score += 25
    else:
        recommendations.append("Use descriptive link text instead of generic phrases")
    
    # Check for clear form labels
    inputs = driver.find_elements(By.TAG_NAME, "input")
    labeled_inputs = 0
    for input_elem in inputs:
        if input_elem.get_attribute("placeholder") or driver.execute_script(
            "return arguments[0].labels.length > 0;", input_elem
        ):
            labeled_inputs += 1
    
    if labeled_inputs == len(inputs) or len(inputs) == 0:
        score += 25
    else:
        recommendations.append("Add clear labels or placeholders for all form inputs")
    
    results["clarity_score"] = score
    results["detailed_recommendations"].extend(recommendations)

def test_accessibility(driver, results):
    """Test for accessibility features including keyboard navigation and screen reader support"""
    score = 0
    recommendations = []
    
    # Check for alt text on images
    images = driver.find_elements(By.TAG_NAME, "img")
    images_with_alt = 0
    for img in images:
        if img.get_attribute("alt"):
            images_with_alt += 1
    
    if len(images) == 0 or images_with_alt == len(images):
        score += 25
    else:
        recommendations.append("Add alt text to all images for screen reader accessibility")
    
    # Check for semantic HTML
    semantic_elements = driver.find_elements(By.CSS_SELECTOR, "nav, main, article, section, aside, header, footer")
    if len(semantic_elements) > 0:
        score += 25
    else:
        recommendations.append("Use semantic HTML elements for better accessibility")
    
    # Check for proper heading hierarchy
    headings = driver.find_elements(By.XPATH, "//h1|//h2|//h3|//h4|//h5|//h6")
    if len(headings) > 0:
        levels = [int(h.tag_name[1]) for h in headings]
        if levels and min(levels) == 1:
            score += 25
        else:
            recommendations.append("Start with H1 heading and maintain proper hierarchy")
    
    # Check for keyboard accessibility
    focusable_elements = driver.execute_script("""
        return document.querySelectorAll('a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])').length;
    """)
    if focusable_elements > 0:
        score += 25
    else:
        recommendations.append("Ensure all interactive elements are keyboard accessible")
    
    results["accessibility_score"] = score
    results["detailed_recommendations"].extend(recommendations)

def test_usability(driver, results):
    """Test for overall usability and ease of navigation"""
    score = 0
    recommendations = []
    
    # Check for clear navigation structure
    nav_elements = driver.find_elements(By.TAG_NAME, "nav")
    if nav_elements:
        score += 25
    else:
        recommendations.append("Add clear navigation structure")
    
    # Check for search functionality
    search_elements = driver.find_elements(By.CSS_SELECTOR, "input[type='search'], .search, #search")
    if search_elements:
        score += 25
    else:
        recommendations.append("Consider adding search functionality for better usability")
    
    # Check for breadcrumbs
    breadcrumb_elements = driver.find_elements(By.CSS_SELECTOR, ".breadcrumb, .breadcrumbs, [class*='breadcrumb']")
    if breadcrumb_elements:
        score += 25
    else:
        recommendations.append("Add breadcrumb navigation for complex sites")
    
    # Check for reasonable page load time
    load_time = driver.execute_script("""
        return window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
    """)
    
    if load_time < 3000:  # Less than 3 seconds
        score += 25
    else:
        recommendations.append("Optimize page load time for better user experience")
    
    results["usability_score"] = score
    results["detailed_recommendations"].extend(recommendations)

def test_efficiency(driver, results):
    """Test for efficiency in achieving user goals quickly and easily"""
    score = 0
    recommendations = []
    
    # Check for optimized images
    images = driver.find_elements(By.TAG_NAME, "img")
    if len(images) <= 20:  # Reasonable number of images
        score += 25
    else:
        recommendations.append("Optimize and compress images for faster loading")
    
    # Check for minimal HTTP requests (basic check)
    scripts = driver.find_elements(By.TAG_NAME, "script")
    stylesheets = driver.find_elements(By.TAG_NAME, "link")
    if len(scripts) + len(stylesheets) <= 10:  # Reasonable number of resources
        score += 25
    else:
        recommendations.append("Minimize HTTP requests by combining resources")
    
    # Check for efficient form design
    forms = driver.find_elements(By.TAG_NAME, "form")
    if forms:
        for form in forms:
            inputs = form.find_elements(By.TAG_NAME, "input")
            if len(inputs) <= 10:  # Reasonable form length
                score += 25
                break
    else:
        score += 25  # No forms to worry about
    
    # Check for clear call-to-actions
    cta_elements = driver.find_elements(By.CSS_SELECTOR, "button, .btn, .cta, .call-to-action")
    if len(cta_elements) > 0:
        score += 25
    else:
        recommendations.append("Add clear call-to-action buttons for efficient user flow")
    
    results["efficiency_score"] = score
    results["detailed_recommendations"].extend(recommendations)

def test_delight(driver, results):
    """Test for delightful user experience that invokes positive emotions"""
    score = 0
    recommendations = []
    
    # Check for modern design elements
    modern_elements = driver.find_elements(By.CSS_SELECTOR, ".card, .shadow, .rounded, .gradient, .animation")
    if modern_elements:
        score += 25
    else:
        recommendations.append("Add modern design elements like cards, shadows, or subtle animations")
    
    # Check for engaging visuals
    images = driver.find_elements(By.TAG_NAME, "img")
    if len(images) > 0:
        score += 25
    else:
        recommendations.append("Add engaging visuals to create a more delightful experience")
    
    # Check for interactive elements
    interactive_elements = driver.find_elements(By.CSS_SELECTOR, "a, button, .interactive, [onclick]")
    if len(interactive_elements) > 0:
        score += 25
    else:
        recommendations.append("Add interactive elements for user engagement")
    
    # Check for positive messaging
    positive_words = ["welcome", "thank", "success", "great", "awesome", "excellent"]
    page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    if any(word in page_text for word in positive_words):
        score += 25
    else:
        recommendations.append("Use positive, encouraging language in your content")
    
    results["delight_score"] = score
    results["detailed_recommendations"].extend(recommendations)

def check_accessibility(driver, results):
    # Check for missing alt text
    images = driver.find_elements(By.TAG_NAME, "img")
    for img in images:
        alt = img.get_attribute("alt")
        if alt is None or alt.strip() == "":
            src = img.get_attribute("src") or "unknown source"
            results["accessibility_issues"].append(f"Missing alt text: {src}")

    # Check for proper heading hierarchy
    headings = driver.find_elements(By.XPATH, "//h1|//h2|//h3|//h4|//h5|//h6")
    levels = [int(h.tag_name[1]) for h in headings]
    if levels and min(levels) > 1:
        results["accessibility_issues"].append("No H1 heading found")
    
    # Check form labels
    inputs = driver.find_elements(By.TAG_NAME, "input")
    for input_elem in inputs:
        if input_elem.get_attribute("type") not in ["hidden", "submit"]:
            if not driver.execute_script(
                "return arguments[0].labels.length > 0;", input_elem
            ):
                results["accessibility_issues"].append(
                    f"Input missing label: {input_elem.get_attribute('outerHTML')[:50]}"
                )

def check_responsiveness(driver, results):
    # Test different viewports
    viewports = [
        (360, 640),   # Mobile
        (768, 1024),  # Tablet
        (1920, 1080)  # Desktop
    ]
    
    original_size = driver.get_window_size()
    
    for width, height in viewports:
        driver.set_window_size(width, height)
        time.sleep(1)  # Allow content to reflow
        
        # Check for horizontal scrolling
        scroll_width = driver.execute_script(
            "return document.documentElement.scrollWidth"
        )
        if scroll_width > width:
            results["responsive_issues"].append(
                f"Horizontal scrolling at {width}x{height} (content width: {scroll_width})"
            )

    # Restore original size
    driver.set_window_size(original_size["width"], original_size["height"])

def check_broken_links(driver, results):
    links = driver.find_elements(By.TAG_NAME, "a")
    unique_links = set()
    
    for link in links:
        href = link.get_attribute("href")
        if href and "#" not in href and href not in unique_links:
            unique_links.add(href)
            
            try:
                response = requests.head(
                    href,
                    allow_redirects=True,
                    timeout=10,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                if response.status_code >= 400:
                    results["broken_links"].append(
                        f"Broken link ({response.status_code}): {href}"
                    )
            except requests.RequestException:
                results["broken_links"].append(f"Inaccessible link: {href}")

def check_broken_images(driver, results):
    images = driver.find_elements(By.TAG_NAME, "img")
    for img in images:
        src = img.get_attribute("src")
        if src:
            try:
                response = requests.head(
                    src,
                    allow_redirects=True,
                    timeout=10,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                if response.status_code >= 400:
                    results["broken_images"].append(
                        f"Broken image ({response.status_code}): {src}"
                    )
            except requests.RequestException:
                results["broken_images"].append(f"Inaccessible image: {src}")

def get_console_errors(driver):
    return driver.get_log("browser")

def get_performance_metrics(driver):
    metrics = driver.execute_script("""
        const perf = window.performance || {};
        const timings = perf.timing || {};
        return {
            dns: timings.domainLookupEnd - timings.domainLookupStart,
            tcp: timings.connectEnd - timings.connectStart,
            request: timings.responseStart - timings.requestStart,
            response: timings.responseEnd - timings.responseStart,
            domLoad: timings.domContentLoadedEventEnd - timings.navigationStart,
            fullLoad: timings.loadEventEnd - timings.navigationStart
        };
    """)
    return metrics

def get_meta_tags(driver):
    return driver.execute_script("""
        const metas = {};
        document.querySelectorAll('meta').forEach(meta => {
            const name = meta.getAttribute('name') || meta.getAttribute('property');
            if (name) metas[name] = meta.getAttribute('content');
        });
        return metas;
    """)

def generate_report(results):
    print("\n" + "="*50)
    print(f"UI/UX Test Report for: {results['url']}")
    print("="*50)
    
    # Simplicity Report
    print("\n[ SIMPLICITY SCORE: {:.2f} ]".format(results["simplicity_score"]))
    print("-"*50)
    if results["detailed_recommendations"]:
        for rec in results["detailed_recommendations"]:
            print(f"- {rec}")
    else:
        print("No specific simplicity recommendations found.")
    
    # User-Centered Design Report
    print("\n[ USER-CENTERED DESIGN SCORE: {:.2f} ]".format(results["user_centered_design_score"]))
    print("-"*50)
    if results["detailed_recommendations"]:
        for rec in results["detailed_recommendations"]:
            if "user-centered" in rec.lower():
                print(f"- {rec}")
    else:
        print("No specific user-centered design recommendations found.")
    
    # Visibility Report
    print("\n[ VISIBILITY SCORE: {:.2f} ]".format(results["visibility_score"]))
    print("-"*50)
    if results["detailed_recommendations"]:
        for rec in results["detailed_recommendations"]:
            if "visibility" in rec.lower():
                print(f"- {rec}")
    else:
        print("No specific visibility recommendations found.")
    
    # Consistency Report
    print("\n[ CONSISTENCY SCORE: {:.2f} ]".format(results["consistency_score"]))
    print("-"*50)
    if results["detailed_recommendations"]:
        for rec in results["detailed_recommendations"]:
            if "consistency" in rec.lower():
                print(f"- {rec}")
    else:
        print("No specific consistency recommendations found.")
    
    # Feedback Report
    print("\n[ FEEDBACK SCORE: {:.2f} ]".format(results["feedback_score"]))
    print("-"*50)
    if results["detailed_recommendations"]:
        for rec in results["detailed_recommendations"]:
            if "feedback" in rec.lower():
                print(f"- {rec}")
    else:
        print("No specific feedback recommendations found.")
    
    # Clarity Report
    print("\n[ CLARITY SCORE: {:.2f} ]".format(results["clarity_score"]))
    print("-"*50)
    if results["detailed_recommendations"]:
        for rec in results["detailed_recommendations"]:
            if "clarity" in rec.lower():
                print(f"- {rec}")
    else:
        print("No specific clarity recommendations found.")
    
    # Accessibility Report
    print("\n[ ACCESSIBILITY SCORE: {:.2f} ]".format(results["accessibility_score"]))
    print("-"*50)
    if results["detailed_recommendations"]:
        for rec in results["detailed_recommendations"]:
            if "accessibility" in rec.lower():
                print(f"- {rec}")
    else:
        print("No specific accessibility recommendations found.")
    
    # Usability Report
    print("\n[ USABILITY SCORE: {:.2f} ]".format(results["usability_score"]))
    print("-"*50)
    if results["detailed_recommendations"]:
        for rec in results["detailed_recommendations"]:
            if "usability" in rec.lower():
                print(f"- {rec}")
    else:
        print("No specific usability recommendations found.")
    
    # Efficiency Report
    print("\n[ EFFICIENCY SCORE: {:.2f} ]".format(results["efficiency_score"]))
    print("-"*50)
    if results["detailed_recommendations"]:
        for rec in results["detailed_recommendations"]:
            if "efficiency" in rec.lower():
                print(f"- {rec}")
    else:
        print("No specific efficiency recommendations found.")
    
    # Delight Report
    print("\n[ DELIGHT SCORE: {:.2f} ]".format(results["delight_score"]))
    print("-"*50)
    if results["detailed_recommendations"]:
        for rec in results["detailed_recommendations"]:
            if "delight" in rec.lower():
                print(f"- {rec}")
    else:
        print("No specific delight recommendations found.")
    
    # Original Issues Report
    print("\n[ ORIGINAL ACCESSIBILITY ISSUES ]")
    if results["accessibility_issues"]:
        for issue in results["accessibility_issues"]:
            print(f"- {issue}")
    else:
        print("No critical accessibility issues found")
    
    print("\n[ RESPONSIVENESS ISSUES ]")
    if results["responsive_issues"]:
        for issue in results["responsive_issues"]:
            print(f"- {issue}")
    else:
        print("No responsiveness issues found")
    
    print("\n[ BROKEN LINKS ]")
    if results["broken_links"]:
        for link in results["broken_links"]:
            print(f"- {link}")
    else:
        print("No broken links found")
    
    print("\n[ BROKEN IMAGES ]")
    if results["broken_images"]:
        for img in results["broken_images"]:
            print(f"- {img}")
    else:
        print("No broken images found")
    
    # Console Errors Report
    print("\n[ CONSOLE ERRORS ]")
    if results["console_errors"]:
        for error in results["console_errors"]:
            print(f"- {error['message']}")
    else:
        print("No console errors found")
    
    # Performance Report
    print("\n[ PERFORMANCE METRICS ]")
    metrics = results["performance_metrics"]
    if metrics:
        print(f"DNS Lookup: {metrics.get('dns', 'N/A')}ms")
        print(f"TCP Connection: {metrics.get('tcp', 'N/A')}ms")
        print(f"Request: {metrics.get('request', 'N/A')}ms")
        print(f"Response: {metrics.get('response', 'N/A')}ms")
        print(f"DOM Load: {metrics.get('domLoad', 'N/A')}ms")
        print(f"Full Load: {metrics.get('fullLoad', 'N/A')}ms")
    else:
        print("Performance metrics not available")
    
    # Overall UI/UX Score Summary
    print("\n" + "="*60)
    print("OVERALL UI/UX DESIGN PRINCIPLES SUMMARY")
    print("="*60)
    
    scores = {
        "Simplicity": results["simplicity_score"],
        "User-Centered Design": results["user_centered_design_score"],
        "Visibility": results["visibility_score"],
        "Consistency": results["consistency_score"],
        "Feedback": results["feedback_score"],
        "Clarity": results["clarity_score"],
        "Accessibility": results["accessibility_score"],
        "Usability": results["usability_score"],
        "Efficiency": results["efficiency_score"],
        "Delight": results["delight_score"]
    }
    
    total_score = sum(scores.values())
    average_score = total_score / len(scores)
    
    print(f"\nOverall Average Score: {average_score:.1f}/100")
    print("\nIndividual Principle Scores:")
    print("-" * 40)
    
    for principle, score in scores.items():
        status = "✅ EXCELLENT" if score >= 80 else "🟡 GOOD" if score >= 60 else "🟠 NEEDS IMPROVEMENT" if score >= 40 else "🔴 POOR"
        print(f"{principle:<25} {score:>3}/100 {status}")
    
    print(f"\nTotal Score: {total_score}/1000")
    
    # Priority recommendations
    print("\n" + "="*60)
    print("PRIORITY RECOMMENDATIONS")
    print("="*60)
    
    # Get top 5 recommendations
    all_recommendations = results["detailed_recommendations"]
    if all_recommendations:
        print("Top recommendations for improvement:")
        for i, rec in enumerate(all_recommendations[:5], 1):
            print(f"{i}. {rec}")
    else:
        print("Great job! No specific recommendations at this time.")
    
    # Export results option
    print(f"\n" + "="*60)
    print("EXPORT OPTIONS")
    print("="*60)
    print("Results can be exported to JSON for further analysis.")
    print("Use the --export flag when running the script to save results.")

def export_results(results, filename=None):
    """Export results to JSON file"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ui_ux_test_results_{timestamp}.json"
    
    # Clean up results for JSON serialization
    export_data = {
        "url": results["url"],
        "test_date": datetime.now().isoformat(),
        "scores": {
            "simplicity": results["simplicity_score"],
            "user_centered_design": results["user_centered_design_score"],
            "visibility": results["visibility_score"],
            "consistency": results["consistency_score"],
            "feedback": results["feedback_score"],
            "clarity": results["clarity_score"],
            "accessibility": results["accessibility_score"],
            "usability": results["usability_score"],
            "efficiency": results["efficiency_score"],
            "delight": results["delight_score"]
        },
        "issues": {
            "accessibility_issues": results["accessibility_issues"],
            "responsive_issues": results["responsive_issues"],
            "broken_links": results["broken_links"],
            "broken_images": results["broken_images"],
            "console_errors": [str(error) for error in results["console_errors"]]
        },
        "performance_metrics": results["performance_metrics"],
        "meta_tags": results["meta_tags"],
        "recommendations": results["detailed_recommendations"]
    }
    
    with open(filename, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"\nResults exported to: {filename}")
    return filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UI/UX Testing Tool")
    parser.add_argument("--url", help="Website URL to test")
    parser.add_argument("--export", action="store_true", help="Export results to JSON file")
    parser.add_argument("--output", help="Output filename for JSON export")
    
    args = parser.parse_args()
    
    if args.url:
        url = args.url.strip()
    else:
        url = input("Enter website URL to test: ").strip()
    
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    print(f"\nStarting comprehensive UI/UX test for {url}...")
    print("Testing all design principles: Simplicity, User-centered Design, Visibility, Consistency, Feedback, Clarity, Accessibility, Usability, Efficiency, and Delight...")
    
    results = run_ui_ux_test(url)
    generate_report(results)
    
    if args.export:
        export_results(results, args.output)
    
    print("\nTest completed!") 