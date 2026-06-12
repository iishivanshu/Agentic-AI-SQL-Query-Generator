# Explanation Agent
# Responsible for explaining query results to users
"""
Explanation Agent - Generates human-readable explanations of SQL queries.
"""

from app.core.llm_client import GrokClient
from app.core.logger import logger


class ExplanationAgent:
    """Agent responsible for explaining SQL queries in simple language."""
    
    def __init__(self):
        """Initialize explanation agent with LLM client."""
        self.llm_client = GrokClient()
    
    def explain_sql(self, sql: str, user_query: str) -> str:
        """
        Generate a simple explanation of the SQL query.
        
        Args:
            sql: SQL query to explain
            user_query: Original user query
            
        Returns:
            Plain English explanation
        """
        logger.info("ExplanationAgent: Generating SQL explanation")
        
        prompt = self._build_explanation_prompt(sql, user_query)
        explanation = self.llm_client.send_prompt(prompt)
        
        logger.info("ExplanationAgent: Explanation generated")
        return explanation
    
    def _build_explanation_prompt(self, sql: str, user_query: str) -> str:
        """Build prompt for generating explanation."""
        prompt = f"""Explain the following SQL query in simple, non-technical language.

User's Original Question: {user_query}

SQL Query:
{sql}

Provide a brief, clear explanation (2-3 sentences) of what this SQL query does and how it answers the user's question.

Do not include technical jargon. Write as if explaining to someone without SQL knowledge.

Explanation:"""
        
        return prompt