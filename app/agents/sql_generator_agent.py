# SQL Generator Agent
# Responsible for generating SQL queries
"""
SQL Generator Agent - Uses LLM to generate SQL queries.
"""

from typing import Dict, Any

from app.core.llm_client import GrokClient
from app.core.logger import logger


class SQLGeneratorAgent:
    """Agent responsible for generating SQL using LLM."""
    
    def __init__(self):
        """Initialize SQL generator with LLM client."""
        self.llm_client = GrokClient()
    
    def generate_sql(
        self,
        user_query: str,
        schema_info: str,
        plan: Dict[str, Any]
    ) -> str:
        """
        Generate SQL query using Grok LLM.
        
        Args:
            user_query: Natural language query
            schema_info: Formatted schema information
            plan: Query execution plan
            
        Returns:
            Generated SQL query string
        """
        logger.info("SQLGeneratorAgent: Generating SQL query")
        
        prompt = self._build_prompt(user_query, schema_info, plan)
        response = self.llm_client.send_prompt(prompt)
        
        # Extract SQL from response
        sql = self._extract_sql(response)
        logger.info(f"SQLGeneratorAgent: SQL generated successfully")
        
        return sql
    
    def _build_prompt(
        self,
        user_query: str,
        schema_info: str,
        plan: Dict[str, Any]
    ) -> str:
        """Build the prompt for LLM."""
        prompt = f"""You are an expert SQL query generator.

{schema_info}

User Query: {user_query}

Query Type: {plan['query_type']}
Tables Mentioned: {', '.join(plan['tables_mentioned']) if plan['tables_mentioned'] else 'None specified'}

Generate a valid MySQL SELECT query to answer the user's question.

IMPORTANT RULES:
1. Return ONLY the SQL query, nothing else
2. Do not include explanations or markdown
3. Use only SELECT statements
4. Make sure the query is syntactically correct
5. Use appropriate JOINs if multiple tables are needed
6. Include appropriate WHERE clauses for filtering

SQL Query:"""
        
        return prompt
    
    def _extract_sql(self, response: str) -> str:
        """
        Extract SQL query from LLM response.
        
        Args:
            response: LLM response text
            
        Returns:
            Cleaned SQL query
        """
        # Remove markdown code blocks if present
        sql = response.strip()
        
        if "```sql" in sql:
            sql = sql.split("```sql")[1].split("```")[0].strip()
        elif "```" in sql:
            sql = sql.split("```")[1].split("```")[0].strip()
        
        # Remove any leading/trailing whitespace
        sql = sql.strip()
        
        # Remove semicolon if present at the end
        if sql.endswith(";"):
            sql = sql[:-1].strip()
        
        return sql