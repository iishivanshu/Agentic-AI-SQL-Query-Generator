# Main Router
# Orchestrates the flow between different agents
"""
Main Router - Orchestrates all agents to process user queries.
"""

from typing import Dict, Any

from app.agents.schema_agent import SchemaAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.sql_generator_agent import SQLGeneratorAgent
from app.agents.safety_agent import SafetyAgent
from app.agents.execution_agent import ExecutionAgent
from app.agents.explanation_agent import ExplanationAgent
from app.core.logger import logger


class MainRouter:
    """Central orchestrator for the agentic SQL system."""
    
    def __init__(self):
        """Initialize all agents."""
        self.schema_agent = SchemaAgent()
        self.planner_agent = PlannerAgent()
        self.sql_generator = SQLGeneratorAgent()
        self.safety_agent = SafetyAgent()
        self.execution_agent = ExecutionAgent()
        self.explanation_agent = ExplanationAgent()
    
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """
        Process user query through the agentic pipeline.
        
        Args:
            user_query: Natural language query from user
            
        Returns:
            Dictionary containing SQL, explanation, and data
        """
        logger.info(f"MainRouter: Processing query: '{user_query}'")
        
        try:
            # Step 1: Fetch database schema
            logger.info("Step 1: Fetching schema")
            schema = self.schema_agent.get_schema_info()
            schema_formatted = self.schema_agent.format_schema_for_llm(schema)
            
            # Step 2: Create query plan
            logger.info("Step 2: Creating plan")
            plan = self.planner_agent.create_plan(user_query, schema)
            
            # Step 3: Generate SQL
            logger.info("Step 3: Generating SQL")
            sql = self.sql_generator.generate_sql(user_query, schema_formatted, plan)
            
            # Step 4: Validate SQL safety
            logger.info("Step 4: Validating SQL safety")
            is_safe, safety_reason = self.safety_agent.validate_sql(sql)
            
            if not is_safe:
                logger.warning(f"MainRouter: Query blocked - {safety_reason}")
                return {
                    "success": False,
                    "error": safety_reason,
                    "sql": sql,
                    "explanation": None,
                    "data": []
                }
            
            # Step 5: Execute SQL
            logger.info("Step 5: Executing SQL")
            rows, columns = self.execution_agent.execute_sql(sql)
            formatted_data = self.execution_agent.format_results(rows, columns)
            
            # Step 6: Generate explanation
            logger.info("Step 6: Generating explanation")
            explanation = self.explanation_agent.explain_sql(sql, user_query)
            
            logger.info("MainRouter: Query processed successfully")
            
            return {
                "success": True,
                "sql": sql,
                "explanation": explanation,
                "data": formatted_data,
                "row_count": len(rows),
                "columns": columns
            }
        
        except Exception as e:
            logger.error(f"MainRouter: Error processing query - {e}")
            return {
                "success": False,
                "error": str(e),
                "sql": None,
                "explanation": None,
                "data": []
            }