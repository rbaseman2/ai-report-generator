import streamlit as st
import pandas as pd
import openai

st.title("AI-Powered Client Report Generator")

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
prompt_type = st.selectbox("Select the type of report", ["Summary", "Proposal", "Client Letter"])
openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")

def read_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    else:
        raise ValueError("Unsupported file type")

def generate_report(prompt, api_key):
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful AI that writes professional business documents."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=800
    )
    return response.choices[0].message.content

if uploaded_file is not None:
    df = read_file(uploaded_file)

    # Create prompt with business context
    prompt = (
        f"Generate a professional {prompt_type.lower()} from the following business data.\n\n"
        f"{df.to_string(index=False)}\n\n"
        "Make sure the report is clear, concise, and appropriate for business clients."
    )

    if st.button("Generate Report"):
        if not openai_api_key:
            st.error("Please enter your OpenAI API key.")
        else:
            with st.spinner("Generating report..."):
                try:
                    content = generate_report(prompt, openai_api_key)
                    st.success("Report generated successfully:")
                    st.write(content)
                except Exception as e:
                    st.error(f"An error occurred: {e}")