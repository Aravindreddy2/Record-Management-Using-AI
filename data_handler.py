import pandas as pd
import os
import tempfile

DATABASE_PATH = "database.csv"

# Initialize the database file if it does not exist
def initialize_database():
    if not os.path.exists(DATABASE_PATH):
        df = pd.DataFrame(columns=["ID", "Title", "Description", "Category", "Created", "Modified"])
        df.to_csv(DATABASE_PATH, index=False)

# Save data to the CSV safely using a temporary file
def save_dataframe(df):
    # Create a temporary file without holding it open
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.csv')
    temp_file_path = temp_file.name  # Save the path to use later
    temp_file.close()  # Close the file to release the handle

    try:
        # Write to the temporary file
        df.to_csv(temp_file_path, index=False)
        # Replace the original file with the temporary file
        os.replace(temp_file_path, DATABASE_PATH)
    finally:
        # Ensure that if any error occurs, the temp file is cleaned up
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# Add a record, ensuring no duplicate IDs
def add_record(record):
    initialize_database()
    df = pd.read_csv(DATABASE_PATH)
    df["ID"] = df["ID"].astype(str)
    record_id = str(record["ID"])

    # Check if the ID already exists
    if record_id in df["ID"].values:
        print(f"Record with ID {record_id} already exists. Duplicate IDs are not allowed.")
        return False

    # Append the new record and save the DataFrame
    new_record_df = pd.DataFrame([record])
    df = pd.concat([df, new_record_df], ignore_index=True)
    save_dataframe(df)
    print(f"Record with ID {record_id} added successfully!")
    return True

# Read a record by ID
def read_record(record_id):
    initialize_database()
    df = pd.read_csv(DATABASE_PATH)
    df["ID"] = df["ID"].astype(str)
    record_id = str(record_id)
    return df[df["ID"] == record_id]

# Update a record by ID if it exists
def update_record(record_id, updated_data):
    initialize_database()
    df = pd.read_csv(DATABASE_PATH)
    df["ID"] = df["ID"].astype(str)
    record_id = str(record_id)
    
    if record_id in df["ID"].values:
        df.loc[df["ID"] == record_id, updated_data.keys()] = updated_data.values()
        save_dataframe(df)
        print(f"Record {record_id} updated successfully!")
        return True
    else:
        print(f"Record {record_id} not found for update.")
        return False

# Delete a record by ID if it exists
def delete_record(record_id):
    initialize_database()
    df = pd.read_csv(DATABASE_PATH)
    df["ID"] = df["ID"].astype(str)
    record_id = str(record_id)
    
    if record_id in df["ID"].values:
        df = df[df["ID"] != record_id]
        save_dataframe(df)
        print(f"Record {record_id} deleted successfully!")
        return True
    else:
        print(f"Record {record_id} not found for deletion.")
        return False
