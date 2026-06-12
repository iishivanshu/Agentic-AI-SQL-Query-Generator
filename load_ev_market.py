"""
Script to load the ev_market_2026.csv into the MySQL database.
"""

import csv
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Database connection config
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "agentic_sql_db"),
    "port": int(os.getenv("DB_PORT", 3306)),
}

CSV_PATH = r"C:\Users\ASUS\Downloads\ev_market_2026.csv"

# Create table SQL
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS ev_market_2026 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50),
    model VARCHAR(100),
    year INT,
    variant VARCHAR(50),
    price_usd DECIMAL(12, 2),
    battery_capacity_kwh DECIMAL(6, 2),
    range_miles DECIMAL(6, 1),
    charging_speed_kw DECIMAL(6, 1),
    acceleration_0_60_mph DECIMAL(4, 2),
    top_speed_mph DECIMAL(5, 1),
    horsepower INT,
    torque_nm DECIMAL(6, 1),
    drive_type VARCHAR(10),
    seating_capacity INT,
    body_type VARCHAR(20),
    cargo_volume_cubic_ft DECIMAL(5, 1),
    weight_kg DECIMAL(6, 1),
    safety_rating INT,
    autopilot_level INT,
    country_of_origin VARCHAR(30),
    market_segment VARCHAR(20),
    annual_sales_units INT,
    customer_rating DECIMAL(3, 2),
    warranty_years INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

INSERT_SQL = """
INSERT INTO ev_market_2026 (
    brand, model, year, variant, price_usd, battery_capacity_kwh,
    range_miles, charging_speed_kw, acceleration_0_60_mph, top_speed_mph,
    horsepower, torque_nm, drive_type, seating_capacity, body_type,
    cargo_volume_cubic_ft, weight_kg, safety_rating, autopilot_level,
    country_of_origin, market_segment, annual_sales_units, customer_rating,
    warranty_years
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s
)
"""


def main():
    print("Connecting to MySQL database...")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Drop existing table if it exists (fresh load)
    print("Dropping existing ev_market_2026 table if it exists...")
    cursor.execute("DROP TABLE IF EXISTS ev_market_2026")

    # Create new table
    print("Creating ev_market_2026 table...")
    cursor.execute(CREATE_TABLE_SQL)

    # Read CSV and insert rows
    print(f"Reading CSV from: {CSV_PATH}")
    row_count = 0
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        batch = []
        for row in reader:
            values = (
                row["brand"],
                row["model"],
                int(row["year"]),
                row["variant"],
                float(row["price_usd"]),
                float(row["battery_capacity_kwh"]),
                float(row["range_miles"]),
                float(row["charging_speed_kw"]),
                float(row["acceleration_0_60_mph"]),
                float(row["top_speed_mph"]),
                int(float(row["horsepower"])),
                float(row["torque_nm"]),
                row["drive_type"],
                int(row["seating_capacity"]),
                row["body_type"],
                float(row["cargo_volume_cubic_ft"]),
                float(row["weight_kg"]),
                int(row["safety_rating"]),
                int(row["autopilot_level"]),
                row["country_of_origin"],
                row["market_segment"],
                int(row["annual_sales_units"]),
                float(row["customer_rating"]),
                int(row["warranty_years"]),
            )
            batch.append(values)
            row_count += 1

            # Insert in batches of 500
            if len(batch) >= 500:
                cursor.executemany(INSERT_SQL, batch)
                conn.commit()
                print(f"  Inserted {row_count} rows so far...")
                batch = []

        # Insert remaining rows
        if batch:
            cursor.executemany(INSERT_SQL, batch)
            conn.commit()

    print(f"\n✅ Successfully loaded {row_count} rows into ev_market_2026 table!")

    # Verify
    cursor.execute("SELECT COUNT(*) FROM ev_market_2026")
    count = cursor.fetchone()[0]
    print(f"📊 Verification: {count} rows in ev_market_2026 table")

    # Show sample data
    cursor.execute("SELECT brand, model, year, variant, price_usd, range_miles FROM ev_market_2026 LIMIT 5")
    print("\n📋 Sample data:")
    for r in cursor.fetchall():
        print(f"  {r[0]} {r[1]} ({r[2]}) - {r[3]} | ${r[4]:,.2f} | {r[5]} miles")

    cursor.close()
    conn.close()
    print("\n🎉 Done!")


if __name__ == "__main__":
    main()
