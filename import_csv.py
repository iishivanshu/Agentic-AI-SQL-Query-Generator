"""
Import Global Weapons Systems CSV into MySQL database.
"""
import csv
import mysql.connector
from dotenv import load_dotenv
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

# Database connection
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'agentic_sql_db'),
    'port': int(os.getenv('DB_PORT', 3306)),
}

CSV_PATH = r"C:\Users\ASUS\Downloads\Global Weapons Systems.csv"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS global_weapons_systems (
    ID INT PRIMARY KEY,
    Weapon_Name VARCHAR(255),
    Country_of_Origin VARCHAR(100),
    Manufacturer VARCHAR(255),
    Category VARCHAR(100),
    Subcategory VARCHAR(255),
    Year_Introduced INT,
    Year_Retired VARCHAR(10),
    Service_Status VARCHAR(100),
    Caliber VARCHAR(255),
    Action_Type VARCHAR(255),
    Effective_Range_m DOUBLE,
    Max_Range_m DOUBLE,
    Weight_kg DOUBLE,
    Length_mm DOUBLE,
    Barrel_Length_mm DOUBLE,
    Muzzle_Velocity_mps DOUBLE,
    Rate_of_Fire_rpm DOUBLE,
    Magazine_Capacity VARCHAR(50),
    Warhead_Weight_kg DOUBLE,
    Max_Speed_kmh DOUBLE,
    Crew_Size INT,
    Unit_Cost_USD DOUBLE,
    Num_Operator_Nations INT,
    Primary_Users TEXT,
    NATO_Compatible VARCHAR(20),
    Generation VARCHAR(50),
    Theater_of_Operation VARCHAR(100),
    Export_Status VARCHAR(100),
    Combat_Proven VARCHAR(20),
    Propulsion_Type VARCHAR(255),
    Guidance_System VARCHAR(255),
    Communication_System VARCHAR(255),
    Operating_Environment VARCHAR(100),
    Protection_Level VARCHAR(255),
    Notes TEXT
);
"""

INSERT_SQL = """
INSERT INTO global_weapons_systems (
    ID, Weapon_Name, Country_of_Origin, Manufacturer, Category, Subcategory,
    Year_Introduced, Year_Retired, Service_Status, Caliber, Action_Type,
    Effective_Range_m, Max_Range_m, Weight_kg, Length_mm, Barrel_Length_mm,
    Muzzle_Velocity_mps, Rate_of_Fire_rpm, Magazine_Capacity, Warhead_Weight_kg,
    Max_Speed_kmh, Crew_Size, Unit_Cost_USD, Num_Operator_Nations, Primary_Users,
    NATO_Compatible, Generation, Theater_of_Operation, Export_Status, Combat_Proven,
    Propulsion_Type, Guidance_System, Communication_System, Operating_Environment,
    Protection_Level, Notes
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s
)
"""

def safe_float(val):
    """Convert to float or None."""
    if val is None or val.strip() == '':
        return None
    try:
        return float(val.replace(',', ''))
    except ValueError:
        return None

def safe_int(val):
    """Convert to int or None."""
    if val is None or val.strip() == '':
        return None
    try:
        return int(float(val))
    except ValueError:
        return None

def main():
    print("🔌 Connecting to MySQL...")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Drop existing table and recreate
    print("🗑️  Dropping existing table if any...")
    cursor.execute("DROP TABLE IF EXISTS global_weapons_systems")
    
    print("📋 Creating table...")
    cursor.execute(CREATE_TABLE_SQL)
    conn.commit()

    print(f"📂 Reading CSV: {CSV_PATH}")
    
    row_count = 0
    batch = []
    batch_size = 500

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        
        for row in reader:
            if len(row) < 36:
                row.extend([''] * (36 - len(row)))
            
            record = (
                safe_int(row[0]),        # ID
                row[1].strip(),          # Weapon_Name
                row[2].strip(),          # Country_of_Origin
                row[3].strip(),          # Manufacturer
                row[4].strip(),          # Category
                row[5].strip(),          # Subcategory
                safe_int(row[6]),        # Year_Introduced
                row[7].strip() or None,  # Year_Retired
                row[8].strip(),          # Service_Status
                row[9].strip(),          # Caliber
                row[10].strip(),         # Action_Type
                safe_float(row[11]),     # Effective_Range_m
                safe_float(row[12]),     # Max_Range_m
                safe_float(row[13]),     # Weight_kg
                safe_float(row[14]),     # Length_mm
                safe_float(row[15]),     # Barrel_Length_mm
                safe_float(row[16]),     # Muzzle_Velocity_mps
                safe_float(row[17]),     # Rate_of_Fire_rpm
                row[18].strip() or None, # Magazine_Capacity (can be "Belt")
                safe_float(row[19]),     # Warhead_Weight_kg
                safe_float(row[20]),     # Max_Speed_kmh
                safe_int(row[21]),       # Crew_Size
                safe_float(row[22]),     # Unit_Cost_USD
                safe_int(row[23]),       # Num_Operator_Nations
                row[24].strip(),         # Primary_Users
                row[25].strip() or None, # NATO_Compatible
                row[26].strip(),         # Generation
                row[27].strip(),         # Theater_of_Operation
                row[28].strip(),         # Export_Status
                row[29].strip() or None, # Combat_Proven
                row[30].strip(),         # Propulsion_Type
                row[31].strip(),         # Guidance_System
                row[32].strip(),         # Communication_System
                row[33].strip(),         # Operating_Environment
                row[34].strip(),         # Protection_Level
                row[35].strip() if len(row) > 35 else None,  # Notes
            )
            
            batch.append(record)
            row_count += 1
            
            if len(batch) >= batch_size:
                cursor.executemany(INSERT_SQL, batch)
                conn.commit()
                print(f"  ✅ Inserted {row_count} rows...")
                batch = []

    # Insert remaining rows
    if batch:
        cursor.executemany(INSERT_SQL, batch)
        conn.commit()

    print(f"\n🎉 Done! Imported {row_count} rows into 'global_weapons_systems' table.")
    
    # Verify
    cursor.execute("SELECT COUNT(*) FROM global_weapons_systems")
    count = cursor.fetchone()[0]
    print(f"📊 Verification: {count} rows in database.")
    
    # Show sample
    cursor.execute("SELECT ID, Weapon_Name, Country_of_Origin, Category FROM global_weapons_systems LIMIT 5")
    print("\n📋 Sample data:")
    for r in cursor.fetchall():
        print(f"  {r[0]} | {r[1]} | {r[2]} | {r[3]}")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
