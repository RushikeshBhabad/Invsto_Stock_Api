# 📋 Assignment Submission Checklist

## Before You Submit - Complete Verification

### ✅ Phase 1: Files & Code

#### Core Application Files
- [ ] `main.py` - FastAPI application is complete
- [ ] `test_main.py` - All tests are written and passing
- [ ] `load_data.py` - Data loader script is functional
- [ ] `requirements.txt` - All dependencies listed with correct versions
- [ ] `Dockerfile` - Docker configuration is correct
- [ ] `docker-compose.yml` - Services configuration is complete
- [ ] `README.md` - Documentation is comprehensive
- [ ] `.gitignore` - Proper files are excluded

#### Helper Scripts
- [ ] `setup.sh` - Database setup script works
- [ ] `quick_start.sh` - Automated setup script works
- [ ] `run_tests.sh` - Test runner script works
- [ ] All scripts have execute permissions (`chmod +x *.sh`)

#### Data Files
- [ ] `hindalco_data.csv` - Stock data is properly formatted
- [ ] CSV has correct headers: datetime,open,high,low,close,volume,instrument
- [ ] CSV data is clean (no missing values, correct types)

---

### ✅ Phase 2: Functionality Testing

#### Database Setup
- [ ] PostgreSQL is installed and running
- [ ] Database `hindalco_db` is created
- [ ] Database `hindalco_test_db` is created
- [ ] Connection to database works
- [ ] Tables are created automatically by SQLAlchemy

#### API Endpoints
- [ ] Server starts without errors
- [ ] GET `/` returns welcome message
- [ ] GET `/data` returns stock records
- [ ] GET `/data` pagination works (skip, limit parameters)
- [ ] POST `/data` adds single record successfully
- [ ] POST `/data` validates input correctly (rejects invalid data)
- [ ] POST `/data/bulk` adds multiple records
- [ ] GET `/strategy/performance` returns correct metrics
- [ ] DELETE `/data/all` works (for testing)

#### Data Validation
- [ ] Rejects negative prices (open, high, low, close)
- [ ] Validates high >= low
- [ ] Validates high >= open, close
- [ ] Validates low <= open, close
- [ ] Rejects negative volume
- [ ] Validates datetime format
- [ ] Returns proper error messages (422 status)

#### Strategy Calculation
- [ ] Moving averages calculate correctly
- [ ] Buy signals generate when short MA > long MA
- [ ] Sell signals generate when short MA < long MA
- [ ] Total returns calculate correctly
- [ ] Trade counts are accurate
- [ ] Validates window parameters (short < long)
- [ ] Handles insufficient data gracefully

---

### ✅ Phase 3: Testing

#### Unit Tests
- [ ] All tests pass (`python -m unittest test_main.py`)
- [ ] Test output shows 0 failures, 0 errors
- [ ] At least 50+ tests implemented
- [ ] Tests cover input validation
- [ ] Tests cover API endpoints
- [ ] Tests cover moving average calculations
- [ ] Tests cover strategy logic

#### Test Coverage
- [ ] Coverage report generated (`coverage report`)
- [ ] Coverage is >80% (84% achieved)
- [ ] HTML coverage report created (`coverage html`)
- [ ] Coverage report reviewed for gaps

#### Test Categories Covered
- [ ] TestStockDataAPI class with 7+ tests
- [ ] TestMovingAverageCalculations class with 3+ tests
- [ ] TestStrategyEndpoint class with 4+ tests

---

### ✅ Phase 4: Docker Setup

#### Docker Files
- [ ] Dockerfile builds successfully
- [ ] docker-compose.yml is configured correctly
- [ ] Services start without errors

#### Docker Testing
- [ ] `docker-compose up --build` works
- [ ] Both containers start (app and db)
- [ ] `docker-compose ps` shows running containers
- [ ] API accessible at http://localhost:8000
- [ ] Data can be loaded in Docker environment
- [ ] Logs are accessible (`docker-compose logs`)
- [ ] Services stop cleanly (`docker-compose down`)

---

### ✅ Phase 5: Documentation

#### README.md
- [ ] Has project description
- [ ] Lists all features
- [ ] Shows tech stack
- [ ] Includes prerequisites
- [ ] Has installation instructions for all methods
- [ ] Documents all API endpoints with examples
- [ ] Explains trading strategy
- [ ] Shows testing instructions
- [ ] Has troubleshooting section
- [ ] Includes usage examples

#### Additional Documentation
- [ ] STEP_BY_STEP_GUIDE.md is complete
- [ ] COMMANDS_REFERENCE.md has all commands
- [ ] Code has inline comments where needed
- [ ] Functions have docstrings

---

### ✅ Phase 6: Screenshots

#### Required Screenshots
- [ ] **Screenshot API**: API Documentation page (`/docs`)
  - Shows all endpoints
  - Swagger UI visible
  - Clear and readable

- [ ] **Screenshot API (1,2)**: GET /data response
  - Shows JSON response with records
  - Demonstrates pagination
  - Data format is clear

- [ ] **Screenshot (API 3, 4)**: POST /data response
  - Shows successful record addition
  - Includes returned ID
  - Demonstrates validation

- [ ] **Screenshot API (5)**: Strategy performance response
  - Shows all metrics (returns, trades, signals)
  - JSON formatted
  - Values are reasonable

- [ ] **Screenshot Unit Test**: Test results
  - Terminal output of test run
  - Shows all tests passed
  - Includes test count and timing

- [ ] **Screenshot Unit Test - Coverage**: Coverage report
  - Shows coverage percentage
  - Lists all files
  - Demonstrates >80% coverage

- [ ] **Screenshot DockerFile**: Docker status
  - Shows `docker-compose ps` output
  - Both containers running
  - Ports correctly mapped

#### Screenshot Quality
- [ ] All screenshots are clear and readable
- [ ] Text is legible (not too small)
- [ ] Full output is visible
- [ ] Screenshots are properly named
- [ ] Screenshots show timestamps where relevant

---

### ✅ Phase 7: GitHub Repository

#### Repository Setup
- [ ] Repository created on GitHub
- [ ] Repository is PUBLIC
- [ ] Repository name is descriptive
- [ ] Repository has description

#### Files Committed
- [ ] All source code files pushed
- [ ] README.md displays correctly on GitHub
- [ ] requirements.txt is present
- [ ] Docker files are present
- [ ] Helper scripts are present
- [ ] .gitignore is working (no venv/, __pycache__, etc.)

#### Repository Quality
- [ ] Commit messages are descriptive
- [ ] No sensitive data committed (passwords, keys)
- [ ] No unnecessary files (*.pyc, venv/, etc.)
- [ ] Screenshots folder created (if including screenshots)

#### GitHub README
- [ ] Displays correctly on repository page
- [ ] Images/badges show properly
- [ ] Links work correctly
- [ ] Code blocks are formatted
- [ ] Tables are readable

---
