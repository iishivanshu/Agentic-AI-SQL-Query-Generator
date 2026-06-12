"""
Streamlit Frontend for Agentic AI SQL Query Generator
Clean, minimal, professional data-analytics dashboard.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Import backend orchestrator
from app.orchestrator.main_router import MainRouter


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Agentic AI SQL Query Generator",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Custom CSS - light, clean, corporate dashboard aesthetic
# ---------------------------------------------------------------------------
def inject_click_feedback():
    """Inject javascript to show click feedback for the first 4 seconds only."""
    import urllib.parse
    html_content = """
    <script>
    (function() {
        // Find and hide our own iframe container in the parent document
        const parentDoc = window.parent.document;
        const iframes = parentDoc.getElementsByTagName('iframe');
        for (let i = 0; i < iframes.length; i++) {
            try {
                if (iframes[i].contentWindow === window) {
                    const container = iframes[i].closest('.element-container');
                    if (container) {
                        container.style.display = 'none';
                        container.style.height = '0px';
                        container.style.margin = '0px';
                        container.style.padding = '0px';
                    }
                    break;
                }
            } catch (err) {
                // Ignore cross-origin frame access errors
            }
        }

        if (window.parent.__clickFeedbackInitialized) {
            return;
        }
        window.parent.__clickFeedbackInitialized = true;
        
        const style = parentDoc.createElement('style');
        style.id = 'click-feedback-style';
        style.innerHTML = `
            .click-feedback-ripple {
                position: fixed;
                border-radius: 50%;
                background: rgba(26, 115, 232, 0.4);
                pointer-events: none;
                transform: translate(-50%, -50%) scale(0);
                animation: click-ripple-anim 0.6s ease-out;
                z-index: 999999;
            }
            @keyframes click-ripple-anim {
                to {
                    transform: translate(-50% , -50%) scale(1);
                    opacity: 0;
                }
            }
        `;
        parentDoc.head.appendChild(style);
        
        parentDoc.addEventListener('click', function(e) {
            const elapsed = window.parent.performance.now();
            if (elapsed <= 4000) {
                const ripple = parentDoc.createElement('div');
                ripple.className = 'click-feedback-ripple';
                const size = 60;
                ripple.style.width = size + 'px';
                ripple.style.height = size + 'px';
                ripple.style.left = e.clientX + 'px';
                ripple.style.top = e.clientY + 'px';
                parentDoc.body.appendChild(ripple);
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            }
        });
    })();
    </script>
    """
    encoded_html = urllib.parse.quote(html_content)
    st.iframe(
        src=f"data:text/html;charset=utf-8,{encoded_html}",
        height=1,
    )

def inject_custom_css():
    """Inject custom CSS for a clean, minimal, professional look."""
    st.markdown(
        """
    <style>
    /* ---------- Google Font ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ---------- Global ---------- */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* ---------- Main background ---------- */
    [data-testid="stAppViewContainer"] {
        background-color: #f8f9fb;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e8eaed;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li {
        color: #5f6368;
        font-size: 0.88rem;
    }
    [data-testid="stSidebar"] h3 {
        color: #202124;
        font-size: 0.95rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        margin-bottom: 0.4rem;
    }

    /* ---------- Metric cards ---------- */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e8eaed;
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    [data-testid="stMetricValue"] {
        font-weight: 700;
        font-size: 1.5rem !important;
        color: #202124 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #80868b !important;
        font-weight: 500;
        font-size: 0.78rem !important;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }

    /* ---------- Primary button ---------- */
    .stButton > button {
        background-color: #1a73e8;
        color: #ffffff !important;
        border: none;
        border-radius: 8px;
        padding: 0.55rem 1.3rem;
        font-weight: 600;
        font-size: 0.88rem;
        transition: background-color 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 1px 3px rgba(26,115,232,0.15);
    }
    .stButton > button:hover {
        background-color: #1765cc;
        box-shadow: 0 2px 8px rgba(26,115,232,0.22);
        color: #ffffff !important;
    }
    .stButton > button:active {
        background-color: #1558b0;
    }

    /* ---------- Download button ---------- */
    .stDownloadButton > button {
        background-color: #ffffff;
        color: #1a73e8 !important;
        border: 1.5px solid #1a73e8;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.88rem;
        transition: all 0.2s ease;
    }
    .stDownloadButton > button:hover {
        background-color: #e8f0fe;
        color: #1a73e8 !important;
    }

    /* ---------- Text area ---------- */
    .stTextArea textarea {
        background-color: #ffffff !important;
        border: 1.5px solid #dadce0 !important;
        border-radius: 8px !important;
        color: #202124 !important;
        font-size: 0.95rem !important;
        padding: 12px 14px !important;
        transition: border-color 0.2s ease;
    }
    .stTextArea textarea::placeholder {
        color: #9aa0a6 !important;
    }
    .stTextArea textarea:focus {
        border-color: #1a73e8 !important;
        box-shadow: 0 0 0 2px rgba(26,115,232,0.12) !important;
    }

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 2px solid #e8eaed;
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 0;
        padding: 10px 20px;
        color: #5f6368;
        font-weight: 500;
        font-size: 0.88rem;
        border-bottom: 2px solid transparent;
        margin-bottom: -2px;
        transition: color 0.15s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #202124;
    }
    .stTabs [aria-selected="true"] {
        color: #1a73e8 !important;
        font-weight: 600;
        border-bottom: 2px solid #1a73e8 !important;
        background: transparent !important;
    }

    /* ---------- Dataframe ---------- */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e8eaed;
    }

    /* ---------- Code block ---------- */
    .stCodeBlock {
        border-radius: 8px !important;
    }

    /* ---------- Select box ---------- */
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 1.5px solid #dadce0 !important;
        border-radius: 8px !important;
        color: #202124 !important;
    }

    /* ---------- Expander ---------- */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #202124;
        font-size: 0.9rem;
    }

    /* ---------- Divider ---------- */
    hr {
        border-color: #e8eaed !important;
    }

    /* ---------- Success / Error / Warning alerts ---------- */
    .stAlert {
        border-radius: 8px;
    }

    /* ---------- Header area ---------- */
    .app-header {
        padding: 8px 0 4px 0;
    }
    .app-header h1 {
        color: #202124;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0 0 4px 0;
    }
    .app-header p {
        color: #5f6368;
        font-size: 1rem;
        margin: 0;
    }

    /* ---------- Sidebar history cards ---------- */
    .hist-card {
        background: #f8f9fb;
        border: 1px solid #e8eaed;
        border-radius: 8px;
        padding: 10px 12px;
        margin-bottom: 6px;
        font-size: 0.82rem;
        line-height: 1.45;
    }
    .hist-card .ts {
        color: #9aa0a6;
        font-size: 0.72rem;
    }
    .hist-card .qt {
        color: #3c4043;
    }
    .badge-ok {
        display: inline-block;
        background: #e6f4ea;
        color: #137333;
        border-radius: 4px;
        padding: 1px 7px;
        font-size: 0.68rem;
        font-weight: 600;
    }
    .badge-err {
        display: inline-block;
        background: #fce8e6;
        color: #c5221f;
        border-radius: 4px;
        padding: 1px 7px;
        font-size: 0.68rem;
        font-weight: 600;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
def initialize_session_state():
    """Initialize session state variables."""
    if "query_history" not in st.session_state:
        st.session_state.query_history = []
    if "router" not in st.session_state:
        st.session_state.router = None
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    if "user_query_input" not in st.session_state:
        st.session_state.user_query_input = ""


def add_to_history(query: str, result: dict):
    """Store query in session history (last 5)."""
    st.session_state.query_history.insert(
        0,
        {
            "timestamp": datetime.now(),
            "query": query,
            "success": result.get("success", False),
        },
    )
    st.session_state.query_history = st.session_state.query_history[:5]


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
def load_router():
    """Initialize the MainRouter."""
    try:
        if st.session_state.router is None:
            with st.spinner("🔄 Initializing AI agents..."):
                st.session_state.router = MainRouter()
        return st.session_state.router
    except Exception as e:
        st.error(f"❌ Failed to initialize the system: {str(e)}")
        st.error("⚙️ Please check your .env configuration and database connection.")
        st.stop()


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
def render_sidebar():
    """Minimal sidebar: about, features, query history."""
    with st.sidebar:
        st.markdown("### 📖 About")
        st.markdown(
            "A multi-agent AI system that converts natural language "
            "questions into validated SQL queries, executes them, "
            "and explains the results."
        )

        st.divider()

        st.markdown("### ✨ Features")
        st.markdown(
            """
- 🧠 Multi-agent pipeline (6 agents)
- 🔒 Safety validation (SELECT only)
- ⚡ Instant query execution
- 💬 Plain-English explanations
- 📊 Smart data visualization
- 📥 CSV export
"""
        )

        st.divider()

        st.markdown("### 🕘 Query History")
        if st.session_state.query_history:
            for item in st.session_state.query_history:
                badge = (
                    '<span class="badge-ok">SUCCESS</span>'
                    if item["success"]
                    else '<span class="badge-err">FAILED</span>'
                )
                ts = item["timestamp"].strftime("%H:%M:%S")
                text = (
                    item["query"][:55] + "..."
                    if len(item["query"]) > 55
                    else item["query"]
                )
                st.markdown(
                    f'<div class="hist-card">'
                    f'{badge} <span class="ts">{ts}</span><br/>'
                    f'<span class="qt">{text}</span>'
                    f"</div>",
                    unsafe_allow_html=True,
                )
        else:
            st.caption("🔍 No queries yet — try one!")


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
def render_header():
    """Simple, clean header."""
    st.markdown(
        """
    <div class="app-header">
        <h1>🤖 Agentic AI SQL Query Generator</h1>
        <p>💡 Ask questions in plain English and get SQL results instantly</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.divider()


# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------
def set_query(query):
    """Callback to set the query in session state."""
    st.session_state.user_query_input = query

def clear_query():
    """Callback to clear the query in session state."""
    st.session_state.user_query_input = ""
    st.session_state.last_result = None

def render_input_section():
    """Query input area with example queries."""

    with st.expander("💡 Example queries — click to try one", expanded=False):
        examples = [
            "Show me all customers from New York",
            "What is the average order value?",
            "List the top 10 products by sales",
            "How many orders were placed last month?",
            "Show total revenue per category",
            "Which customer has the most orders?",
        ]
        cols = st.columns(3)
        for i, q in enumerate(examples):
            cols[i % 3].button(
                q, 
                key=f"ex_{i}", 
                use_container_width=True, 
                on_click=set_query, 
                args=(q,)
            )

    user_query = st.text_area(
        "🔍 Your question",
        placeholder="e.g., Show me all customers who made purchases in the last 30 days...",
        height=110,
        key="user_query_input",
    )

    c1, c2, _ = st.columns([1, 0.7, 5])
    with c1:
        run_btn = st.button("🚀 Run Query", use_container_width=True)
    with c2:
        st.button(
            "🗑️ Clear", 
            use_container_width=True, 
            on_click=clear_query
        )

    return user_query, run_btn


# ---------------------------------------------------------------------------
# Processing
# ---------------------------------------------------------------------------
def process_query(router, user_query: str) -> dict:
    """Run the query through the backend pipeline."""
    with st.spinner("🤖 AI agents are processing your query..."):
        return router.process_query(user_query)


# ---------------------------------------------------------------------------
# KPIs
# ---------------------------------------------------------------------------
def render_kpis(df: pd.DataFrame, result: dict):
    """Metric cards: rows, columns, optional numeric summary."""
    cols = st.columns(3)
    with cols[0]:
        st.metric("📋 Total Rows", f"{result.get('row_count', len(df)):,}")
    with cols[1]:
        st.metric("📊 Columns", f"{len(df.columns)}")

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    with cols[2]:
        if numeric_cols:
            avg = df[numeric_cols[0]].mean()
            label = numeric_cols[0]
            if len(label) > 22:
                label = label[:22] + "..."
            st.metric(f"📈 Avg {label}", f"{avg:,.2f}" if not pd.isna(avg) else "-")
        else:
            uniq = df.iloc[:, 0].nunique() if len(df.columns) > 0 else 0
            st.metric("🔢 Unique Values", f"{uniq:,}")


# ---------------------------------------------------------------------------
# Tab - Results
# ---------------------------------------------------------------------------
def render_results_tab(df: pd.DataFrame, result: dict):
    """Dataframe display + CSV download."""
    st.dataframe(df, width="stretch", height=400)
    st.caption(
        f"Showing **{len(df)}** of **{result.get('row_count', len(df))}** rows"
    )

    csv = df.to_csv(index=False)
    st.download_button(
        "📥 Download CSV",
        data=csv,
        file_name=f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )


# ---------------------------------------------------------------------------
# Tab - Visualization
# ---------------------------------------------------------------------------
def _auto_chart_type(df: pd.DataFrame) -> str:
    """Pick a sensible default chart type from the data."""
    has_dt = any(pd.api.types.is_datetime64_any_dtype(df[c]) for c in df.columns)
    if has_dt:
        return "Line"
    num = df.select_dtypes(include=[np.number]).columns.tolist()
    cat = df.select_dtypes(include=["object", "str", "category"]).columns.tolist()
    if num and cat:
        return "Bar"
    return "Bar"


def render_visualization_tab(df: pd.DataFrame):
    """Clean charts with auto-detection + manual override."""
    if df.empty or len(df.columns) < 2:
        st.info("Not enough data to generate a chart.")
        return

    # Attempt datetime parsing
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                df[col] = pd.to_datetime(df[col])
            except (ValueError, TypeError):
                pass

    default = _auto_chart_type(df)

    left, right = st.columns([1, 3])
    with left:
        chart_type = st.selectbox(
            "Chart type",
            ["Bar", "Line", "Area"],
            index=["Bar", "Line", "Area"].index(default),
            key="chart_sel",
        )

    # Build chart-friendly dataframe
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "str", "category"]).columns.tolist()
    dt_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]

    chart_df = None
    if dt_cols and num_cols:
        chart_df = df.set_index(dt_cols[0])[num_cols]
    elif cat_cols and num_cols:
        chart_df = df.groupby(cat_cols[0])[num_cols[0]].sum().reset_index()
        chart_df = chart_df.set_index(cat_cols[0])
    elif num_cols:
        chart_df = df[num_cols]

    if chart_df is None or chart_df.empty:
        st.info("Cannot build a meaningful chart from this data.")
        return

    with right:
        if chart_type == "Bar":
            st.bar_chart(chart_df)
        elif chart_type == "Line":
            st.line_chart(chart_df)
        else:
            st.area_chart(chart_df)


# ---------------------------------------------------------------------------
# Tab - SQL
# ---------------------------------------------------------------------------
def render_sql_tab(result: dict):
    """Show generated SQL."""
    if result.get("sql"):
        st.code(result["sql"], language="sql")
        st.caption("💡 Use the copy icon in the top-right of the code block.")
    else:
        st.info("No SQL generated.")


# ---------------------------------------------------------------------------
# Tab - Explanation
# ---------------------------------------------------------------------------
def render_explanation_tab(result: dict):
    """Show the plain-English explanation."""
    if result.get("explanation"):
        st.markdown("#### 💬 What this query does")
        st.markdown(result["explanation"])
    else:
        st.info("No explanation available.")


# ---------------------------------------------------------------------------
# Full output section
# ---------------------------------------------------------------------------
def render_output(result: dict):
    """KPIs + tabbed output."""

    # Error path
    if not result.get("success"):
        st.error("❌ " + result.get("error", "An unknown error occurred."))
        if result.get("sql"):
            st.markdown("**🚫 Generated SQL (blocked)**")
            st.code(result["sql"], language="sql")
        return

    st.success("✅ Query executed successfully!")
    st.write("")

    data = result.get("data", [])
    df = pd.DataFrame(data) if data else pd.DataFrame()

    # KPIs
    render_kpis(df, result)
    st.write("")

    # Tabs
    t_results, t_viz, t_sql, t_explain = st.tabs(
        ["📋 Results", "📈 Visualization", "🛢️ SQL Query", "💬 Explanation"]
    )

    with t_results:
        if not df.empty:
            render_results_tab(df, result)
        else:
            st.info("The query returned no rows.")

    with t_viz:
        if not df.empty:
            render_visualization_tab(df.copy())
        else:
            st.info("No data available for visualization.")

    with t_sql:
        render_sql_tab(result)

    with t_explain:
        render_explanation_tab(result)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    """Application entry point."""
    initialize_session_state()
    inject_custom_css()
    inject_click_feedback()
    render_sidebar()
    render_header()

    router = load_router()
    user_query, run_btn = render_input_section()

    if run_btn:
        if not user_query or not user_query.strip():
            st.warning("⚠️ Please enter a query first.")
        else:
            result = process_query(router, user_query.strip())
            add_to_history(user_query.strip(), result)
            st.session_state.last_result = result

    if st.session_state.last_result is not None:
        st.divider()
        render_output(st.session_state.last_result)

    # Footer
    st.divider()
    st.markdown(
        "<p style='text-align:center; color:#9aa0a6; font-size:0.82rem;'>"
        "Built by Shivanshu using Streamlit &middot; Python &middot; MySQL &middot; Grok AI"
        "</p>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()