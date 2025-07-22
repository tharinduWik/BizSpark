import sys
import os
sys.path.append('.')

from file_loader import load_all_data

# Test data loading
print("Testing data loading...")
data = load_all_data("../data/")

print(f"\nFound {len(data)} rooms:")
for room_name, df in data.items():
    print(f"- {room_name}: {len(df)} records, columns: {list(df.columns)}")
    if len(df) > 0:
        print(f"  Sample row: {df.iloc[0].to_dict()}")

print("Test complete!")
