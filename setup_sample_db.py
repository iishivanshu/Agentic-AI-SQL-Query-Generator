import mysql.connector
from mysql.connector import Error
import getpass
import os

def setup_database():
    print("🤖 Agentic AI SQL Query Generator - Database Setup")
    print("--------------------------------------------------")
    print("This script will create a sample database 'agentic_sql_db' with some tables (customers, orders, products) to test the application.")
    
    # Get MySQL credentials
    host = input("Enter MySQL Host [localhost]: ").strip() or "localhost"
    user = input("Enter MySQL User [root]: ").strip() or "root"
    password = getpass.getpass("Enter MySQL Password: ")
    
    try:
        # Connect to MySQL server (without specifying a database)
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create Database
            db_name = "agentic_sql_db"
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
            print(f"✅ Database '{db_name}' created or already exists.")
            
            # Use the database
            cursor.execute(f"USE {db_name};")
            
            # Create sample tables
            print("⏳ Creating sample tables and inserting data...")
            
            # 1. Customers Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE,
                    city VARCHAR(50),
                    country VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # 2. Products Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    category VARCHAR(50),
                    price DECIMAL(10, 2),
                    stock INT DEFAULT 0
                );
            """)
            
            # 3. Orders Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_id INT,
                    product_id INT,
                    quantity INT,
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                );
            """)
            
            # Insert Sample Data (Ignore if already exists)
            # Customers
            cursor.execute("SELECT COUNT(*) FROM customers")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO customers (name, email, city, country) VALUES
                    ('John Doe', 'john@example.com', 'New York', 'USA'),
                    ('Jane Smith', 'jane@example.com', 'London', 'UK'),
                    ('Michael Johnson', 'mike@example.com', 'New York', 'USA'),
                    ('Emily Davis', 'emily@example.com', 'Paris', 'France')
                """)
                
            # Products
            cursor.execute("SELECT COUNT(*) FROM products")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO products (name, category, price, stock) VALUES
                    ('Laptop Pro', 'Electronics', 1299.99, 50),
                    ('Wireless Mouse', 'Accessories', 29.99, 200),
                    ('Mechanical Keyboard', 'Accessories', 149.50, 75),
                    ('27-inch Monitor', 'Electronics', 349.00, 30)
                """)
                
            # Orders
            cursor.execute("SELECT COUNT(*) FROM orders")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO orders (customer_id, product_id, quantity) VALUES
                    (1, 1, 1),
                    (1, 2, 2),
                    (2, 3, 1),
                    (3, 4, 2),
                    (4, 1, 1)
                """)
                
            # Commit the changes
            connection.commit()
            print("✅ Sample tables (customers, products, orders) created and populated.")
            
            # Update .env file
            env_path = ".env"
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    lines = f.readlines()
                
                with open(env_path, 'w') as f:
                    for line in lines:
                        if line.startswith('DB_PASSWORD='):
                            f.write(f'DB_PASSWORD={password}\n')
                        elif line.startswith('DB_NAME='):
                            f.write(f'DB_NAME={db_name}\n')
                        elif line.startswith('DB_USER='):
                            f.write(f'DB_USER={user}\n')
                        else:
                            f.write(line)
                print("✅ Updated .env file with your database credentials.")
            else:
                print("⚠️ .env file not found. Please manually update your .env file.")
                
            print("\n🎉 Setup complete! You can now run the application.")
            
    except Error as e:
        print(f"❌ Error while connecting to MySQL: {e}")
        print("Please ensure MySQL is running and your credentials are correct.")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    setup_database()
