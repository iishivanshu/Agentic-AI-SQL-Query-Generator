# Safety Agent
# Responsible for validating and ensuring query safety
"""
Safety Agent - Validates SQL queries for safety.
"""

from typing import Tuple
import re

from app.core.logger import logger


class SafetyAgent:
    """Agent responsible for validating SQL query safety."""
    
    # Dangerous SQL operations that should be blocked
    DANGEROUS_KEYWORDS = [
        "DROP", "DELETE", "UPDATE", "ALTER", "TRUNCATE",
        "INSERT", "CREATE", "GRANT", "REVOKE", "EXECUTE"
    ]
    
    def validate_sql(self, sql: str) -> Tuple[bool, str]:
        """
        Validate SQL query for safety.
        
        Args:
            sql: SQL query string to validate
            
        Returns:
            Tuple of (is_safe: bool, reason: str)
        """
        logger.info("SafetyAgent: Validating SQL query")
        
        sql_upper = sql.upper()
        
        # Check for dangerous keywords
        for keyword in self.DANGEROUS_KEYWORDS:
            # Use word boundary to avoid false positives
            pattern = r'\b' + keyword + r'\b'
            if re.search(pattern, sql_upper):
                reason = f"Blocked: Query contains dangerous operation '{keyword}'"
                logger.warning(f"SafetyAgent: {reason}")
                return False, reason
        
        # Ensure query starts with SELECT
        if not sql_upper.strip().startswith("SELECT"):
            reason = "Blocked: Only SELECT queries are allowed"
            logger.warning(f"SafetyAgent: {reason}")
            return False, reason
        
        # Check for SQL injection patterns
        if self._check_injection_patterns(sql):
            reason = "Blocked: Potential SQL injection detected"
            logger.warning(f"SafetyAgent: {reason}")
            return False, reason
        
        logger.info("SafetyAgent: SQL query validated successfully")
        return True, "Query is safe"
    
    def _check_injection_patterns(self, sql: str) -> bool:
        """
        Check for common SQL injection patterns.
        
        Args:
            sql: SQL query string
            
        Returns:
            True if suspicious patterns found
        """
        # Basic SQL injection patterns
        injection_patterns = [
            r";\s*DROP",
            r";\s*DELETE",
            r"'\s*OR\s*'1'\s*=\s*'1",
            r"--\s*",
            r"/\*.*\*/"
        ]
        
        sql_upper = sql.upper()
        for pattern in injection_patterns:
            if re.search(pattern, sql_upper):
                return True
        
        return False