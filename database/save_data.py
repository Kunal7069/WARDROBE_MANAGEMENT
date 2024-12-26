import pandas as pd
from pymongo import MongoClient

# MongoDB connection URI and database name
uri = "mongodb+srv://TEST:12345@mubustest.yfyj3.mongodb.net/investz?retryWrites=true&w=majority"
db_name = "WARDROBE"
collection_name = "CASUAL"

def save_excel_to_mongo(file_path):
    try:
        # Step 1: Read Excel file using pandas
        data = pd.read_excel(file_path)

        # Convert the DataFrame to a list of dictionaries (rows)
        records = data.to_dict(orient="records")

        # Step 2: Connect to MongoDB
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]

        # Step 3: Insert the data into MongoDB
        result = collection.insert_many(records)
        print(f"{len(result.inserted_ids)} records inserted.")
    
    except Exception as e:
        print(f"Error: {e}")

# Example usage
file_path = 'combinations.xlsx'
save_excel_to_mongo(file_path)
