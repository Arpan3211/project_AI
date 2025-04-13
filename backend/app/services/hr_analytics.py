import os
import sqlite3
import re
from typing import Dict, Any, List, Optional
from collections import deque
import time

# Handle imports for both direct and package execution
try:
    from app.core.config import settings
    from app.services.hr_db import hr_db
except ImportError:
    from backend.app.core.config import settings
    from backend.app.services.hr_db import hr_db

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize LangChain components if available
try:
    from langchain_community.utilities import SQLDatabase
    from langchain_openai import AzureChatOpenAI
    from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
    from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
    from langchain_core.messages import HumanMessage, SystemMessage

    # Database Configuration
    DATABASE_URI = settings.HR_DATABASE_URL

    # Initialize database connection
    try:
        db = SQLDatabase.from_uri(DATABASE_URI)
        print("Using LangChain SQLDatabase for HR Analytics")
        using_langchain = True

        # Initialize query prompt template
        system_template = """You are a SQL expert. Given an input question and conversation history, create a syntactically correct {dialect} query to run.
always limit your query to at most {top_k} results using the LIMIT clause.
Never query for all columns. Only ask for the few relevant columns given the question.
Pay attention to use only the column names that you can see in the schema description.
IMPORTANT RULES:
1. For textual columns (e.g., Employee Name, Manager Name), ALWAYS use the LIKE operator with wildcard '%' for partial matches
2. Make textual searches case-insensitive using LOWER() function on both column and value
3. Example: SELECT * FROM table WHERE LOWER(Employee_Name) LIKE LOWER('%john%')
4. Use CAST instead of CONVERT for data type conversions
5. Use LIMIT clause for result limiting
6. Prioritize partial matches over exact matches for textual data
7. For numerical comparisons, use appropriate mathematical operators (=, >, <, etc.)
8. Consider previous conversation context when interpreting the current question
9. Step 1: Count Total Attrited Employees
Identify the total number of employees who have left the organization (attrited) using the sum(Overall_Inactive) column, match the condition overall_inactive = 1
Apply all user-specified filters, such as:Department. Location, Band, Process, Gender, Month, Year
If no filters are provided, Consider all months of the year 2024.


Step 2: Calculate Total Headcount
Determine the total headcount using the sum(Count) column.
Apply the same user-defined filters as in Step 1.

Step 3: Calculate Attrition Rate
Use the formula:
Attrition Percentage =
(Total Attrited Employees divided by Total Headcount) multiplied by 100.

This gives the percentage of employees who have left the organization relative to the total headcount.

For month-on-month calculations:
Compute the attrition rate for each month sequentially, Ensure all filters provided by the user are applied without omission.
If no specific month or year is provided, perform the calculation for each month in sequence.

Step 4: Handle Missing Inputs
If any filter is missing (e.g., specific month or year), default to considering all months in 2024 and include all entities for unspecified filters.
Ensure no data is excluded unintentionally.
Step 5: Return Results
Return the following:
Attrition Rate (as a percentage).
Total Attrited Employees (from Step 1).
Total Headcount (from Step 2).
Ensure the results are aligned with the user-defined filters.

Key Notes
Ensure all filters provided by the user are applied without omission.
If no filters are provided, consider the default scenario (all months of 2024 and all entities).
The calculation should be transparent and include all relevant data.
Do not hide any sensitive data.

CONVERSATION HISTORY:
{conversation_history}
AVAILABLE TABLES:
{table_info}
QUESTION: {input}"""

        query_prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_template)
        ])
    except Exception as e:
        print(f"Error connecting to HR database with LangChain: {str(e)}")
        db = hr_db
        using_langchain = False
        query_prompt_template = None
except ImportError:
    print("LangChain not available. Using custom database implementation.")
    db = hr_db
    using_langchain = False
    query_prompt_template = None

# Define HR database columns
COLUMNS = {
    "Month", "Date", "Month&Year", "Year", "Count", "Emp_ID", "Employee_Name",
    "Date_Of_Birth", "Age", "Gender", "Date_Of_Joining", "Band", "Designation",
    "Process", "Voice/Non_Voice", "Account_Name", "Domain", "Department",
    "Manager", "Functional_Head", "Location", "Sub_Location", "Country",
    "Date_of_Resignation", "Last_Working_Day", "Date_of_intimation_of_attrition",
    "Reason", "Voluntary/Involuntary", "NASCOM_Attrition_Analysis", "New_Country",
    "Active_Count", "New_Hire", "Opening_HC", "Overall_Inactive_Count",
    "Inactive_Count", "Age_Group", "Tenure_bucket"
}

