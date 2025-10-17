#!/bin/bash
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Header
clear
print_header "Stock Data API - Quick Start Setup"

# Check if running in correct directory
if [ ! -f "main.py" ]; then
    print_error "main.py not found. Make sure you're in the project directory."
    exit 1
fi

# Step 1: Python Environment
print_header "Step 1: Setting up Python Environment"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

echo "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

echo "Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
print_success "All dependencies installed"

# Step 2: PostgreSQL Setup
print_header "Step 2: Setting up PostgreSQL Databases"

# Check if PostgreSQL is running
if ! pg_isready -q; then
    print_error "PostgreSQL is not running. Please start PostgreSQL and try again."
    echo "Run: sudo systemctl start postgresql"
    exit 1
fi
print_success "PostgreSQL is running"

# Create main database
if psql -U postgres -lqt | cut -d \| -f 1 | grep -qw hindalco_db; then
    print_success "Database 'hindalco_db' already exists"
else
    echo "Creating hindalco_db..."
    psql -U postgres -c "CREATE DATABASE hindalco_db;" > /dev/null 2>&1
    print_success "Database 'hindalco_db' created"
fi

# Create test database
if psql -U postgres -lqt | cut -d \| -f 1 | grep -qw hindalco_test_db; then
    print_success "Database 'hindalco_test_db' already exists"
else
    echo "Creating hindalco_test_db..."
    psql -U postgres -c "CREATE DATABASE hindalco_test_db;" > /dev/null 2>&1
    print_success "Database 'hindalco_test_db' created"
fi

# Step 3: Environment Configuration
print_header "Step 3: Creating Environment Configuration"

cat > .env << EOF
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/hindalco_db
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/hindalco_test_db
EOF
print_success ".env file created"

# Step 4: Check Data File
print_header "Step 4: Checking Data File"

if [ -f "hindalco_data.csv" ]; then
    lines=$(wc -l < hindalco_data.csv)
    print_success "Data file found with $lines lines"
else
    print_warning "hindalco_data.csv not found"
    echo "Please create hindalco_data.csv with your stock data before loading."
fi

# Step 5: Run Tests
print_header "Step 5: Running Tests"

echo "Running unit tests..."
python -m unittest test_main.py > /dev/null 2>&1 && print_success "All tests passed" || print_warning "Some tests failed (this is OK if database is empty)"

# Step 6: Start Instructions
print_header "Setup Complete! Next Steps:"

echo -e "${GREEN}1. Start the server:${NC}"
echo "   uvicorn main:app --reload"
echo ""
echo -e "${GREEN}2. In a new terminal, load data:${NC}"
echo "   source venv/bin/activate"
echo "   python load_data.py hindalco_data.csv"
echo ""
echo -e "${GREEN}3. Test the API:${NC}"
echo "   Open: http://localhost:8000/docs"
echo ""
echo -e "${GREEN}4. Run tests with coverage:${NC}"
echo "   ./run_tests.sh"
echo ""
echo -e "${GREEN}5. Start with Docker (alternative):${NC}"
echo "   docker-compose up --build"

print_header "Quick Test Commands"
echo "# Get all data"
echo "curl http://localhost:8000/data?limit=5"
echo ""
echo "# Add a record"
echo 'curl -X POST http://localhost:8000/data -H "Content-Type: application/json" -d '"'"'{"datetime":"2024-01-01T00:00:00","open":250.5,"high":255.0,"low":248.0,"close":253.5,"volume":1000000,"instrument":"HINDALCO"}'"'"
echo ""
echo "# Get strategy performance"
echo "curl http://localhost:8000/strategy/performance"

print_header "Environment Ready!"
echo -e "${YELLOW}Virtual environment activated. You can now start the server.${NC}"
echo -e "${YELLOW}Run 'deactivate' to exit the virtual environment.${NC}"