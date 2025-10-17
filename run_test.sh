#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== Running Tests ===${NC}\n"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo -e "${RED}Virtual environment not found. Run setup.sh first${NC}"
    exit 1
fi

# Check test database
echo -e "${YELLOW}Checking test database...${NC}"
psql -U postgres -lqt | cut -d \| -f 1 | grep -qw hindalco_test_db
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Creating test database...${NC}"
    psql -U postgres -c "CREATE DATABASE hindalco_test_db;"
fi
echo -e "${GREEN}✓ Test database ready${NC}\n"

# Run tests with verbose output
echo -e "${GREEN}=== Running Unit Tests ===${NC}\n"
python -m unittest test_main.py -v

# Check if tests passed
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✓ All tests passed!${NC}\n"
else
    echo -e "\n${RED}✗ Some tests failed${NC}\n"
    exit 1
fi

# Run coverage
echo -e "${GREEN}=== Running Coverage Analysis ===${NC}\n"
coverage run -m unittest test_main.py 2>/dev/null
coverage report

echo -e "\n${YELLOW}Generating HTML coverage report...${NC}"
coverage html
echo -e "${GREEN}✓ HTML report generated in htmlcov/index.html${NC}"

# Summary
echo -e "\n${GREEN}=== Test Summary ===${NC}"
coverage report | tail -n 1

echo -e "\n${YELLOW}To view detailed coverage:${NC}"
echo "  open htmlcov/index.html"
echo -e "\n${YELLOW}To run specific tests:${NC}"
echo "  python -m unittest test_main.TestStockDataAPI"
echo "  python -m unittest test_main.TestMovingAverageCalculations"
echo "  python -m unittest test_main.TestStrategyEndpoint"