# Initialize LLM if API keys are available, otherwise use mock LLM
try:
    if settings.API_KEY and settings.AZURE_OPENAI_ENDPOINT:
        llm = AzureChatOpenAI(
            openai_api_version="2024-02-01",
            azure_deployment="gpt-4o",
            model_name="gpt-4o",
            api_key=settings.API_KEY,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            temperature=0
        )
        print("Using Azure OpenAI for HR Analytics")
    else:
        print("API keys not found. Using mock LLM for HR Analytics.")
        llm = None
except Exception as e:
    print(f"Error initializing LLM: {str(e)}")
    llm = None

# Query Prompt Template with Conversation Context
system_template = """You are a SQL expert. Given an input question and conversation history, create a syntactically correct {dialect} query to run.
always limit your query to at most {top_k} results using the LIMIT clause.
Never query for all columns. Only ask for the few relevant columns given the question.
Pay attention to use only the column names that you can see in the schema description.
IMPORTANT RULES:
1. For textual columns (e.g., Employee Name, Manager Name), ALWAYS use the LIKE operator with wildcard '%' for partial matches
2. Make textual searches case-insensitive using LOWER() function on both column and value
3. Example: SELECT * FROM table WHERE LOWER(Employee_Name) LIKE LOWER('%john%')
4. Use CAST instead of CONVERT for data type conversions
5. Use LIMIT clause for result limiting
6. Prioritize partial matches over exact matches for textual data
7. For numerical comparisons, use appropriate mathematical operators (=, >, <, etc.)
8. Consider previous conversation context when interpreting the current question
9. Step 1: Count Total Attrited Employees
Identify the total number of employees who have left the organization (attrited) using the sum(Overall_Inactive) column, match the condition overall_inactive = 1
Apply all user-specified filters, such as:Department. Location, Band, Process, Gender, Month, Year
If no filters are provided, Consider all months of the year 2024.


Step 2: Calculate Total Headcount
Determine the total headcount using the sum(Count) column.
Apply the same user-defined filters as in Step 1.

Step 3: Calculate Attrition Rate
Use the formula:
Attrition Percentage =
(Total Attrited Employees divided by Total Headcount) multiplied by 100.

This gives the percentage of employees who have left the organization relative to the total headcount.

For month-on-month calculations:
Compute the attrition rate for each month sequentially, Ensure all filters provided by the user are applied without omission.
If no specific month or year is provided, perform the calculation for each month in sequence.

Step 4: Handle Missing Inputs
If any filter is missing (e.g., specific month or year), default to considering all months in 2024 and include all entities for unspecified filters.
Ensure no data is excluded unintentionally.
Step 5: Return Results
Return the following:
Attrition Rate (as a percentage).
Total Attrited Employees (from Step 1).
Total Headcount (from Step 2).
Ensure the results are aligned with the user-defined filters.

Key Notes
Ensure all filters provided by the user are applied without omission.
If no filters are provided, consider the default scenario (all months of 2024 and all entities).
The calculation should be transparent and include all relevant data.
Do not hide any sensitive data.

CONVERSATION HISTORY:
{conversation_history}
AVAILABLE TABLES:
{table_info}
QUESTION: {input}"""

query_prompt_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_template)
])

