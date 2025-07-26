#!/bin/bash

# Exit on error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎯 UI/UX Testing Tool${NC}"
echo "========================"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate the virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip and install requirements
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Check if demo mode is requested
if [ "$1" = "--demo" ]; then
    echo -e "${GREEN}Running demo mode...${NC}"
    python demo.py
else
    echo -e "${GREEN}Starting UI/UX tester...${NC}"
    echo -e "${BLUE}Usage options:${NC}"
    echo "  ./run_ui_ux_test.sh          - Interactive mode"
    echo "  ./run_ui_ux_test.sh --demo   - Run demo with sample website"
    echo "  python ui_ux_tester.py --url <website> --export"
    echo ""
    python ui_ux_tester.py
fi 