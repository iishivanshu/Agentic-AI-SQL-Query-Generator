# Contributing to Agentic AI SQL Query Generator

Thank you for your interest in contributing to the Agentic AI SQL Query Generator project! We welcome contributions, bug reports, and suggestions to help improve this multi-agent SQL assistant.

## How to Contribute

You can contribute in several ways:
- **Reporting bugs**: Open an issue describing the bug and steps to reproduce.
- **Suggesting features**: Propose new ideas, agents, or improvements to existing functionality.
- **Submitting code**: Fix an issue, add tests, or implement a new feature via a pull request.
- **Improving documentation**: Clarify instructions, add examples, or fix typos in the docs.

## Development Setup

1. **Fork and clone** the repository:
   ```bash
   git clone https://github.com/iishivanshu/Agentic-AI-SQL-Query-Generator.git
   cd Agentic-AI-SQL-Query-Generator
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file based on the example in the README with your MySQL and Grok API credentials.

5. **Run the application**:
   - CLI: `python -m app.main`
   - Streamlit Web App: `streamlit run frontend/streamlit_app.py`

## Code Style

To keep the codebase maintainable and clean:
- Follow [PEP 8](https://peps.python.org/pep-0008/) conventions for Python code.
- Write clear, descriptive variable and function names.
- Ensure all queries generated and processed adhere to security practices (only `SELECT` operations permitted by safety validation).
- Add comments and docstrings where appropriate to explain non-trivial agent logic.

## Submitting Changes

1. Create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes and test them locally to ensure agents execute properly and safety checks pass.
3. Commit your changes with clear, descriptive commit messages:
   ```bash
   git commit -m "feat: add query caching mechanism"
   ```
4. Push your branch to GitHub:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a Pull Request against the `main` branch with a summary of changes and testing steps.

## Reporting Issues

If you find a bug or security concern:
1. Check existing GitHub Issues to see if the problem has already been reported.
2. If not, open a new issue with:
   - A clear and descriptive title
   - Steps to reproduce the issue
   - Expected vs. actual behavior
   - Relevant error logs or screenshots (make sure to redact sensitive API keys or credentials)
