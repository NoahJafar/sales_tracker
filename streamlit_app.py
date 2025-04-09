import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime

# Google Sheets credentials
import json
import streamlit as st
from google.oauth2.service_account import Credentials

creds_dict = st.secrets["gcp_service_account"]
creds = Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets"])
client = gspread.authorize(creds)

# Load the spreadsheet and worksheets
spreadsheet = client.open_by_key("1Hlq0fKZtkCh0pNd_NhPtQt_GSnlWTQWy_54FGXLRcNw")
clients_sheet = spreadsheet.worksheet("Clients")
sales_sheet = spreadsheet.worksheet("SalesData")

# Get the client list from "Clients" sheet
clients_data = clients_sheet.get_all_values()
clients_list = [row[0] for row in clients_data[1:] if row]  # skip header

# Streamlit app setup
st.set_page_config(page_title="Sales Tracker", layout="centered")
st.title("📦 Product Sales Tracker")

st.subheader("📝 New Sale Entry")

# Sale Entry Form
with st.form("sales_form"):
    date = st.date_input("Date", value=datetime.today())
    client_name = st.selectbox("Client Name", clients_list)

    st.markdown("### Products Sold")
    product_entries = []
    for i in range(1, 6):
        col1, col2, col3 = st.columns(3)
        with col1:
            product = st.selectbox(f"Product {i}", ["", "Product 1", "Product 2", "Product 3"], key=f"product_{i}")
        with col2:
            quantity = st.number_input(f"Qty", min_value=0, step=1, key=f"qty_{i}")
        with col3:
            price = st.number_input(f"Price", min_value=0.0, step=0.1, key=f"price_{i}")

        if product and quantity > 0:
            product_entries.append({
                "Product": product,
                "Quantity": quantity,
                "Price": price,
                "Total": quantity * price
            })

    notes = st.text_area("Notes (Optional)")
    submit = st.form_submit_button("✅ Submit Entry")

    if submit and client_name and product_entries:
        for entry in product_entries:
            new_row = [
                date.strftime("%Y-%m-%d"),
                client_name,
                entry["Product"],
                entry["Quantity"],
                entry["Price"],
                entry["Total"],
                notes
            ]
            sales_sheet.append_row(new_row)
        st.success("Sale entry saved successfully!")

# Display Session Sales Log (optional)
st.subheader("📊 Recent Entries This Session")
if "sales_data" not in st.session_state:
    st.session_state.sales_data = []

if submit and client_name and product_entries:
    for entry in product_entries:
        st.session_state.sales_data.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Client": client_name,
            **entry,
            "Notes": notes
        })

if st.session_state.sales_data:
    df = pd.DataFrame(st.session_state.sales_data)
    st.dataframe(df)
else:
    st.info("No sales entries this session.")
