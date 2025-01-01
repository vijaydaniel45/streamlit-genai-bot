import os
import pandas as pd
import requests
import streamlit as st
import matplotlib.pyplot as plt
import io
import contextlib
import re

# Groq API settings
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = "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"

# Initialize session state for code persistence and response memory
if "extracted_code" not in st.session_state:
    st.session_state.extracted_code = ""
if "execution_output" not in st.session_state:
    st.session_state.execution_output = ""
if "generated_plot" not in st.session_state:
    st.session_state.generated_plot = None

def main():
    st.title("Welcome to Vijay's GenAI App")
    st.sidebar.header("Upload File")

    # File upload supporting various formats
    uploaded_file = st.sidebar.file_uploader("Upload your .csv, .txt, .log, .xlsx, or .xls file", type=["csv", "txt", "log", "xlsx", "xls"])

    # Model selection in sidebar
    model = st.sidebar.selectbox("Select Model", [
        "distil-whisper-large-v3-en",
        "gemma2-9b-it",
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama-guard-3-8b",
        "llama3-70b-8192",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "whisper-large-v3",
        "whisper-large-v3-turbo"
    ], index=2)  # default to "llama-3.3-70b-versatile"

    # Temperature slider in sidebar
    temperature = st.sidebar.slider("Select Temperature", 0.0, 2.0, 1.0)

    # Display the selected model and temperature
    st.sidebar.write(f"Selected Model: {model}")
    st.sidebar.write(f"Selected Temperature: {temperature}")

    # Display the text area for entering a prompt
    user_prompt = st.text_area("Enter your prompt for code generation (e.g., can you generate python script to get pie chart for getting DependentSiteCount by City? Here DependentSiteCount and City are the column names):")

    # Button to clear previous responses
    if st.sidebar.button("Clear Previous Responses"):
        clear_responses()

    if uploaded_file:
        # Save the uploaded file to the current directory
        save_uploaded_file(uploaded_file)

        try:
            # Handle file format and display data
            file_extension = uploaded_file.name.split(".")[-1].lower()
            if file_extension in ["xlsx", "xls"]:
                df = pd.read_excel(uploaded_file)
                st.write("### Uploaded Excel Data")
                st.dataframe(df)
            elif file_extension == "csv":
                df = pd.read_csv(uploaded_file)
                st.write("### Uploaded CSV Data")
                st.dataframe(df)
            elif file_extension in ["txt", "log"]:
                content = uploaded_file.read().decode("utf-8")
                st.write("### Uploaded Text/Log Data")
                st.text(content)
            else:
                st.error("Unsupported file format.")
                return

        except Exception as e:
            st.error(f"Error processing the file: {e}")

    else:
        st.info("Please upload a file or enter a general question.")

    # Always show the "Generate Code" button for both cases
    if st.button("Generate Response"):
        if user_prompt:
            st.info("Sending prompt to Groq API...")
            process_with_groq_api(user_prompt, uploaded_file, model, temperature)  # Pass model and temperature as arguments
        else:
            st.warning("Please enter a prompt to generate code.")

    # Display extracted code if available
    if st.session_state.extracted_code:
        st.write("### Extracted Code")
        st.code(st.session_state.extracted_code)

        # Add "Run Extracted Code" button
        if st.button("Click me to run the Extracted Code"):
            st.info("Running extracted code...")
            run_code(st.session_state.extracted_code)

        # Display execution output and plot if available
        if st.session_state.execution_output:
            st.write("### Output from Code Execution")
            st.text(st.session_state.execution_output)

        if st.session_state.generated_plot:
            st.write("### Generated Plot")
            st.image(st.session_state.generated_plot, caption="Generated Plot", use_container_width=True)

def save_uploaded_file(uploaded_file):
    """Save the uploaded file to the current directory."""
    try:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File saved as {uploaded_file.name}")
    except Exception as e:
        st.error(f"Error saving file: {e}")

def process_with_groq_api(user_prompt, uploaded_file=None, model="llama-3.3-70b-versatile", temperature=1.0):
    """Send user prompt to Groq API and extract and display the returned code."""
    try:
        if GROQ_API_KEY:
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            # Prepare the payload with the latest prompt, model, and temperature
            prompt = f"{user_prompt} from the uploaded file named {uploaded_file.name}" if uploaded_file else user_prompt
            payload = {
                "model": model,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}]
            }

            # Send the payload to the Groq API
            response = requests.post(GROQ_API_URL, json=payload, headers=headers)

            # Handle the response
            if response.status_code == 200:
                response_content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
                if response_content:
                    code = extract_code_from_response(response_content)
                    if code:
                        st.session_state.extracted_code = code
                    else:
                        st.error("No valid code was found in the response.")
                else:
                    st.error("No content was returned from Groq API.")
            else:
                st.error(f"Groq API Error: {response.text}")
        else:
            st.warning("Groq API key not provided. Skipping code generation.")
    except Exception as e:
        st.error(f"Error processing prompt: {e}")

def clear_responses():
    """Clear previously generated responses."""
    st.session_state.extracted_code = ""
    st.session_state.execution_output = ""
    st.session_state.generated_plot = None
    st.info("Previous responses cleared.")

def extract_code_from_response(response):
    """Extract the script from the response."""
    matches = re.findall(r"```([a-zA-Z]+)?\n(.*?)```", response, re.DOTALL)
    if matches:
        return matches[0][1].strip()
    return response.strip()

def run_code(code):
    """Run the extracted code."""
    try:
        captured_output = io.StringIO()
        with contextlib.redirect_stdout(captured_output):
            plt.close("all")
            exec(code, {"__name__": "__main__", "plt": plt})
        st.session_state.execution_output = captured_output.getvalue()

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        if buf.getbuffer().nbytes > 0:
            st.session_state.generated_plot = buf
    except Exception as e:
        st.error(f"Error executing the code: {e}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
