# Main Application Entry Point
# Initializes and runs the Agentic AI SQL system
"""
Main entry point for the Agentic SQL AI application.
"""

import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import json

from app.orchestrator.main_router import MainRouter
from app.core.logger import logger


def print_banner():
    """Print application banner."""
    banner = """
╔═══════════════════════════════════════════════╗
║   Agentic AI SQL Query Generator             ║
║   Natural Language → SQL → Results            ║
╚═══════════════════════════════════════════════╝
    """
    print(banner)


def print_results(result: dict):
    """
    Print query results in a formatted way.
    
    Args:
        result: Result dictionary from MainRouter
    """
    print("\n" + "="*60)
    
    if not result["success"]:
        print(f"❌ ERROR: {result['error']}")
        if result["sql"]:
            print(f"\n📝 Generated SQL:\n{result['sql']}")
        print("="*60)
        return
    
    print("✅ Query processed successfully!")
    print("\n📝 Generated SQL:")
    print(f"{result['sql']}\n")
    
    print("💡 Explanation:")
    print(f"{result['explanation']}\n")
    
    print(f"📊 Results ({result['row_count']} rows):")
    
    if result['data']:
        # Print first few rows
        display_limit = min(10, len(result['data']))
        for i, row in enumerate(result['data'][:display_limit], 1):
            print(f"\nRow {i}:")
            for key, value in row.items():
                print(f"  {key}: {value}")
        
        if result['row_count'] > display_limit:
            print(f"\n... and {result['row_count'] - display_limit} more rows")
    else:
        print("No results found.")
    
    print("="*60)


def main():
    """Main application loop."""
    print_banner()
    
    # Initialize the main router
    try:
        router = MainRouter()
        logger.info("Application initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        print(f"\n❌ Initialization Error: {e}")
        print("Please check your .env configuration and database connection.")
        sys.exit(1)
    
    print("\nEnter your natural language query (or 'quit' to exit):")
    
    while True:
        try:
            # Get user input
            print("\n" + "-"*60)
            user_query = input("🔍 Query: ").strip()
            
            if not user_query:
                continue
            
            if user_query.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋")
                break
            
            # Process query
            print("\n🤖 Processing your query...\n")
            result = router.process_query(user_query)
            
            # Display results
            print_results(result)
        
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"\n❌ Unexpected Error: {e}")


if __name__ == "__main__":
    main()