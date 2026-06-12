# Schema Agent
# Responsible for analyzing and managing database schema
"""
Schema Agent - Retrieves and structures database schema information.
"""

from typing import Dict, List

from app.core.database import DatabaseConnection
from app.core.logger import logger


class SchemaAgent:
    """Agent responsible for fetching and formatting database schema."""
    
    def __init__(self):
        """Initialize schema agent with database connection."""
        self.db = DatabaseConnection()
    
    def get_schema_info(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Retrieve database schema information.
        
        Returns:
            Dictionary containing table and column information
        """
        logger.info("SchemaAgent: Fetching database schema")
        schema = self.db.fetch_schema()
        self.db.disconnect()
        return schema
    
    def format_schema_for_llm(self, schema: Dict[str, List[Dict[str, str]]]) -> str:
        """
        Format schema information for LLM consumption.
        
        Args:
            schema: Raw schema dictionary
            
        Returns:
            Formatted schema string
        """
        formatted_lines = ["Database Schema:"]
        
        for table_name, columns in schema.items():
            formatted_lines.append(f"\nTable: {table_name}")
            for col in columns:
                formatted_lines.append(
                    f"  - {col['column']} ({col['type']}) "
                    f"{'PRIMARY KEY' if col['key'] == 'PRI' else ''}"
                )
        
        formatted_schema = "\n".join(formatted_lines)
        logger.info("SchemaAgent: Schema formatted for LLM")
        return formatted_schema