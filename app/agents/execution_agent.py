# Execution Agent
# Responsible for executing SQL queries against the database
"""
Execution Agent - Executes validated SQL queries.
"""

from typing import List, Dict, Any, Tuple

from app.core.database import DatabaseConnection
from app.core.logger import logger


class ExecutionAgent:
    """Agent responsible for executing SQL queries."""
    
    def __init__(self):
        """Initialize execution agent with database connection."""
        self.db = DatabaseConnection()
    
    def execute_sql(self, sql: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Execute SQL query and return results.
        
        Args:
            sql: Validated SQL query string
            
        Returns:
            Tuple of (result rows, column names)
            
        Raises:
            Exception: If execution fails
        """
        logger.info("ExecutionAgent: Executing SQL query")
        
        try:
            rows, columns = self.db.execute_query(sql)
            logger.info(f"ExecutionAgent: Query executed. Rows returned: {len(rows)}")
            return rows, columns
        
        except Exception as e:
            logger.error(f"ExecutionAgent: Execution failed - {e}")
            raise
        
        finally:
            self.db.disconnect()
    
    def format_results(
        self,
        rows: List[Dict[str, Any]],
        columns: List[str],
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Format query results for presentation.
        
        Args:
            rows: Query result rows
            columns: Column names
            limit: Maximum number of rows to return
            
        Returns:
            Formatted results
        """
        logger.info("ExecutionAgent: Formatting results")
        
        # Limit results if too many
        limited_rows = rows[:limit]
        
        if len(rows) > limit:
            logger.info(f"ExecutionAgent: Results limited to {limit} rows (total: {len(rows)})")
        
        return limited_rows