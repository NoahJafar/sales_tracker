import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sales Tracker", layout="centered")
st.title("📦 Product Sales & Follow-Up Tracker")

# Initialize session state if not present
if "sales_data" not in st.session_state:
    st.session_state.sales_data = []

st.subheader("📝 New Sale Entry")

# Sale Entry Form
with st.form("sales_form"):
    date = st.date_input("Date", value=datetime.today())
    client_name = st.text_input("Client Name (Pharmacy/Doctor)")

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
            st.session_state.sales_data.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Client": client_name,
                **entry,
                "Notes": notes
            })
        st.success("Sale entry saved successfully!")

# Display Sales Log
st.subheader("📊 Sales Log")
if st.session_state.sales_data:
    df = pd.DataFrame(st.session_state.sales_data)
    st.dataframe(df)
else:
    st.info("No sales entries yet.")
