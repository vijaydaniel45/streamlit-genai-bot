# GenAI App for Code Generation and Execution

Welcome to the GenAI App built using Streamlit, which allows users to upload data files and generate code to analyze them. This app integrates with the Groq API to process user inputs and generate Python code, which can then be executed to visualize the results. The app supports various file types, including CSV, Excel, text, and log files.

## Features

- **File Upload**: Supports uploading CSV, Excel, text, and log files.
- **Model Selection**: Choose from a list of models for code generation.
- **Code Generation**: Input a prompt and generate Python code using the Groq API.
- **Code Execution**: Run the generated code and view the output.
- **Data Display**: View uploaded data in tabular format.
- **Plot Generation**: Automatically generate and display plots from the executed code.

## Requirements

- **Python 3.7+**
- **Streamlit**
- **Pandas**
- **Matplotlib**
- **Requests**

Install the required packages using:

```bash
pip install streamlit pandas matplotlib requests


Setup Instructions
Clone the Repository
Clone the repository to your local machine:


git clone https://github.com/vijaydaniel45/streamlit-genai-bot.git
cd genai-app

Configure API Keys
Set up the Groq API credentials by creating a secrets.toml file under the .streamlit/ directory. The file should include your API URL and API key.

Path: .streamlit/secrets.toml
Example secrets.toml:

[GROQ_API]
GROQ_API_URL = "your_groq_api_url"
GROQ_API_KEY = "your_groq_api_key"
Replace your_groq_api_url and your_groq_api_key with your actual Groq API credentials.

File Structure
Ensure the file structure is like this:


genai-app/
├── .streamlit/
│   └── secrets.toml
├── app.py
├── requirements.txt
└── README.md

Running the App Locally
Step 1: Install Dependencies
In the project directory, install the required dependencies:


pip install -r requirements.txt

Step 2: Run the Streamlit App
Once all dependencies are installed, start the app using:


streamlit run app.py
This will open the app in your default web browser.

Step 3: Access the App
Once the app is running, you can access it via your browser at the default Streamlit URL:


http://localhost:8501
You should now be able to upload files, input prompts for code generation, and execute the generated Python code to visualize the results.

How the App Works
1. File Upload
You can upload a CSV, Excel, text, or log file using the sidebar. The app will display the contents of the file in a readable format.

2. Model Selection
The app allows you to choose a model from the dropdown in the sidebar for code generation. Available models include:

gemma2-9b-it
llama-3.1-8b-instant
llama-guard-3-8b
llama3-70b-8192
llama3-8b-8192
mixtral-8x7b-32768


3. Input Prompt
Enter a prompt in the provided text area to specify what you want the app to do. For example, you can ask the app to generate a Python script for data analysis or create a plot from the uploaded data.

4. Generate Code
Once you enter the prompt, click the Generate Response button. The app will send the prompt to the Groq API and return Python code based on your input.

5. Execute Code
The app will display the generated code and provide an option to run it. Clicking the Run Extracted Code button will execute the code, and the output, along with any generated plots, will be shown on the page.

6. Clear Responses
If you want to clear all previous responses and start over, use the Clear Previous Responses button in the sidebar.

Example Use Case

Upload a File: Upload a CSV or Excel file containing data.
Generate Code: Enter a prompt like "Generate a pie chart for dependent site count by city" and click Generate Response.
Run Code: Execute the generated Python code and view the output, including any plots.

Contributing
We welcome contributions! Feel free to fork the repo, submit issues, or create pull requests.

Issues and Bug Reports
If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub Issues page.

License
This project is licensed under the MIT License. See the LICENSE file for more information.

