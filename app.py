from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import random
import re

app = Flask(__name__)
CORS(app)  
port=5000

MONGO_URI = "mongodb+srv://TEST:12345@mubustest.yfyj3.mongodb.net/investz?retryWrites=true&w=majority" 
DATABASE_NAME = "WARDROBE"              


# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]


@app.route('/getOutfit', methods=['POST'])
def predict():
    try:
        # Get JSON data from request
        manual_input = request.json
        Outfit=manual_input.get('Outfit')
        Style=manual_input.get('Style')
        Watch=manual_input.get('Watch')
        Belt=manual_input.get('Belt')
        preferred_shirt = manual_input.get('preferred_shirt', [])
        preferred_pants = manual_input.get('preferred_pants', [])
        
        if Belt=='YES':
            random_variable = random.randint(1, 10)
            if random_variable%2==0:
                Belt='BLACK'
            else:
                Belt='BROWN'
        if Outfit=='FORMAL':
            database=Outfit+'_'+Style
        else:
            database=Outfit
        collection=db[database]
        query = {
            "Outfit": {"$regex": f"^{Outfit}$", "$options": "i"},
            "Style": {"$regex": f"^{Style}$", "$options": "i"},
            "Watch": {"$regex": f"^{Watch}$", "$options": "i"},
            "Belt": {"$regex": f"^{Belt}$", "$options": "i"}
        }

        # Add case-insensitive filters for preferred shirt and pants colors
        if preferred_shirt:
            query["Shirt"] = {"$in": [re.compile(f"^{color}$", re.IGNORECASE) for color in preferred_shirt]}
        if preferred_pants:
            query["Pants"] = {"$in": [re.compile(f"^{color}$", re.IGNORECASE) for color in preferred_pants]}


        # Query the database
        matched_entries = list(collection.find(query, {"_id": 0})) 
        
        if not matched_entries:
            return jsonify({
                "status": "success",
                "message": "No matching entries found.",
                "data": []
            })
        for i in matched_entries:
            if i['Pants']=='BROWN':
                i['Belt']='BROWN'
            else:
                i['Belt']='BLACK'
        return jsonify({
            "data":matched_entries
        })
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": "An unexpected error occurred."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)