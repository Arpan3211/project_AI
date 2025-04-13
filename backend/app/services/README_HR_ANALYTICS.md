# HR Analytics Module

This module integrates HR Analytics capabilities into the AI Chat application using Azure OpenAI and LangChain, with fallback options for development and testing.

## Features

- SQL-based HR data analysis
- Natural language queries for HR data
- Conversation context for follow-up questions
- Detailed analysis of HR metrics
- Integration with the existing chat system
- Fallback mode for development without API keys
- Demo data generation for testing

## Setup

1. Install the required dependencies:
   ```
   python install_hr_dependencies.py
   ```

2. Create the HR database and generate demo data:
   ```
   python generate_demo_hr_data.py
   ```

3. (Optional) For production use, create a `.env` file with your Azure OpenAI credentials:
   ```
   API_KEY=your_azure_openai_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-azure-openai-endpoint.openai.azure.com/
   ```

   Note: If you don't have API keys, the system will automatically use a fallback approach with pre-defined responses.

## Usage

The HR Analytics module is integrated with the existing chat system. Users can ask HR-related questions in the chat interface, and the system will automatically process them using the HR Analytics module.

### API Endpoints

- `POST /api/hr-analytics/query` - Process an HR analytics query with conversation history

### Example Queries

- "What is the attrition rate for the IT department in 2023?"
- "Show me the headcount by department"
- "What is the gender distribution in the marketing team?"
- "Which location has the highest attrition rate?"
- "Compare attrition rates between different age groups"

## Architecture

The HR Analytics module uses:

1. **LangChain** for orchestrating the AI components
2. **Azure OpenAI** for natural language processing
3. **SQLite** for storing HR data
4. **SQLDatabase** from LangChain for database access
5. **Conversation memory** for context-aware responses

## Development Mode vs. Production Mode

The HR Analytics module can operate in two modes:

1. **Development Mode** (No API Keys):
   - Uses a rule-based approach to generate SQL queries
   - Provides pre-defined responses and analysis
   - Works with the demo data
   - No external API calls required

2. **Production Mode** (With API Keys):
   - Uses Azure OpenAI for natural language understanding
   - Generates dynamic SQL queries based on user questions
   - Provides detailed, context-aware responses
   - Requires valid API keys in the `.env` file

## Troubleshooting

If you encounter issues:

1. Check that the HR database exists at `app/db/hrattri_new.db`
2. If using Production Mode, verify your Azure OpenAI credentials in the `.env` file
3. Make sure all dependencies are installed correctly
4. Check the logs for specific error messages
5. If you're getting database errors, try regenerating the demo data with `python generate_demo_hr_data.py`
