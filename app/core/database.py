# Database Module
# Handles database connections and operations
"""
MySQL database connection and query execution module.
"""

from typing import List, Dict, Any, Optional, Tuple
import mysql.connector
from mysql.connector import Error

from app.core.config import settings
from app.core.logger import logger


class DatabaseConnection:
    """MySQL database connection handler."""
    
    def __init__(self):
        """Initialize database connection parameters."""
        self.host = settings.DB_HOST
        self.user = settings.DB_USER
        self.password = settings.DB_PASSWORD
        self.database = settings.DB_NAME
        self.port = settings.DB_PORT
        self.connection: Optional[mysql.connector.MySQLConnection] = None
    
    def connect(self) -> None:
        """
        Establish database connection.
        
        Raises:
            Exception: If connection fails
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            logger.info(f"Connected to MySQL database: {self.database}")
        except Error as e:
            logger.error(f"Database connection error: {e}")
            raise Exception(f"Failed to connect to database: {e}")
    
    def disconnect(self) -> None:
        """Close database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed")
    
    def execute_query(self, query: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Execute a SQL query and return results.
        
        Args:
            query: SQL query string
            
        Returns:
            Tuple of (rows as list of dicts, column names)
            
        Raises:
            Exception: If query execution fails
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query)
            
            # Fetch results
            rows = cursor.fetchall()
            column_names = cursor.column_names if cursor.column_names else []
            
            cursor.close()
            logger.info(f"Query executed successfully. Rows returned: {len(rows)}")
            
            return rows, list(column_names)
        
        except Error as e:
            logger.error(f"Query execution error: {e}")
            raise Exception(f"Failed to execute query: {e}")
    
    def fetch_schema(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Fetch database schema information.
        
        Returns:
            Dictionary mapping table names to their column information
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor(dictionary=True)
            
            # Get all tables in the database
            cursor.execute(f"SHOW TABLES")
            tables = cursor.fetchall()
            
            schema_info = {}
            table_key = f"Tables_in_{self.database}"
            
            for table_row in tables:
                table_name = table_row[table_key]
                
                # Get columns for each table
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                
                schema_info[table_name] = [
                    {
                        "column": col["Field"],
                        "type": col["Type"],
                        "nullable": col["Null"],
                        "key": col["Key"]
                    }
                    for col in columns
                ]
            
            cursor.close()
            logger.info(f"Schema fetched successfully. Tables found: {len(schema_info)}")
            
            return schema_info
        
        except Error as e:
            logger.error(f"Schema fetch error: {e}")
            raise Exception(f"Failed to fetch schema: {e}")