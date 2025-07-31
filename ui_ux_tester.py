import time
import requests
import json
import argparse
import os
import base64
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
    chrome_options.add_argument("--enable-javascript")
    chrome_options.add_argument("--disable-web-security")  # Allow cross-origin requests for better error detection
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
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
        "detailed_recommendations": [],
        "screenshots": []
    }

    try:
        # Open URL and wait for initial load
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Set up JavaScript error listener to capture console errors
        driver.execute_script("""
            // Initialize error capture array
            window.capturedErrors = [];
            
            // Override console.error to capture errors
            const originalConsoleError = console.error;
            console.error = function(...args) {
                const errorInfo = {
                    message: args.join(' '),
                    timestamp: new Date().toISOString(),
                    url: window.location.href,
                    source: 'console.error'
                };
                window.capturedErrors.push(errorInfo);
                originalConsoleError.apply(console, args);
            };
            
            // Override console.warn to capture warnings
            const originalConsoleWarn = console.warn;
            console.warn = function(...args) {
                const errorInfo = {
                    message: args.join(' '),
                    timestamp: new Date().toISOString(),
                    url: window.location.href,
                    source: 'console.warn'
                };
                window.capturedErrors.push(errorInfo);
                originalConsoleWarn.apply(console, args);
            };
            
            // Add global error handler
            window.addEventListener('error', function(event) {
                const errorInfo = {
                    message: event.message || 'Unknown error',
                    filename: event.filename || 'Unknown file',
                    line: event.lineno || 'Unknown',
                    column: event.colno || 'Unknown',
                    stack: event.error ? event.error.stack : 'No stack trace available',
                    timestamp: new Date().toISOString(),
                    url: window.location.href,
                    source: 'window.error'
                };
                window.capturedErrors.push(errorInfo);
            });
            
            // Add unhandled promise rejection handler
            window.addEventListener('unhandledrejection', function(event) {
                const errorInfo = {
                    message: event.reason ? event.reason.toString() : 'Unhandled promise rejection',
                    timestamp: new Date().toISOString(),
                    url: window.location.href,
                    source: 'unhandledrejection'
                };
                window.capturedErrors.push(errorInfo);
            });
            
            // Also capture any existing errors that might have occurred during page load
            if (window.performance && window.performance.getEntriesByType) {
                const navigationEntries = window.performance.getEntriesByType('navigation');
                if (navigationEntries.length > 0) {
                    const navEntry = navigationEntries[0];
                    if (navEntry.loadEventEnd > 0) {
                        // Page has loaded, check for any existing console errors
                        console.error('Page load completed - checking for existing errors');
                    }
                }
            }
        """)
        
        # Wait a bit for any page load errors to occur
        time.sleep(2)
        
        # Trigger some common JavaScript errors to test error capture
        driver.execute_script("""
            // Test error capture by triggering some common errors
            try {
                // Test console.error capture
                console.error('Test console error capture from UI/UX tester');
                console.warn('Test console warning capture from UI/UX tester');
                
                // Test undefined variable error
                console.log(undefinedVariable);
            } catch (e) {
                // This error should be captured by our error listener
                console.error('Test error caught:', e.message);
            }
            
            // Test promise rejection
            Promise.reject(new Error('Test promise rejection from UI/UX tester'));
            
            // Test async error
            setTimeout(() => {
                throw new Error('Test async error from UI/UX tester');
            }, 100);
        """)
        
        # Wait a bit more for async errors to be captured
        time.sleep(1)
        
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
        print("DEBUG: Starting original tests...")
        check_accessibility(driver, results)
        check_responsiveness(driver, results)
        check_broken_links(driver, results)
        check_broken_images(driver, results)
        print("DEBUG: About to call get_console_errors...")
        results["console_errors"] = get_console_errors(driver)
        print("DEBUG: get_console_errors completed")
        results["performance_metrics"] = get_performance_metrics(driver)
        results["meta_tags"] = get_meta_tags(driver)
        
    except Exception as e:
        print(f"DEBUG: Exception caught: {str(e)}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
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
            # Get element position and line info
            line_info = driver.execute_script("""
                const element = arguments[0];
                const rect = element.getBoundingClientRect();
                const tagName = element.tagName.toLowerCase();
                const className = element.className || '';
                const id = element.id || '';
                return {
                    tag: tagName,
                    class: className,
                    id: id,
                    position: {x: Math.round(rect.x), y: Math.round(rect.y)},
                    size: {width: Math.round(rect.width), height: Math.round(rect.height)}
                };
            """, img)
            
            # Capture screenshot of the image
            screenshot = capture_element_screenshot(driver, img, "missing_alt", "accessibility")
            if screenshot:
                results["screenshots"].append(screenshot)
            
            results["accessibility_issues"].append(
                f"Missing alt text: {src} | Element: {line_info['tag']}{'#' + line_info['id'] if line_info['id'] else ''}{'.' + line_info['class'] if line_info['class'] else ''} | Position: ({line_info['position']['x']}, {line_info['position']['y']})"
            )

    # Check for proper heading hierarchy
    headings = driver.find_elements(By.XPATH, "//h1|//h2|//h3|//h4|//h5|//h6")
    levels = [int(h.tag_name[1]) for h in headings]
    if levels and min(levels) > 1:
        # Get first heading info
        first_heading = headings[0]
        heading_info = driver.execute_script("""
            const element = arguments[0];
            const rect = element.getBoundingClientRect();
            return {
                tag: element.tagName.toLowerCase(),
                text: element.textContent.substring(0, 50) + '...' if element.textContent.length > 50 else element.textContent,
                position: {x: Math.round(rect.x), y: Math.round(rect.y)}
            };
        """, first_heading)
        
        # Capture screenshot of the heading area
        screenshot = capture_element_screenshot(driver, first_heading, "no_h1_heading", "accessibility")
        if screenshot:
            results["screenshots"].append(screenshot)
        
        results["accessibility_issues"].append(
            f"No H1 heading found | First heading: {heading_info['tag']} '{heading_info['text']}' | Position: ({heading_info['position']['x']}, {heading_info['position']['y']})"
        )
    
    # Check form labels
    inputs = driver.find_elements(By.TAG_NAME, "input")
    for input_elem in inputs:
        if input_elem.get_attribute("type") not in ["hidden", "submit"]:
            if not driver.execute_script(
                "return arguments[0].labels.length > 0;", input_elem
            ):
                input_info = driver.execute_script("""
                    const element = arguments[0];
                    const rect = element.getBoundingClientRect();
                    return {
                        type: element.type,
                        name: element.name || '',
                        placeholder: element.placeholder || '',
                        position: {x: Math.round(rect.x), y: Math.round(rect.y)}
                    };
                """, input_elem)
                
                # Capture screenshot of the input field
                screenshot = capture_element_screenshot(driver, input_elem, "missing_label", "accessibility")
                if screenshot:
                    results["screenshots"].append(screenshot)
                
                results["accessibility_issues"].append(
                    f"Input missing label | Type: {input_info['type']} | Name: {input_info['name']} | Placeholder: {input_info['placeholder']} | Position: ({input_info['position']['x']}, {input_info['position']['y']})"
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
            # Find elements causing overflow
            overflow_elements = driver.execute_script("""
                const viewportWidth = arguments[0];
                const elements = document.querySelectorAll('*');
                const overflowElements = [];
                
                elements.forEach(el => {
                    const rect = el.getBoundingClientRect();
                    if (rect.width > viewportWidth || rect.right > viewportWidth) {
                        overflowElements.push({
                            tag: el.tagName.toLowerCase(),
                            class: el.className || '',
                            id: el.id || '',
                            width: Math.round(rect.width),
                            right: Math.round(rect.right),
                            text: el.textContent.length > 30 ? el.textContent.substring(0, 30) + '...' : el.textContent
                        });
                    }
                });
                
                return overflowElements.slice(0, 5); // Return top 5 overflow elements
            """, width)
            
            overflow_info = ""
            if overflow_elements:
                overflow_info = " | Overflow elements: " + ", ".join([
                    f"{elem['tag']}{'#' + elem['id'] if elem['id'] else ''}{'.' + elem['class'] if elem['class'] else ''} (width: {elem['width']}px)"
                    for elem in overflow_elements[:3]
                ])
                
                # Capture screenshot of the overflow area
                if overflow_elements:
                    first_overflow = overflow_elements[0]
                    screenshot = capture_area_screenshot(
                        driver, 
                        first_overflow.get('x', 0), 
                        first_overflow.get('y', 0), 
                        first_overflow.get('width', 100), 
                        first_overflow.get('height', 100), 
                        f"overflow_{width}x{height}", 
                        "responsiveness"
                    )
                    if screenshot:
                        results["screenshots"].append(screenshot)
            
            results["responsive_issues"].append(
                f"Horizontal scrolling at {width}x{height} (content width: {scroll_width}){overflow_info}"
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
            
            # Get link element info
            link_info = driver.execute_script("""
                const element = arguments[0];
                const rect = element.getBoundingClientRect();
                return {
                    text: element.textContent.trim() || '[No text]',
                    class: element.className || '',
                    id: element.id || '',
                    position: {x: Math.round(rect.x), y: Math.round(rect.y)}
                };
            """, link)
            
            try:
                response = requests.head(
                    href,
                    allow_redirects=True,
                    timeout=10,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                if response.status_code >= 400:
                    # Capture screenshot of the broken link
                    screenshot = capture_element_screenshot(driver, link, "broken_link", "links")
                    if screenshot:
                        results["screenshots"].append(screenshot)
                    
                    results["broken_links"].append(
                        f"Broken link ({response.status_code}): {href} | Text: '{link_info['text']}' | Element: a{'#' + link_info['id'] if link_info['id'] else ''}{'.' + link_info['class'] if link_info['class'] else ''} | Position: ({link_info['position']['x']}, {link_info['position']['y']})"
                    )
            except requests.RequestException:
                # Capture screenshot of the inaccessible link
                screenshot = capture_element_screenshot(driver, link, "inaccessible_link", "links")
                if screenshot:
                    results["screenshots"].append(screenshot)
                
                results["broken_links"].append(
                    f"Inaccessible link: {href} | Text: '{link_info['text']}' | Element: a{'#' + link_info['id'] if link_info['id'] else ''}{'.' + link_info['class'] if link_info['class'] else ''} | Position: ({link_info['position']['x']}, {link_info['position']['y']})"
                )

def check_broken_images(driver, results):
    images = driver.find_elements(By.TAG_NAME, "img")
    for img in images:
        src = img.get_attribute("src")
        if src:
            # Get image element info
            img_info = driver.execute_script("""
                const element = arguments[0];
                const rect = element.getBoundingClientRect();
                return {
                    alt: element.alt || '[No alt text]',
                    class: element.className || '',
                    id: element.id || '',
                    position: {x: Math.round(rect.x), y: Math.round(rect.y)},
                    size: {width: Math.round(rect.width), height: Math.round(rect.height)}
                };
            """, img)
            
            try:
                response = requests.head(
                    src,
                    allow_redirects=True,
                    timeout=10,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                if response.status_code >= 400:
                    # Capture screenshot of the broken image
                    screenshot = capture_element_screenshot(driver, img, "broken_image", "images")
                    if screenshot:
                        results["screenshots"].append(screenshot)
                    
                    results["broken_images"].append(
                        f"Broken image ({response.status_code}): {src} | Alt: '{img_info['alt']}' | Element: img{'#' + img_info['id'] if img_info['id'] else ''}{'.' + img_info['class'] if img_info['class'] else ''} | Position: ({img_info['position']['x']}, {img_info['position']['y']}) | Size: {img_info['size']['width']}x{img_info['size']['height']}px"
                    )
            except requests.RequestException:
                # Capture screenshot of the inaccessible image
                screenshot = capture_element_screenshot(driver, img, "inaccessible_image", "images")
                if screenshot:
                    results["screenshots"].append(screenshot)
                
                results["broken_images"].append(
                    f"Inaccessible image: {src} | Alt: '{img_info['alt']}' | Element: img{'#' + img_info['id'] if img_info['id'] else ''}{'.' + img_info['class'] if img_info['class'] else ''} | Position: ({img_info['position']['x']}, {img_info['position']['y']}) | Size: {img_info['size']['width']}x{img_info['size']['height']}px"
                )

def get_console_errors(driver):
    """Capture both browser logs and JavaScript console errors with detailed information"""
    print("DEBUG: get_console_errors function called")
    errors = []
    
    # Get browser-level logs
    browser_logs = driver.get_log("browser")
    print(f"DEBUG: Found {len(browser_logs)} browser logs")
    for log in browser_logs:
        print(f"DEBUG: Browser log - Level: {log['level']}, Message: {log['message'][:100]}...")
        if log['level'] in ['SEVERE', 'ERROR']:
            error_details = driver.execute_script("""
                return {
                    url: window.location.href,
                    title: document.title,
                    userAgent: navigator.userAgent,
                    timestamp: new Date().toISOString()
                };
            """)
            
            detailed_error = {
                'message': log['message'],
                'level': log['level'],
                'timestamp': log['timestamp'],
                'url': error_details['url'],
                'page_title': error_details['title'],
                'user_agent': error_details['userAgent'],
                'source': 'browser'
            }
            errors.append(detailed_error)
    
    # Capture JavaScript console errors with line numbers and stack traces
    js_errors = driver.execute_script("""
        // Return any errors that were captured by our error listener
        console.log('DEBUG: Checking for captured errors, found:', window.capturedErrors ? window.capturedErrors.length : 0);
        return window.capturedErrors || [];
    """)
    
    print(f"DEBUG: Found {len(js_errors)} JavaScript errors")
    for js_error in js_errors:
        print(f"DEBUG: JS error - Source: {js_error.get('source')}, Message: {js_error.get('message', 'Unknown')[:100]}...")
        error_details = driver.execute_script("""
            return {
                url: window.location.href,
                title: document.title,
                userAgent: navigator.userAgent,
                timestamp: new Date().toISOString()
            };
        """)
        
        detailed_error = {
            'message': js_error.get('message', 'Unknown JavaScript error'),
            'level': 'ERROR',
            'timestamp': js_error.get('timestamp', error_details['timestamp']),
            'url': js_error.get('url', error_details['url']),
            'page_title': error_details['title'],
            'user_agent': error_details['userAgent'],
            'source': 'javascript',
            'line': js_error.get('line', 'Unknown'),
            'column': js_error.get('column', 'Unknown'),
            'stack': js_error.get('stack', 'No stack trace available'),
            'filename': js_error.get('filename', 'Unknown file')
        }
        errors.append(detailed_error)
    
    print(f"DEBUG: Total errors captured: {len(errors)}")
    return errors

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

def capture_element_screenshot(driver, element, issue_type, filename_prefix):
    """Capture screenshot of a specific element with highlighting"""
    try:
        # Highlight the element temporarily
        driver.execute_script("""
            const element = arguments[0];
            const originalStyle = element.style.outline;
            element.style.outline = '3px solid red';
            element.style.outlineOffset = '2px';
            element.style.backgroundColor = 'rgba(255, 0, 0, 0.1)';
            return originalStyle;
        """, element)
        
        time.sleep(0.5)  # Wait for highlight to be visible
        
        # Get element position and size
        rect = element.rect
        location = element.location
        
        # Capture full page screenshot
        screenshot = driver.get_screenshot_as_png()
        
        # Remove highlighting
        driver.execute_script("""
            const element = arguments[0];
            const originalStyle = arguments[1];
            element.style.outline = originalStyle;
            element.style.outlineOffset = '';
            element.style.backgroundColor = '';
        """, element, driver.execute_script("return arguments[0].style.outline;", element))
        
        # Convert to base64 for HTML embedding
        screenshot_b64 = base64.b64encode(screenshot).decode('utf-8')
        
        return {
            'base64': screenshot_b64,
            'filename': f"{filename_prefix}_{issue_type}_{int(time.time())}.png",
            'position': {'x': location['x'], 'y': location['y']},
            'size': {'width': rect['width'], 'height': rect['height']}
        }
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return None

def capture_area_screenshot(driver, x, y, width, height, issue_type, filename_prefix):
    """Capture screenshot of a specific area of the page"""
    try:
        # Scroll to the area
        driver.execute_script(f"window.scrollTo({x}, {y - 100});")
        time.sleep(0.5)
        
        # Capture full page screenshot
        screenshot = driver.get_screenshot_as_png()
        
        # Convert to base64 for HTML embedding
        screenshot_b64 = base64.b64encode(screenshot).decode('utf-8')
        
        return {
            'base64': screenshot_b64,
            'filename': f"{filename_prefix}_{issue_type}_{int(time.time())}.png",
            'position': {'x': x, 'y': y},
            'size': {'width': width, 'height': height}
        }
    except Exception as e:
        print(f"Error capturing area screenshot: {e}")
        return None

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
            print(f"- {error['level']}: {error['message']}")
            if error.get('source'):
                print(f"  Source: {error['source']}")
            if error.get('filename') and error.get('filename') != 'Unknown file':
                print(f"  File: {error['filename']}")
            if error.get('line') and error.get('line') != 'Unknown':
                print(f"  Line: {error['line']}, Column: {error.get('column', 'Unknown')}")
            if error.get('stack') and error.get('stack') != 'No stack trace available':
                print(f"  Stack: {error['stack'][:200]}...")
            print()
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

def generate_html_report(results, filename=None):
    """Generate an attractive HTML report"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ui_ux_test_report_{timestamp}.html"
    
    # Calculate overall score
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
    
    # Get status and color for each score
    def get_score_status(score):
        if score >= 80:
            return "EXCELLENT", "#10B981", "🟢"
        elif score >= 60:
            return "GOOD", "#F59E0B", "🟡"
        elif score >= 40:
            return "NEEDS IMPROVEMENT", "#F97316", "🟠"
        else:
            return "POOR", "#EF4444", "🔴"
    
    # Generate score cards HTML
    score_cards_html = ""
    for principle, score in scores.items():
        status, color, emoji = get_score_status(score)
        score_cards_html += f"""
        <div class="score-card">
            <div class="score-header">
                <h3>{principle}</h3>
                <span class="score-badge" style="background-color: {color}">{score}/100</span>
            </div>
            <div class="score-bar">
                <div class="score-fill" style="width: {score}%; background-color: {color}"></div>
            </div>
            <div class="score-status" style="color: {color}">{emoji} {status}</div>
        </div>
        """
    
    # Generate issues HTML with screenshots
    def generate_issues_html(issues, title, icon, issue_type):
        if not issues:
            return f"""
            <div class="issue-section">
                <h3>{icon} {title}</h3>
                <p class="no-issues">✅ No issues found</p>
            </div>
            """
        
        issues_html = f'<div class="issue-section"><h3>{icon} {title}</h3><ul class="issue-list">'
        for i, issue in enumerate(issues):
            # Format the issue with better styling for detailed information
            formatted_issue = issue.replace(' | ', '</span><br><span class="issue-detail">')
            issues_html += f'<li><span class="issue-main">{formatted_issue}</span>'
            
            # Add screenshot if available for this issue type
            screenshots_for_issue = [s for s in results["screenshots"] if issue_type in s['filename']]
            if screenshots_for_issue and i < len(screenshots_for_issue):
                screenshot = screenshots_for_issue[i]
                issues_html += f'''
                <div class="screenshot-container">
                    <img src="data:image/png;base64,{screenshot['base64']}" 
                         alt="Screenshot of {title.lower()}" 
                         class="issue-screenshot"
                         onclick="openScreenshotModal(this.src, '{screenshot['filename']}')">
                    <div class="screenshot-info">
                        <small>Click to enlarge | {screenshot['filename']}</small>
                    </div>
                </div>'''
            
            issues_html += '</li>'
        issues_html += '</ul></div>'
        return issues_html
    
    # Generate recommendations HTML
    recommendations_html = ""
    if results["detailed_recommendations"]:
        recommendations_html = '<div class="recommendations-section"><h3>💡 Priority Recommendations</h3><ol>'
        for i, rec in enumerate(results["detailed_recommendations"][:10], 1):
            recommendations_html += f'<li>{rec}</li>'
        recommendations_html += '</ol></div>'
    
    # Performance metrics HTML
    performance_html = ""
    if results["performance_metrics"]:
        metrics = results["performance_metrics"]
        performance_html = """
        <div class="performance-section">
            <h3>📊 Performance Metrics</h3>
            <div class="metrics-grid">
        """
        for key, value in metrics.items():
            if value is not None:
                performance_html += f'<div class="metric"><span class="metric-label">{key.title()}</span><span class="metric-value">{value}ms</span></div>'
        performance_html += '</div></div>'
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>UI/UX Test Report - {results['url']}</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
                font-weight: 300;
            }}
            
            .header p {{
                font-size: 1.2em;
                opacity: 0.9;
            }}
            
            .url-info {{
                background: rgba(255,255,255,0.1);
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                font-family: monospace;
                word-break: break-all;
            }}
            
            .overall-score {{
                background: white;
                padding: 40px;
                text-align: center;
                border-bottom: 1px solid #eee;
            }}
            
            .score-circle {{
                width: 150px;
                height: 150px;
                border-radius: 50%;
                margin: 0 auto 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2em;
                font-weight: bold;
                color: white;
                position: relative;
            }}
            
            .score-circle::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                border-radius: 50%;
                background: conic-gradient(
                    {get_score_status(average_score)[1]} 0deg {average_score * 3.6}deg,
                    #e5e7eb {average_score * 3.6}deg 360deg
                );
                z-index: -1;
            }}
            
            .score-label {{
                font-size: 1.5em;
                color: #666;
                margin-bottom: 10px;
            }}
            
            .scores-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                padding: 40px;
                background: #f8fafc;
            }}
            
            .score-card {{
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                transition: transform 0.3s ease;
            }}
            
            .score-card:hover {{
                transform: translateY(-5px);
            }}
            
            .score-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }}
            
            .score-header h3 {{
                font-size: 1.1em;
                color: #374151;
            }}
            
            .score-badge {{
                padding: 5px 12px;
                border-radius: 20px;
                color: white;
                font-weight: bold;
                font-size: 0.9em;
            }}
            
            .score-bar {{
                height: 8px;
                background: #e5e7eb;
                border-radius: 4px;
                overflow: hidden;
                margin-bottom: 10px;
            }}
            
            .score-fill {{
                height: 100%;
                transition: width 0.3s ease;
            }}
            
            .score-status {{
                font-size: 0.9em;
                font-weight: 500;
            }}
            
            .content-section {{
                padding: 40px;
            }}
            
            .section-title {{
                font-size: 1.8em;
                color: #374151;
                margin-bottom: 30px;
                text-align: center;
                position: relative;
            }}
            
            .section-title::after {{
                content: '';
                position: absolute;
                bottom: -10px;
                left: 50%;
                transform: translateX(-50%);
                width: 60px;
                height: 3px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 2px;
            }}
            
            .issues-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 30px;
                margin-bottom: 40px;
            }}
            
            .issue-section {{
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            }}
            
            .issue-section h3 {{
                color: #374151;
                margin-bottom: 15px;
                font-size: 1.2em;
            }}
            
            .issue-section ul, .issue-section ol {{
                padding-left: 20px;
            }}
            
            .issue-section li {{
                margin-bottom: 12px;
                line-height: 1.6;
                padding: 10px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #e5e7eb;
            }}
            
            .issue-main {{
                font-weight: 500;
                color: #374151;
            }}
            
            .issue-detail {{
                font-size: 0.9em;
                color: #6b7280;
                font-family: 'Courier New', monospace;
                background: #f3f4f6;
                padding: 2px 6px;
                border-radius: 4px;
                margin-left: 10px;
            }}
            
            .screenshot-container {{
                margin-top: 15px;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                overflow: hidden;
                background: #f9fafb;
            }}
            
            .issue-screenshot {{
                width: 100%;
                max-width: 400px;
                height: auto;
                cursor: pointer;
                transition: transform 0.2s ease;
                border-radius: 4px;
            }}
            
            .issue-screenshot:hover {{
                transform: scale(1.02);
            }}
            
            .screenshot-info {{
                padding: 8px 12px;
                background: #f3f4f6;
                border-top: 1px solid #e5e7eb;
                text-align: center;
                font-size: 0.8em;
                color: #6b7280;
            }}
            
            .screenshot-modal {{
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.8);
                backdrop-filter: blur(5px);
            }}
            
            .screenshot-modal-content {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                max-width: 90%;
                max-height: 90%;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            
            .screenshot-modal img {{
                width: 100%;
                height: auto;
                display: block;
            }}
            
            .screenshot-modal-header {{
                padding: 15px 20px;
                background: #f8fafc;
                border-bottom: 1px solid #e5e7eb;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            
            .screenshot-modal-close {{
                background: none;
                border: none;
                font-size: 24px;
                cursor: pointer;
                color: #6b7280;
                padding: 0;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                transition: background-color 0.2s ease;
            }}
            
            .screenshot-modal-close:hover {{
                background-color: #e5e7eb;
                color: #374151;
            }}
            
            .no-issues {{
                color: #10B981;
                font-weight: 500;
            }}
            
            .recommendations-section {{
                background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
                padding: 30px;
                border-radius: 15px;
                margin-bottom: 30px;
            }}
            
            .recommendations-section h3 {{
                color: #92400e;
                margin-bottom: 20px;
            }}
            
            .recommendations-section ol {{
                padding-left: 20px;
            }}
            
            .recommendations-section li {{
                margin-bottom: 10px;
                color: #78350f;
            }}
            
            .performance-section {{
                background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
                padding: 30px;
                border-radius: 15px;
                margin-bottom: 30px;
            }}
            
            .performance-section h3 {{
                color: #1e40af;
                margin-bottom: 20px;
            }}
            
            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
            }}
            
            .metric {{
                background: white;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
            }}
            
            .metric-label {{
                display: block;
                font-size: 0.9em;
                color: #6b7280;
                margin-bottom: 5px;
            }}
            
            .metric-value {{
                display: block;
                font-size: 1.2em;
                font-weight: bold;
                color: #1e40af;
            }}
            
            .footer {{
                background: #374151;
                color: white;
                text-align: center;
                padding: 30px;
            }}
            
            .footer p {{
                opacity: 0.8;
            }}
            
            @media (max-width: 768px) {{
                .scores-grid {{
                    grid-template-columns: 1fr;
                }}
                
                .issues-grid {{
                    grid-template-columns: 1fr;
                }}
                
                .header h1 {{
                    font-size: 2em;
                }}
                
                .container {{
                    margin: 10px;
                    border-radius: 15px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎨 UI/UX Test Report</h1>
                <p>Comprehensive analysis of user interface and user experience design principles</p>
                <div class="url-info">
                    <strong>Tested URL:</strong> {results['url']}
                </div>
            </div>
            
            <div class="overall-score">
                <div class="score-label">Overall Score</div>
                <div class="score-circle" style="background: {get_score_status(average_score)[1]}">
                    {average_score:.1f}
                </div>
                <p style="color: #666; font-size: 1.1em;">{get_score_status(average_score)[2]} {get_score_status(average_score)[0]}</p>
            </div>
            
            <div class="scores-grid">
                {score_cards_html}
            </div>
            
            <div class="content-section">
                <h2 class="section-title">📋 Detailed Analysis</h2>
                
                <div class="issues-grid">
                    {generate_issues_html(results["accessibility_issues"], "Accessibility Issues", "♿", "accessibility")}
                    {generate_issues_html(results["responsive_issues"], "Responsiveness Issues", "📱", "responsiveness")}
                    {generate_issues_html(results["broken_links"], "Broken Links", "🔗", "links")}
                    {generate_issues_html(results["broken_images"], "Broken Images", "🖼️", "images")}
                    {generate_issues_html([f"{error['level'].upper()}: {error['message']} | Source: {error.get('source', 'Unknown')} | File: {error.get('filename', 'Unknown')} | Line: {error.get('line', 'Unknown')} | Column: {error.get('column', 'Unknown')} | URL: {error['url']} | Page: {error['page_title']}" for error in results["console_errors"]], "Console Errors", "⚠️", "console")}
                </div>
                
                {recommendations_html}
                {performance_html}
            </div>
            
            <div class="footer">
                <p>Report generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
                <p>UI/UX Testing Tool - Comprehensive Design Analysis</p>
            </div>
        </div>
        
        <!-- Screenshot Modal -->
        <div id="screenshotModal" class="screenshot-modal">
            <div class="screenshot-modal-content">
                <div class="screenshot-modal-header">
                    <h3 id="modalTitle">Screenshot</h3>
                    <button class="screenshot-modal-close" onclick="closeScreenshotModal()">&times;</button>
                </div>
                <img id="modalImage" src="" alt="Screenshot">
            </div>
        </div>
        
        <script>
            // Add animation to score bars
            document.addEventListener('DOMContentLoaded', function() {{
                const scoreFills = document.querySelectorAll('.score-fill');
                scoreFills.forEach(fill => {{
                    const width = fill.style.width;
                    fill.style.width = '0%';
                    setTimeout(() => {{
                        fill.style.width = width;
                    }}, 500);
                }});
            }});
            
            // Screenshot modal functions
            function openScreenshotModal(imageSrc, filename) {{
                const modal = document.getElementById('screenshotModal');
                const modalImage = document.getElementById('modalImage');
                const modalTitle = document.getElementById('modalTitle');
                
                modalImage.src = imageSrc;
                modalTitle.textContent = filename;
                modal.style.display = 'block';
                
                // Close modal when clicking outside
                modal.onclick = function(event) {{
                    if (event.target === modal) {{
                        closeScreenshotModal();
                    }}
                }};
                
                // Close modal with Escape key
                document.addEventListener('keydown', function(event) {{
                    if (event.key === 'Escape') {{
                        closeScreenshotModal();
                    }}
                }});
            }}
            
            function closeScreenshotModal() {{
                const modal = document.getElementById('screenshotModal');
                modal.style.display = 'none';
            }}
        </script>
    </body>
    </html>
    """
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\nHTML report generated: {filename}")
    return filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UI/UX Testing Tool")
    parser.add_argument("--url", help="Website URL to test")
    parser.add_argument("--export", action="store_true", help="Export results to JSON file")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    parser.add_argument("--output", help="Output filename for export")
    
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
    
    if args.html:
        generate_html_report(results, args.output)
    
    print("\nTest completed!") 