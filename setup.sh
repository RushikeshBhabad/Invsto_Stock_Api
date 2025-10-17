#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Stock API Setup Script ===${NC}\n"

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.13.7${NC}"
    exit 1
fi

# Check PostgreSQL
echo -e "\n${YELLOW}Checking PostgreSQL...${NC}"
if ! command -v psql &> /dev/null; then
    echo -e "${RED}PostgreSQL is not installed. Please install PostgreSQL 16${NC}"
    exit 1
fi

pg_version=$(psql --version | awk '{print $3}')
echo "Found PostgreSQL $pg_version"

# Create virtual environment
echo -e "\n${YELLOW}Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install dependencies
echo -e "\n${YELLOW}Installing Python dependencies...${NC}"
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create databases
echo -e "\n${YELLOW}Setting up databases...${NC}"
echo "Creating hindalco_db..."
psql -U postgres -c "CREATE DATABASE hindalco_db;" 2>/dev/null || echo "Database hindalco_db already exists"

echo "Creating hindalco_test_db..."
psql -U postgres -c "CREATE DATABASE hindalco_test_db;" 2>/dev/null || echo "Database hindalco_test_db already exists"

echo -e "${GREEN}✓ Databases ready${NC}"

# Check if CSV file exists
echo -e "\n${YELLOW}Checking for data file...${NC}"
if [ ! -f "hindalco_data.csv" ]; then
    echo -e "${YELLOW}⚠ hindalco_data.csv not found${NC}"
    echo "Please create hindalco_data.csv with your stock data"
    echo "Format: datetime,open,high,low,close,volume,instrument"
else
    echo -e "${GREEN}✓ Data file found${NC}"
fi

# Create .env file
echo -e "\n${YELLOW}Creating environment configuration...${NC}"
cat > .env << EOF
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/hindalco_db
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/hindalco_test_db
EOF
echo -e "${GREEN}✓ Environment file created${NC}"

# Summary
echo -e "\n${GREEN}=== Setup Complete ===${NC}\n"
echo "Next steps:"
echo "1. Make sure hindalco_data.csv exists with your data"
echo "2. Start the server: uvicorn main:app --reload"
echo "3. In a new terminal, load data: python load_data.py hindalco_data.csv"
echo "4. Run tests: python -m unittest test_main.py -v"
echo "5. Visit http://localhost:8000/docs for API documentation"
echo ""
echo -e "${YELLOW}To activate virtual environment:${NC} source venv/bin/activate"
echo -e "${YELLOW}To deactivate:${NC} deactivate"