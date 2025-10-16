"""
Script to convert the PDF data to CSV format
You can manually copy the data from the PDF or use this script
"""

import csv

# Sample data structure - you'll need to extract all data from the PDF
# This shows the format you need
sample_data = """datetime,open,high,low,close,volume,instrument
2014-01-24 00:00:00,113.15,115.35,113,114,5737135,HINDALCO
2014-01-27 00:00:00,112,112.7,109.3,111.1,8724577,HINDALCO
2014-01-28 00:00:00,110,115,109.75,113.8,4513345,HINDALCO
2014-01-29 00:00:00,114.5,114.75,111.15,111.75,4713458,HINDALCO
2014-01-30 00:00:00,110.2,110.7,107.6,108.1,5077231,HINDALCO
"""

def create_csv_file(output_file='hindalco_data.csv'):
    """
    Create CSV file with stock data
    You need to add all the rows from the PDF
    """
    with open(output_file, 'w', newline='') as f:
        f.write(sample_data)
    
    print(f"✓ Created {output_file}")
    print("⚠ NOTE: This is sample data. You need to add all rows from the PDF")
    print("\nTo complete:")
    print("1. Open the PDF")
    print("2. Copy all the data rows")
    print("3. Format as CSV (comma-separated)")
    print("4. Save as hindalco_data.csv")
    print("\nFormat: datetime,open,high,low,close,volume,instrument")

if __name__ == "__main__":
    create_csv_file()