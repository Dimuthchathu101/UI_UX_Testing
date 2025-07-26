# UI/UX Testing Tool

A comprehensive UI/UX testing tool that evaluates websites against 10 fundamental design principles to ensure optimal user experience.

## 🎯 Design Principles Tested

This tool evaluates websites against the following UI/UX design principles:

### 1. **Simplicity** 
- Easy to use and navigate with minimal effort
- Checks navigation complexity, content organization, and visual hierarchy
- Evaluates whitespace usage and clear call-to-actions

### 2. **User-Centered Design**
- Focuses on user needs and accessibility
- Tests keyboard navigation support, screen reader compatibility
- Evaluates mobile-friendly design and color contrast

### 3. **Visibility**
- Clear and visible interface highlighting important tasks
- Checks for prominent call-to-action buttons
- Evaluates navigation clarity and information hierarchy

### 4. **Consistency**
- Consistent design elements like colors, typography, and layout
- Tests color palette consistency, typography uniformity
- Evaluates spacing patterns and button styling consistency

### 5. **Feedback**
- Visual cues, animations, and success messages
- Tests form validation feedback, loading indicators
- Evaluates hover effects and message containers

### 6. **Clarity**
- Clear content and interface elements
- Tests page titles, heading structure, and link text
- Evaluates form labels and descriptive content

### 7. **Accessibility**
- Usable by everyone including users with disabilities
- Tests alt text, semantic HTML, and keyboard navigation
- Evaluates heading hierarchy and screen reader support

### 8. **Improved Usability**
- Easy to use and navigate for better user satisfaction
- Tests navigation structure, search functionality
- Evaluates breadcrumbs and page load times

### 9. **Efficiency**
- Optimized for speed and performance
- Tests image optimization, HTTP requests, and form design
- Evaluates clear call-to-actions for efficient user flow

### 10. **Delight**
- Invokes positive user emotions and engagement
- Tests modern design elements, engaging visuals
- Evaluates interactive elements and positive messaging

## 🚀 Features

- **Comprehensive Scoring**: Each principle is scored from 0-100
- **Detailed Recommendations**: Specific actionable improvements
- **Performance Metrics**: Page load times and resource analysis
- **Accessibility Testing**: WCAG compliance checks
- **Responsive Design**: Multi-device compatibility testing
- **Export Functionality**: JSON export for further analysis
- **Command Line Interface**: Easy integration into workflows

## 📋 Requirements

- Python 3.7+
- Chrome browser
- Internet connection

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd UI_UX_Testing
```

2. Run the setup script:
```bash
chmod +x run_ui_ux_test.sh
./run_ui_ux_test.sh
```

Or manually install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🎮 Usage

### Basic Usage
```bash
python ui_ux_tester.py
```

### Command Line Options
```bash
# Test a specific URL
python ui_ux_tester.py --url https://example.com

# Export results to JSON
python ui_ux_tester.py --url https://example.com --export

# Specify output filename
python ui_ux_tester.py --url https://example.com --export --output my_results.json
```

### Interactive Mode
```bash
python ui_ux_tester.py
# Enter website URL when prompted
```

## 📊 Sample Output

```
============================================================
UI/UX Test Report for: https://example.com
============================================================

[ SIMPLICITY SCORE: 85.00 ]
--------------------------------------------------
- Consider reducing navigation complexity - too many nav elements found

[ USER-CENTERED DESIGN SCORE: 75.00 ]
--------------------------------------------------
- Add ARIA labels for better screen reader support

[ VISIBILITY SCORE: 90.00 ]
--------------------------------------------------
No specific visibility recommendations found.

[ CONSISTENCY SCORE: 80.00 ]
--------------------------------------------------
- Use consistent typography throughout the interface

[ FEEDBACK SCORE: 70.00 ]
--------------------------------------------------
- Add loading indicators for better user feedback

[ CLARITY SCORE: 95.00 ]
--------------------------------------------------
No specific clarity recommendations found.

[ ACCESSIBILITY SCORE: 85.00 ]
--------------------------------------------------
- Add alt text to all images for screen reader accessibility

[ USABILITY SCORE: 80.00 ]
--------------------------------------------------
- Consider adding search functionality for better usability

[ EFFICIENCY SCORE: 75.00 ]
--------------------------------------------------
- Optimize and compress images for faster loading

[ DELIGHT SCORE: 70.00 ]
--------------------------------------------------
- Add modern design elements like cards, shadows, or subtle animations

============================================================
OVERALL UI/UX DESIGN PRINCIPLES SUMMARY
============================================================

Overall Average Score: 81.5/100

Individual Principle Scores:
----------------------------------------
Simplicity                   85/100 ✅ EXCELLENT
User-Centered Design         75/100 🟡 GOOD
Visibility                   90/100 ✅ EXCELLENT
Consistency                  80/100 🟡 GOOD
Feedback                     70/100 🟡 GOOD
Clarity                      95/100 ✅ EXCELLENT
Accessibility                85/100 ✅ EXCELLENT
Usability                    80/100 🟡 GOOD
Efficiency                   75/100 🟡 GOOD
Delight                      70/100 🟡 GOOD

Total Score: 815/1000

============================================================
PRIORITY RECOMMENDATIONS
============================================================
Top recommendations for improvement:
1. Add ARIA labels for better screen reader support
2. Add loading indicators for better user feedback
3. Add alt text to all images for screen reader accessibility
4. Consider adding search functionality for better usability
5. Optimize and compress images for faster loading
```

## 📁 Output Files

When using the `--export` flag, the tool generates a JSON file containing:
- Individual principle scores
- Detailed recommendations
- Performance metrics
- Accessibility issues
- Broken links and images
- Console errors
- Meta tags analysis

## 🔧 Configuration

The tool can be customized by modifying the scoring thresholds and test parameters in the individual test functions within `ui_ux_tester.py`.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Additional design principles
- Improved testing algorithms
- Enhanced reporting features
- Bug fixes and optimizations

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

This tool is designed to help developers and designers create better user experiences by following established UI/UX design principles and best practices.