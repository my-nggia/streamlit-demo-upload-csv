import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd

st.title("[DEMO: ONLINE RETAIL STORE] Upload CSV and Send Data to Google Sheets")
st.markdown("Author: my.ngngia@gmail.com")
st.markdown("GG Sheets: https://docs.google.com/spreadsheets/d/1swvLce5SGDxrZqsb-xFgevDgPQkFq-CHpSi2wYor-6o/edit?usp=sharing")

conn = st.connection("gsheets", type=GSheetsConnection)

# fetch
df = conn.read(worksheet="TransactionData", usecols=list(range(12)), ttl=5)

csv_file = st.file_uploader("Upload your CSV file", type=["csv"])

if csv_file is not None:
    # Đọc file CSV
    df = pd.read_csv(csv_file)
    st.write("Preview of your data:")
    st.dataframe(df)

    # Kiểm tra cột bắt buộc
    required_columns = [
        "Invoice", "StockCode", "Description", "Quantity", 
        "InvoiceDate", "Price", "Customer ID", "Country", 
        "Gender", "Location", "Age"
    ]
    if all(col in df.columns for col in required_columns):
        st.success("All required columns are present.")
    else:
        st.error("Your CSV is missing one or more required columns.")

def upload_to_gsheet(dataframe):
    pd_csv = pd.DataFrame(csv_file)
    updated_df = pd.concat([df, pd_csv], ignore_index=True)
        
    conn.update(worksheet='TransactionData', data=updated_df)

if st.button("Submit") and csv_file:
    try:
        upload_to_gsheet(df)
        st.success(f"Data successfully uploaded to the GG sheet")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# st.dataframe(df)