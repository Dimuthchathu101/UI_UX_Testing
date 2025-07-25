import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def run_ui_ux_test(url):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    results = {
        "url": url,
        "accessibility_issues": [],
        "responsive_issues": [],
        "broken_links": [],
        "broken_images": [],
        "console_errors": [],
        "performance_metrics": {},
        "meta_tags": {}
    }

    try:
        # Open URL and wait for initial load
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Basic accessibility checks
        check_accessibility(driver, results)
        
        # Responsiveness check
        check_responsiveness(driver, results)
        
        # Find broken links
        check_broken_links(driver, results)
        
        # Find broken images
        check_broken_images(driver, results)
        
        # Get console errors
        results["console_errors"] = get_console_errors(driver)
        
        # Get performance metrics
        results["performance_metrics"] = get_performance_metrics(driver)
        
        # Get meta tags
        results["meta_tags"] = get_meta_tags(driver)
        
    except Exception as e:
        results["error"] = f"Test failed: {str(e)}"
    finally:
        driver.quit()
    
    return results

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
    
    # Accessibility Report
    print("\n[ ACCESSIBILITY ISSUES ]")
    if results["accessibility_issues"]:
        for issue in results["accessibility_issues"]:
            print(f"- {issue}")
    else:
        print("No critical accessibility issues found")
    
    # Responsiveness Report
    print("\n[ RESPONSIVENESS ISSUES ]")
    if results["responsive_issues"]:
        for issue in results["responsive_issues"]:
            print(f"- {issue}")
    else:
        print("No responsiveness issues found")
    
    # Broken Links Report
    print("\n[ BROKEN LINKS ]")
    if results["broken_links"]:
        for link in results["broken_links"]:
            print(f"- {link}")
    else:
        print("No broken links found")
    
    # Broken Images Report
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

if __name__ == "__main__":
    url = input("Enter website URL to test: ").strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    print(f"\nStarting UI/UX test for {url}...")
    results = run_ui_ux_test(url)
    generate_report(results)
    print("\nTest completed!") 