def process_query_with_feedback(question: str, conversation_history: str = "") -> Dict[str, str]:
    """Process HR analytics query with conversation context"""
    state = {"answer": "", "query": "", "result": "", "analysis": ""}

    # Check if database is initialized
    if db is None:
        state["answer"] = "Error: HR Analytics database is not properly initialized. Please check the configuration."
        return state

    try:
        # If LLM is available, use it to generate SQL query
        if llm is not None:
            prompt = query_prompt_template.invoke({
                "dialect": db.dialect,
                "top_k": 2000,
                "table_info": db.get_table_info(),
                "conversation_history": conversation_history,
                "input": question,
            })

            response = llm.invoke(prompt)
            content = response.content

            # Extract SQL query from response
            sql_match = re.search(r"```sql\n(.*?)\n```", content, re.DOTALL)
            state["query"] = sql_match.group(1).strip() if sql_match else content.strip()
        else:
            # If LLM is not available, use a rule-based approach to generate SQL
            state["query"] = generate_mock_sql_query(question, db)

        # Execute query if valid
        if state["query"] and not state["query"].startswith("Error"):
            try:
                if using_langchain:
                    # Use LangChain's QuerySQLDatabaseTool
                    tool = QuerySQLDatabaseTool(db=db)
                    state["result"] = tool.invoke(state["query"])
                else:
                    # Use our custom database implementation
                    try:
                        results = hr_db.execute_query(state["query"])
                        state["result"] = hr_db.format_results(results)
                    except Exception as db_error:
                        print(f"Error executing query with custom DB: {str(db_error)}")
                        state["result"] = f"Error executing query: {str(db_error)}"
            except Exception as query_error:
                print(f"Error executing SQL query: {str(query_error)}")
                state["result"] = f"Error executing query: {str(query_error)}"
                # Try a simpler query as fallback
                fallback_query = generate_fallback_query(question, db)
                if fallback_query:
                    try:
                        state["query"] = fallback_query
                        if using_langchain:
                            state["result"] = tool.invoke(fallback_query)
                        else:
                            results = hr_db.execute_query(fallback_query)
                            state["result"] = hr_db.format_results(results)
                    except:
                        state["result"] = "Could not execute query. Please try a simpler question."

        # Format answer
        if llm is not None:
            answer_prompt = f"""
            CONVERSATION HISTORY:
            {conversation_history}
            QUESTION: {question}
            SQL QUERY: {state['query']}
            SQL RESULT: {state['result']}
            Format your response with:
            1. For numerical results (counts, percentages, rates), create markdown tables
            2. Start with direct answer to the question
            3. Present main findings first
            4. Ensure that all data is displayed comprehensively without omitting any information.
            5. Use this table format for numerical data:
               | Metric | Value |
               |--------|-------|
               | ...    | ...   |

            6. For multi-row results, use:
               | Column1 | Column2 | ... |
               |---------|---------|-----|
               | ...     | ...     | ... |

            7. Keep text explanations concise
            8. Highlight key numbers in **bold**
            9. Maintain professional tone
            10. Add unit specifications (%/count/etc)
            11. Do not generate tables for questions unless they are related to attrition rate or count.
            """

            state["answer"] = llm.invoke(answer_prompt).content

            # Generate analysis
            analysis_prompt = f"""
            Perform detailed analysis of these results:
            {state['result']}
            Include:
            1. Trend identification
            2. Notable patterns/anomalies
            3. Key takeaways
            4. Professional business recommendations
            Structure analysis with:
            - Clear section headers
            - Bullet points for key findings
            - Highlight significant numbers
            - Relate to HR metrics context
            - Keep paragraphs short
            """

            state["analysis"] = llm.invoke(analysis_prompt).content
        else:
            # If LLM is not available, generate a simple formatted response
            state["answer"] = format_mock_response(question, state["result"])
            state["analysis"] = generate_mock_analysis(question, state["result"])

    except Exception as e:
        state["answer"] = f"Error: {str(e)}"
        print(f"Error processing HR analytics query: {str(e)}")

    return state

