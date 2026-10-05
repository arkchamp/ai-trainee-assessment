# ai-trainee-assessment
A Business Data Assistant that answers business questions from CSV data using natural language.

## Problem Understanding

The goal of this project is to make it easier to get information from business data. Instead of manually checking CSV files, users can ask questions in natural language and get answers quickly.

The assistant understands the user's question, looks at the available business data, and provides a relevant response.

## Approach

I started by loading the CSV files into Pandas DataFrames. When a user asks a question, the question is first sent to Gemini to understand the intent and extract the required information such as operation, city, customer type, product, or status.

The extracted intent is then used to perform the required calculations on the data. After getting the result, Gemini is used again to convert the output into a simple business-friendly response.

Finally, the response is shown to the user through a Streamlit web interface.

User
↓
Streamlit UI
↓
Question Input
↓
Gemini API
(Intent Detection)
↓
Business Logic
(Query Execution)
↓
+----> customers.csv
↓
+----> orders.csv
↓
+----> business_terms.csv
↓
Response Formatting
↓
Business Answer


## Technologies Used

### Python
Used as the main programming language for data processing and application logic.

### Pandas
Used to load CSV files, filter records, perform aggregations, and answer business queries.

### Gemini API
Used for intent detection and response generation from natural language questions.

### Streamlit
Used to build the web interface and deploy the application online using Streamlit Community Cloud.

### Python Dotenv
Used to securely load the Gemini API key from the .env file.

### CSV Files
Used as the data source for customers, orders, and business terms information.

### JSON
Used to parse and handle structured responses returned by the Gemini API.

## How I Used Cursor

Cursor was used as my primary code editor during development.

I only used it for basic training:

- Creating some basic files like streamlit_app.py, pandas_checking.py, random_data.csv
- Generating small code snippets and simple codes
- Understanding Python and Streamlit errors
- Learning and debugging parts of the application
- Making small code modifications during development

Most of the project logic, testing, debugging, and implementation decisions were done manually while building the Business Data Assistant and not with the Cursor.

## Problems Faced

During the project, I faced the following challenges:

- Converting natural language questions into structured business queries.
- Handling ambiguous questions and deciding when to make assumptions versus asking for clarification.
- Ensuring Gemini consistently returned valid JSON responses.
- Formatting query results into concise business-friendly answers.
- Managing API keys securely during local development and deployment.
- Hitting OpenAI API quota/usage limits while experimenting with different approaches then had to move to Gemini.
- Reaching Cursor AI usage limits at the start only and having to continue work manually.
- Deploying the application and ensuring it behaved the same way as the local version.
- OCI account verification issues while attempting cloud deployment.

## What I Learned

- How to use the Gemini LLM API for intent detection and response generation.
- How to work with CSV data using Pandas for filtering, aggregation, and analysis.
- How to convert query results into business-friendly responses.
- How to build and deploy a Streamlit application.
- How to manage API keys securely using environment variables and Streamlit Secrets.
- How to debug issues and improve the application through testing and iteration.

### While Learning Cursor

- How to install and set up Cursor.
- How to create and manage a project workspace.
- How to generate code using prompts.
- How to create new files using Cursor.
- How to overlap existing file with AI assistance.
- How to use Cursor for Streamlit development.
- How to run Python applications from the terminal.

### Git & GitHub

- Creating and managing Git repositories.
- Using Git for version control.
- Making meaningful commits during development.
- Pushing code to GitHub.
- Deploying a GitHub repository using Streamlit Community Cloud.

## Improvements

Given more time, I would like to:

- Support customer-specific queries such as revenue from a particular customer.
- Support more business questions and filtering options.
- Add charts and visualizations for better data insights.
- Improve intent detection to handle more variations of user questions.
- Add conversation history for previous questions and answers.
- Connect the application to a database instead of CSV files.
- Improve error handling and user feedback messages.
- Deploy the application on OCI in addition to Streamlit Community Cloud.

## Features
- Ask business questions in plain English
- Uses Gemini API for intent detection
- Retrieves data from CSV files
- Generates business-friendly responses
- Handles ambiguous questions with assumption and clarification prompts
- Streamlit-based web interface

## Dataset
The application uses the following datasets:
- customers.csv
- orders.csv
- business_terms.csv (for business terms and their meanings)

## Installation

1. Clone the repository
```bash
git clone https://github.com/arkchamp/ai-trainee-assessment.git
cd ai-trainee-assessment
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create a .env file
```env
GEMINI_API_KEY=your_api_key_here
```

## Running the Application
Start the Streamlit application:
```bash
streamlit run app.py
```

The application will be available at:
```text
http://localhost:8501
```

## Example Questions
- What are our total sales?
- Who are our top 5 customers?
- How much revenue came from Mumbai?
- What is the value of Open Orders?
- Which market performed best?

## Project Structure
```text
ai-trainee-assessment/
│
├── data/
│   ├── customers.csv
│   ├── orders.csv
│   └── business_terms.csv
│
├── app.py
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

## Deployment
The application is deployed using Streamlit Community Cloud.

Deployment Link:
https://ai-trainee-assessment.streamlit.app/

GitHub Repository:
https://github.com/arkchamp/ai-trainee-assessment

