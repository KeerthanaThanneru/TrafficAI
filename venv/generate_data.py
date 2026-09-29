import csv
import random
from datetime import datetime

def generate_reading(junction_id, hour):
    peak = hour in [8, 9, 17, 18, 19]
    vehicle_count = random.randint(60, 120) if peak else random.randint(10, 50)
    avg_speed = random.randint(10, 20) if peak else random.randint(30, 60)
    level = "Low" if vehicle_count < 40 else "Medium" if vehicle_count < 80 else "High"
    return {
        "timestamp": datetime(2026, 1, 1, hour, 0, 0).isoformat(),
        "junction_id": junction_id,
        "vehicle_count": vehicle_count,
        "avg_speed": avg_speed,
        "congestion_level": level
    }

rows = []
for junction_id in range(1, 5):
    for hour in range(24):
        rows.append(generate_reading(junction_id, hour))

with open("data/traffic_data.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} rows into data/traffic_data.csv")