# Mock functions for when LLM is not available
def generate_mock_sql_query(question: str, db) -> str:
    """Generate a SQL query based on the question using rule-based approach"""
    question_lower = question.lower()

    # Get table info to understand the schema
    try:
        table_info = db.get_table_info()
    except:
        return "SELECT * FROM hr_data LIMIT 10"

    # Basic query templates
    if "attrition rate" in question_lower or "turnover rate" in question_lower:
        return """
        SELECT
            department,
            COUNT(CASE WHEN overall_inactive_count = 1 THEN 1 END) as attrited,
            COUNT(*) as total,
            ROUND(COUNT(CASE WHEN overall_inactive_count = 1 THEN 1 END) * 100.0 / COUNT(*), 2) as attrition_rate
        FROM hr_data
        GROUP BY department
        ORDER BY attrition_rate DESC
        LIMIT 10
        """

    if "headcount" in question_lower:
        if "department" in question_lower:
            return """
            SELECT
                department,
                COUNT(DISTINCT emp_id) as headcount
            FROM hr_data
            WHERE active_count = 1
            GROUP BY department
            ORDER BY headcount DESC
            LIMIT 10
            """
        else:
            return """
            SELECT
                COUNT(DISTINCT emp_id) as total_headcount
            FROM hr_data
            WHERE active_count = 1
            """

    if "gender" in question_lower and "distribution" in question_lower:
        return """
        SELECT
            gender,
            COUNT(DISTINCT emp_id) as count,
            ROUND(COUNT(DISTINCT emp_id) * 100.0 / (SELECT COUNT(DISTINCT emp_id) FROM hr_data), 2) as percentage
        FROM hr_data
        GROUP BY gender
        ORDER BY count DESC
        """

    if "age" in question_lower and "group" in question_lower:
        return """
        SELECT
            age_group,
            COUNT(DISTINCT emp_id) as count,
            ROUND(COUNT(DISTINCT emp_id) * 100.0 / (SELECT COUNT(DISTINCT emp_id) FROM hr_data), 2) as percentage
        FROM hr_data
        GROUP BY age_group
        ORDER BY
            CASE
                WHEN age_group = '20-25' THEN 1
                WHEN age_group = '26-30' THEN 2
                WHEN age_group = '31-35' THEN 3
                WHEN age_group = '36-40' THEN 4
                WHEN age_group = '41-45' THEN 5
                WHEN age_group = '46-50' THEN 6
                WHEN age_group = '51+' THEN 7
            END
        """

    if "tenure" in question_lower or "years of service" in question_lower:
        return """
        SELECT
            tenure_bucket,
            COUNT(DISTINCT emp_id) as count,
            ROUND(COUNT(DISTINCT emp_id) * 100.0 / (SELECT COUNT(DISTINCT emp_id) FROM hr_data), 2) as percentage
        FROM hr_data
        GROUP BY tenure_bucket
        ORDER BY
            CASE
                WHEN tenure_bucket = '<1 year' THEN 1
                WHEN tenure_bucket = '1-2 years' THEN 2
                WHEN tenure_bucket = '3-5 years' THEN 3
                WHEN tenure_bucket = '6-10 years' THEN 4
                WHEN tenure_bucket = '10+ years' THEN 5
            END
        """

    if "location" in question_lower:
        return """
        SELECT
            location,
            COUNT(DISTINCT emp_id) as headcount,
            COUNT(CASE WHEN overall_inactive_count = 1 THEN 1 END) as attrited,
            ROUND(COUNT(CASE WHEN overall_inactive_count = 1 THEN 1 END) * 100.0 / COUNT(*), 2) as attrition_rate
        FROM hr_data
        GROUP BY location
        ORDER BY headcount DESC
        LIMIT 10
        """

    if "reason" in question_lower and ("leaving" in question_lower or "resignation" in question_lower or "attrition" in question_lower):
        return """
        SELECT
            reason,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM hr_data WHERE reason IS NOT NULL), 2) as percentage
        FROM hr_data
        WHERE reason IS NOT NULL
        GROUP BY reason
        ORDER BY count DESC
        LIMIT 10
        """

    # Default query if no specific pattern is matched
    return "SELECT * FROM hr_data LIMIT 10"

def generate_fallback_query(question: str, db) -> str:
    """Generate a simpler fallback query when the main query fails"""
    # Very simple fallback query that should work in most cases
    return "SELECT COUNT(*) as total_records FROM hr_data LIMIT 1"

def format_mock_response(question: str, result: str) -> str:
    """Format a response based on the question and query result without using LLM"""
    question_lower = question.lower()

    # Basic response template
    response = f"Here are the results for your query about '{question}':\n\n"

    # Try to parse the result into a more readable format
    try:
        # Clean up the result string
        result = result.strip()

        # Check if result is empty or an error
        if not result or "error" in result.lower():
            return "I couldn't find any data matching your query. Please try a different question."

        # Format based on question type
        if "attrition rate" in question_lower or "turnover rate" in question_lower:
            response += "### Attrition Rate Analysis\n\n"
            response += "| Department | Attrited | Total | Attrition Rate (%) |\n"
            response += "|------------|----------|-------|-------------------|\n"

            # Try to parse the result into rows
            lines = result.split('\n')
            for line in lines[1:]:  # Skip header
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 5:  # Assuming format: | department | attrited | total | attrition_rate |
                        response += f"| {parts[1].strip()} | {parts[2].strip()} | {parts[3].strip()} | **{parts[4].strip()}%** |\n"

        elif "headcount" in question_lower:
            if "department" in question_lower:
                response += "### Headcount by Department\n\n"
                response += "| Department | Headcount |\n"
                response += "|------------|-----------|\n"
            else:
                response += "### Total Headcount\n\n"
                response += "| Metric | Value |\n"
                response += "|--------|-------|\n"
                response += f"| Total Headcount | **{result.strip()}** |\n"

        elif "gender" in question_lower and "distribution" in question_lower:
            response += "### Gender Distribution\n\n"
            response += "| Gender | Count | Percentage (%) |\n"
            response += "|--------|-------|---------------|\n"

        elif "age" in question_lower and "group" in question_lower:
            response += "### Age Group Distribution\n\n"
            response += "| Age Group | Count | Percentage (%) |\n"
            response += "|-----------|-------|---------------|\n"

        elif "tenure" in question_lower or "years of service" in question_lower:
            response += "### Tenure Distribution\n\n"
            response += "| Tenure | Count | Percentage (%) |\n"
            response += "|--------|-------|---------------|\n"

        elif "location" in question_lower:
            response += "### Location Analysis\n\n"
            response += "| Location | Headcount | Attrited | Attrition Rate (%) |\n"
            response += "|----------|-----------|----------|-------------------|\n"

        elif "reason" in question_lower:
            response += "### Reasons for Leaving\n\n"
            response += "| Reason | Count | Percentage (%) |\n"
            response += "|--------|-------|---------------|\n"

        else:
            # Generic table format for other queries
            response += result

    except Exception as e:
        # If parsing fails, just return the raw result
        response += result

    return response

