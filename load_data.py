import pandas as pd
import requests
from datetime import datetime
import time

# API endpoint
BASE_URL = "http://localhost:8000"

def load_csv_to_api(csv_file_path):
    """Load data from CSV file and send to API"""
    
    print(f"Reading CSV file: {csv_file_path}")
    df = pd.read_csv(csv_file_path)
    
    print(f"Total records: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Convert to list of dictionaries
    records = []
    for _, row in df.iterrows():
        try:
            record = {
                "datetime": row['datetime'],
                "open": float(row['open']),
                "high": float(row['high']),
                "low": float(row['low']),
                "close": float(row['close']),
                "volume": int(row['volume']),
                "instrument": row['instrument']
            }
            records.append(record)
        except Exception as e:
            print(f"Error processing row: {e}")
            continue
    
    print(f"Processed {len(records)} valid records")
    
    # Send in batches
    batch_size = 100
    total_batches = (len(records) + batch_size - 1) // batch_size
    
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        batch_num = i // batch_size + 1
        
        print(f"Sending batch {batch_num}/{total_batches} ({len(batch)} records)...")
        
        try:
            response = requests.post(f"{BASE_URL}/data/bulk", json=batch)
            if response.status_code == 201:
                print(f"✓ Batch {batch_num} uploaded successfully")
            else:
                print(f"✗ Batch {batch_num} failed: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"✗ Error sending batch {batch_num}: {e}")
        
        time.sleep(0.1)  # Small delay between batches
    
    print("\n=== Data Upload Complete ===")
    
    # Verify data
    try:
        response = requests.get(f"{BASE_URL}/data?limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"\nFirst 5 records in database:")
            for record in data:
                print(f"  {record['datetime']}: Close={record['close']}, Volume={record['volume']}")
    except Exception as e:
        print(f"Error verifying data: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python load_data.py <csv_file_path>")
        print("Example: python load_data.py hindalco_data.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    load_csv_to_api(csv_file)