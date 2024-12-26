from pymongo import MongoClient

# MongoDB Atlas connection URI
MONGO_URI = "mongodb+srv://TEST:12345@mubustest.yfyj3.mongodb.net/investz?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)

# Select the database and collection
DATABASE_NAME = "WARDROBE"
COLLECTION_NAME = "COLOURS_DATA"
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Define the colors array
belt_colors = ["BLACK","BROWN"]

# Document to insert 
document = {
    "name": "belt_colors",
    "colors": belt_colors
}

# Insert the document into the collection
result = collection.insert_one(document)

# Print the result
print(f"Document inserted with ID: {result.inserted_id}")
