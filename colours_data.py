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
pants_jeans_colors = [
    "BLACK",
    "WHITE",
    "BROWN",
    "KHAKI",
    "NAVY BLUE",
    "ASH",
    "ICE BLUE",
    "BEIGE",
    "CREAM",
    "GREEN",
    "ORANGE",
    "YELLOW",
    "LIGHT PINK",
    "MAROON",
    "PURPLE",
    "GREY",
    "DARK BLUE",
    "LIGHT BLUE",
    "OLIVE",
]
# Document to insert
document = {
    "name": "pants_jeans_colors",
    "colors": pants_jeans_colors
}

# Insert the document into the collection
result = collection.insert_one(document)

# Print the result
print(f"Document inserted with ID: {result.inserted_id}")
