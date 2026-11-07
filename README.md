# Agentic AI SQL Query Generator

A production-style agentic system that converts natural language queries into SQL, validates them for safety, executes them, and provides explanations.

## 🏗️ Architecture

The system uses multiple specialized agents that collaborate to process queries:

1. **Schema Agent** - Fetches database structure
2. **Planner Agent** - Creates logical query plan
3. **SQL Generator Agent** - Generates SQL using Grok LLM
4. **Safety Agent** - Validates SQL for dangerous operations
5. **Execution Agent** - Runs safe queries on MySQL
6. **Explanation Agent** - Explains SQL in plain English

## 🚀 Features

- Natural language to SQL conversion
- Multi-agent collaboration
- Safety validation (blocks DROP, DELETE, UPDATE, etc.)
- Automatic schema introspection
- Plain English explanations
- Clean, modular architecture

## 📋 Prerequisites

- Python 3.10+
- MySQL database
- Grok API key (from X.AI)

## 🛠️ Installation

1. **Clone the repository**
```bash
   git clone https://github.com/iishivanshu/Agentic-AI-SQL-Query-Generator.git
   cd Agentic-AI-SQL-Query-Generator
```

2. **Install dependencies**
```bash
   pip install -r requirements.txt
```

3. **Configure environment variables**
   
   Edit the `.env` file with your credentials:
```bash
   GROK_API_KEY=your_actual_grok_api_key
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=your_database_name
   DB_PORT=3306
```

4. **Verify database connection**
   
   Ensure your MySQL database is running and accessible.

## 🎯 Usage

Run the application:
```bash
python -m app.main
```

### Example Queries
```
🔍 Query: Show me all customers from New York

🔍 Query: What is the average order value?

🔍 Query: List the top 10 products by sales

🔍 Query: How many orders were placed last month?
```

## 📁 Project Structure
```
Agentic-AI-SQL-Query-Generator/
├── app/
│   ├── agents/
│   │   ├── schema_agent.py          # Database schema retrieval
│   │   ├── planner_agent.py         # Query planning
│   │   ├── sql_generator_agent.py   # SQL generation via LLM
│   │   ├── safety_agent.py          # SQL validation
│   │   ├── execution_agent.py       # Query execution
│   │   └── explanation_agent.py     # Natural language explanation
│   ├── core/
│   │   ├── config.py                # Configuration management
│   │   ├── llm_client.py            # Grok API client
│   │   ├── database.py              # MySQL connection
│   │   └── logger.py                # Logging setup
│   ├── orchestrator/
│   │   └── main_router.py           # Agent orchestration
│   └── main.py                      # Application entry point
├── frontend/
│   └── streamlit_app.py             # Streamlit web interface
├── import_csv.py                    # Script to import weapons dataset
├── load_ev_market.py                # Script to load EV market dataset
├── setup_sample_db.py               # Interactive sample database setup
├── .env                             # Environment variables
├── requirements.txt                 # Python dependencies
└── README.md                        # Documentation
```

## 🔒 Safety Features

The Safety Agent blocks the following operations:
- DROP (tables/databases)
- DELETE (data deletion)
- UPDATE (data modification)
- ALTER (schema changes)
- TRUNCATE (table clearing)
- INSERT (data insertion)
- CREATE (object creation)
- GRANT/REVOKE (permission changes)

Only SELECT queries are allowed.

## 🔧 Configuration

All configuration is managed through environment variables in `.env`:

| Variable | Description | Example |
|----------|-------------|---------|
| GROK_API_KEY | Your Grok API key | xai-abc123... |
| DB_HOST | MySQL host | localhost |
| DB_USER | MySQL username | root |
| DB_PASSWORD | MySQL password | mypassword |
| DB_NAME | Database name | mydb |
| DB_PORT | MySQL port | 3306 |

## 🤖 How It Works

1. User enters a natural language query
2. **Schema Agent** retrieves database structure
3. **Planner Agent** analyzes the query and creates a plan
4. **SQL Generator Agent** uses Grok LLM to generate SQL
5. **Safety Agent** validates the SQL for dangerous operations
6. **Execution Agent** runs the query on MySQL (if safe)
7. **Explanation Agent** generates a plain English explanation
8. Results are displayed to the user

## 📝 Example Output
```
✅ Query processed successfully!

📝 Generated SQL:
SELECT * FROM customers WHERE city = 'New York' LIMIT 100

💡 Explanation:
This query retrieves all customer information for customers located in New York. 
It looks at the customers table and filters the results to show only those 
whose city is New York.

📊 Results (15 rows):
...
```

## 🐛 Troubleshooting

**Database Connection Issues:**
- Verify MySQL is running
- Check credentials in `.env`
- Ensure database exists

**Grok API Errors:**
- Verify API key is correct
- Check internet connection
- Ensure API quota is available

**Module Import Errors:**
- Run from project root: `python -m app.main`
- Verify all dependencies are installed

## 📄 License

This project is provided as-is for educational and commercial use.

## 🤝 Contributing

This is a production-style template. Feel free to extend with:
- Additional agents
- More sophisticated planning
- Query optimization
- Caching mechanisms
- Web interface
- API endpoints

---

**Built by Shivanshu Sharma using Python, MySQL, and Grok AI**