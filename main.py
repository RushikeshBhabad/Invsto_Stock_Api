from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:12345678@localhost:5432/hindalco_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class StockData(Base):
    __tablename__ = "stock_data"
    
    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, nullable=False, index=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    instrument = Column(String, nullable=False)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Models
class StockDataCreate(BaseModel):
    datetime: datetime
    open: float = Field(..., gt=0, description="Opening price must be positive")
    high: float = Field(..., gt=0, description="High price must be positive")
    low: float = Field(..., gt=0, description="Low price must be positive")
    close: float = Field(..., gt=0, description="Closing price must be positive")
    volume: int = Field(..., ge=0, description="Volume must be non-negative")
    instrument: str
    
    @validator('high')
    def high_must_be_highest(cls, v, values):
        if 'low' in values and v < values['low']:
            raise ValueError('High must be greater than or equal to low')
        if 'open' in values and v < values['open']:
            raise ValueError('High must be greater than or equal to open')
        if 'close' in values and v < values['close']:
            raise ValueError('High must be greater than or equal to close')
        return v
    
    @validator('low')
    def low_must_be_lowest(cls, v, values):
        if 'open' in values and v > values['open']:
            raise ValueError('Low must be less than or equal to open')
        if 'close' in values and v > values['close']:
            raise ValueError('Low must be less than or equal to close')
        return v

class StockDataResponse(BaseModel):
    id: int
    datetime: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    instrument: str
    
    class Config:
        from_attributes = True

class StrategyPerformance(BaseModel):
    total_returns: float
    number_of_trades: int
    buy_signals: int
    sell_signals: int
    short_ma_period: int
    long_ma_period: int

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI app
app = FastAPI(title="Stock Data API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Stock Data API - Use /docs for API documentation"}

@app.get("/data", response_model=List[StockDataResponse])
def get_all_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Fetch all records from the database"""
    records = db.query(StockData).offset(skip).limit(limit).all()
    return records

@app.post("/data", response_model=StockDataResponse, status_code=201)
def add_data(stock_data: StockDataCreate, db: Session = Depends(get_db)):
    """Add new record to the database"""
    db_stock = StockData(**stock_data.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

@app.post("/data/bulk", response_model=dict, status_code=201)
def add_bulk_data(stock_data_list: List[StockDataCreate], db: Session = Depends(get_db)):
    """Add multiple records to the database"""
    db_stocks = [StockData(**stock_data.dict()) for stock_data in stock_data_list]
    db.add_all(db_stocks)
    db.commit()
    return {"message": f"Successfully added {len(db_stocks)} records"}

@app.get("/strategy/performance", response_model=StrategyPerformance)
def get_strategy_performance(
    short_window: int = 20, 
    long_window: int = 50, 
    db: Session = Depends(get_db)
):
    """
    Calculate Moving Average Crossover Strategy Performance
    
    Parameters:
    - short_window: Period for short-term moving average (default: 20)
    - long_window: Period for long-term moving average (default: 50)
    """
    if short_window >= long_window:
        raise HTTPException(
            status_code=400, 
            detail="Short window must be less than long window"
        )
    
    # Fetch all data from database
    records = db.query(StockData).order_by(StockData.datetime).all()
    
    if len(records) < long_window:
        raise HTTPException(
            status_code=400, 
            detail=f"Not enough data points. Need at least {long_window} records"
        )
    
    # Convert to DataFrame
    df = pd.DataFrame([{
        'datetime': r.datetime,
        'close': r.close
    } for r in records])
    
    # Calculate moving averages
    df['short_ma'] = df['close'].rolling(window=short_window).mean()
    df['long_ma'] = df['close'].rolling(window=long_window).mean()
    
    # Generate signals
    df['signal'] = 0
    df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1  # Buy signal
    df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1  # Sell signal
    
    # Calculate position changes
    df['position'] = df['signal'].diff()
    
    buy_signals = len(df[df['position'] == 2])  # Changed from 0 to 1
    sell_signals = len(df[df['position'] == -2])  # Changed from 1 to 0
    
    # Calculate returns
    df['returns'] = df['close'].pct_change()
    df['strategy_returns'] = df['signal'].shift(1) * df['returns']
    
    total_returns = (1 + df['strategy_returns']).prod() - 1
    
    return StrategyPerformance(
        total_returns=round(total_returns * 100, 2),  # Percentage
        number_of_trades=buy_signals + sell_signals,
        buy_signals=buy_signals,
        sell_signals=sell_signals,
        short_ma_period=short_window,
        long_ma_period=long_window
    )

@app.delete("/data/all")
def delete_all_data(db: Session = Depends(get_db)):
    """Delete all records from the database (for testing purposes)"""
    deleted_count = db.query(StockData).delete()
    db.execute("ALTER SEQUENCE stock_data_id_seq RESTART WITH 1")
    db.commit()
    return {"message": f"Deleted {deleted_count} records and reset ID sequence"}
