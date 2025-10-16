import unittest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from main import app, get_db, Base, StockData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

# -------------------------------
# Test Database Setup
# -------------------------------
TEST_DATABASE_URL = "postgresql://postgres:12345678@localhost:5432/hindalco_test_db"
test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Override FastAPI dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test tables
Base.metadata.create_all(bind=test_engine)
client = TestClient(app)

# -------------------------------
# Tests
# -------------------------------
class TestStockDataAPI(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(bind=test_engine)
        Base.metadata.create_all(bind=test_engine)

    def tearDown(self):
        Base.metadata.drop_all(bind=test_engine)

    def test_root_endpoint(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_get_empty_data(self):
        response = client.get("/data")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

# -------------------------------
# Strategy Endpoint Tests
# -------------------------------
class TestStrategyEndpoint(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(bind=test_engine)
        Base.metadata.create_all(bind=test_engine)
        db = TestingSessionLocal()
        base_price = 100
        base_date = datetime(2024, 1, 1)
        for i in range(100):
            record = StockData(
                datetime=base_date + timedelta(days=i),  # safe date increment
                open=base_price + i*0.5,
                high=base_price + i*0.5 + 2,
                low=base_price + i*0.5 - 2,
                close=base_price + i*0.5 + 1,
                volume=1000000 + i*1000,
                instrument="HINDALCO"
            )
            db.add(record)
        db.commit()
        db.close()

    def tearDown(self):
        Base.metadata.drop_all(bind=test_engine)

    def test_strategy_performance_endpoint(self):
        response = client.get("/strategy/performance?short_window=10&long_window=20")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total_returns", data)
        self.assertIn("number_of_trades", data)
        self.assertIn("buy_signals", data)
        self.assertIn("sell_signals", data)

    def test_strategy_invalid_windows(self):
        response = client.get("/strategy/performance?short_window=50&long_window=20")
        self.assertEqual(response.status_code, 400)

    def test_strategy_insufficient_data(self):
        db = TestingSessionLocal()
        db.query(StockData).delete()
        db.commit()
        db.close()
        response = client.get("/strategy/performance?short_window=10&long_window=20")
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
