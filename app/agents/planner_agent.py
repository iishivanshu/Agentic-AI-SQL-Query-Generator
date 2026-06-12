# Planner Agent
# Responsible for planning query execution strategy
"""
Planner Agent - Creates logical query execution plan.
"""

from typing import Dict, Any

from app.core.logger import logger


class PlannerAgent:
    """Agent responsible for creating query execution plans."""
    
    def create_plan(self, user_query: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a logical plan for query execution.
        
        Args:
            user_query: Natural language query from user
            schema: Database schema information
            
        Returns:
            Query execution plan
        """
        logger.info("PlannerAgent: Creating query plan")
        
        # Simple rule-based planning
        plan = {
            "query_type": self._identify_query_type(user_query),
            "tables_mentioned": self._extract_table_references(user_query, schema),
            "user_intent": user_query,
            "requires_joins": self._check_join_requirement(user_query)
        }
        
        logger.info(f"PlannerAgent: Plan created - Type: {plan['query_type']}")
        return plan
    
    def _identify_query_type(self, query: str) -> str:
        """Identify the type of query based on keywords."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["count", "how many", "number of"]):
            return "COUNT"
        elif any(word in query_lower for word in ["average", "avg", "mean"]):
            return "AGGREGATE"
        elif any(word in query_lower for word in ["list", "show", "get", "find", "select"]):
            return "SELECT"
        else:
            return "SELECT"
    
    def _extract_table_references(self, query: str, schema: Dict[str, Any]) -> list:
        """Extract potential table references from query."""
        query_lower = query.lower()
        mentioned_tables = []
        
        for table_name in schema.keys():
            if table_name.lower() in query_lower:
                mentioned_tables.append(table_name)
        
        return mentioned_tables
    
    def _check_join_requirement(self, query: str) -> bool:
        """Check if query likely requires joins."""
        join_indicators = ["and", "with", "from multiple", "across"]
        query_lower = query.lower()
        return any(indicator in query_lower for indicator in join_indicators)