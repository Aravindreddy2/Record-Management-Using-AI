import streamlit as st
from data_handler import add_record, read_record, update_record, delete_record
from ai_models import classify_text
from datetime import datetime
import pandas as pd

st.title("Record Management System with AI")

# Sidebar Navigation
menu = ["Add Record", "View Records", "Update Record", "Delete Record"]
choice = st.sidebar.selectbox("Select an Action", menu)

# Initialize session state for category if not already set
if "category" not in st.session_state:
    st.session_state["category"] = None

if choice == "Add Record":
    st.subheader("Add a New Record")
    
    # Form to add a new record
    record_id = st.text_input("Record ID")
    title = st.text_input("Title")
    description = st.text_area("Description")
    created = datetime.now()
    
    # Classify button to determine category based on description
    if st.button("Classify"):
        st.session_state["category"] = classify_text(description)
        st.write(f"Predicted Category: {st.session_state['category']}")
        st.write(f"Session State Category: {st.session_state['category']}")  # Debug line

    # Only allow adding record if category is not None
    if st.button("Add Record"):
        if st.session_state["category"] is None:
            st.warning("Please classify the record before adding.")
        else:
            add_record({
                "ID": record_id,
                "Title": title,
                "Description": description,
                "Category": st.session_state["category"],
                "Created": created,
                "Modified": created
            })
            st.success(f"Record with ID {record_id} added successfully!")
            # Clear the category after adding the record
            st.session_state["category"] = None

elif choice == "View Records":
    st.subheader("View All Records")
    if st.button("Show All"):
        data = pd.read_csv("database.csv")
        st.dataframe(data)

elif choice == "Update Record":
    st.subheader("Update an Existing Record")
    
    record_id = st.text_input("Enter Record ID to Update")
    record = read_record(record_id)
    
    if not record.empty:
        title = st.text_input("Title", value=record["Title"].values[0])
        description = st.text_area("Description", value=record["Description"].values[0])
        
        if st.button("Update Record"):
            updated_data = {"Title": title, "Description": description, "Modified": datetime.now()}
            update_record(record_id, updated_data)
            st.success(f"Record {record_id} updated successfully!")
    else:
        st.warning("Record not found.")

elif choice == "Delete Record":
    st.subheader("Delete a Record")
    record_id = st.text_input("Enter Record ID to Delete")
    
    if st.button("Delete Record"):
        delete_record(record_id)
        st.success(f"Record {record_id} deleted successfully!")