def generate_mock_analysis(question: str, result: str) -> str:
    """Generate a simple analysis of the results without using LLM"""
    question_lower = question.lower()

    analysis = "## Analysis\n\n"

    # Add some generic analysis based on question type
    if "attrition rate" in question_lower or "turnover rate" in question_lower:
        analysis += "### Key Findings\n\n"
        analysis += "* The data shows varying attrition rates across departments\n"
        analysis += "* Departments with higher attrition rates may require focused retention strategies\n"
        analysis += "* Consider investigating the root causes in departments with above-average attrition\n\n"

        analysis += "### Recommendations\n\n"
        analysis += "1. Conduct exit interviews to understand reasons for leaving\n"
        analysis += "2. Implement targeted retention programs for high-attrition departments\n"
        analysis += "3. Review compensation and benefits packages to remain competitive\n"

    elif "headcount" in question_lower:
        analysis += "### Key Findings\n\n"
        analysis += "* The headcount distribution provides insights into organizational structure\n"
        analysis += "* Some departments may be understaffed or overstaffed relative to their responsibilities\n\n"

        analysis += "### Recommendations\n\n"
        analysis += "1. Review resource allocation across departments\n"
        analysis += "2. Consider workforce planning to address any imbalances\n"
        analysis += "3. Align headcount with strategic business objectives\n"

    elif "gender" in question_lower:
        analysis += "### Key Findings\n\n"
        analysis += "* The gender distribution provides insights into workforce diversity\n"
        analysis += "* There may be opportunities to improve gender balance in certain areas\n\n"

        analysis += "### Recommendations\n\n"
        analysis += "1. Review recruitment and promotion practices for potential bias\n"
        analysis += "2. Implement diversity and inclusion initiatives\n"
        analysis += "3. Set targets for improving gender balance where needed\n"

    elif "age" in question_lower:
        analysis += "### Key Findings\n\n"
        analysis += "* The age distribution shows the generational makeup of the workforce\n"
        analysis += "* Different age groups may have different needs and expectations\n\n"

        analysis += "### Recommendations\n\n"
        analysis += "1. Develop age-inclusive policies and practices\n"
        analysis += "2. Consider mentorship programs to facilitate knowledge transfer\n"
        analysis += "3. Ensure benefits and development opportunities appeal to all age groups\n"

    else:
        analysis += "### Key Findings\n\n"
        analysis += "* The data provides valuable insights into workforce metrics\n"
        analysis += "* Further analysis may reveal additional patterns and trends\n\n"

        analysis += "### Recommendations\n\n"
        analysis += "1. Continue monitoring these metrics over time\n"
        analysis += "2. Compare results with industry benchmarks\n"
        analysis += "3. Use these insights to inform HR strategy and decision-making\n"

    return analysis

def format_conversation_history(history: List[Dict[str, str]]) -> str:
    """Format conversation history for the LLM prompt"""
    if not history:
        return ""

    formatted = []
    for msg in history:
        role = msg.get("role", "").upper()
        content = msg.get("content", "")
        formatted.append(f"{role}: {content}")

    return "\n".join(formatted)

def process_hr_analytics_query(query: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, str]:
    """Process HR analytics query and return response"""
    if conversation_history is None:
        conversation_history = []

    # Format conversation history
    formatted_history = format_conversation_history(conversation_history)

    # Process query
    response = process_query_with_feedback(query, formatted_history)

    return response
