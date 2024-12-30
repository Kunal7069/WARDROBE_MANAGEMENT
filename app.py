from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import random
import re
from bson import ObjectId
app = Flask(__name__)
CORS(app)  
port=5000

MONGO_URI = "mongodb+srv://TEST:12345@mubustest.yfyj3.mongodb.net/investz?retryWrites=true&w=majority" 
DATABASE_NAME = "WARDROBE"              


# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

def serialize_document(doc):
    """Converts MongoDB document to a serializable format"""
    doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
    return doc


@app.route('/getColors', methods=['GET'])
def get_colors():
    try:
        collection=db['COLOURS_DATA']
        color_data = list(collection.find())  # Retrieve all documents, including the '_id'

        # Convert ObjectId to string for each document
        color_data = [serialize_document(doc) for doc in color_data]

        if color_data:
            return jsonify({
                "status": "success",
                "data": color_data  # Properly formatted data without BSON types
            })
        else:
            return jsonify({
                "status": "error",
                "message": "No data found"
            }), 404

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    

@app.route('/getOutfit', methods=['POST'])
def predict():
    try:
        # Get JSON data from request
        manual_input = request.json
        Outfit=manual_input.get('Outfit')
        Style=manual_input.get('Style')
        Watch=manual_input.get('Watch')
        Belt=manual_input.get('Belt')
        Shoes=manual_input.get('Shoes')
        preferred_shirt = manual_input.get('preferred_shirt',[])
        preferred_shoes = manual_input.get('preferred_shoes',[])
        if Outfit == 'FORMAL':
            preferred_pants = manual_input.get('preferred_pants',[])
        elif Outfit == 'CASUAL':
            preferred_pants = manual_input.get('preferred_jeans',[])
        
        
        if Outfit=='FORMAL':
            database=Outfit+'_'+Style
        else:
            database=Outfit
        collection=db[database]
        print("1")
        query = {
            "outfit_input": {"$regex": f"^{Outfit}$", "$options": "i"},
            "style_input": {"$regex": f"^{Style}$", "$options": "i"},
            "watch_input": {"$regex": f"^{Watch}$", "$options": "i"},
            "belt_input": {"$regex": f"^{Belt}$", "$options": "i"},
            "shoes_input": {"$regex": f"^{Shoes}$", "$options": "i"}
        }
        print("2")
        # Add case-insensitive filters for preferred shirt and pants colors
        if len(preferred_shirt)>0:
            query["shirt_output"] = {"$in": [re.compile(f"^{color}$", re.IGNORECASE) for color in preferred_shirt]}
        if len(preferred_pants)>0:
            query["pant_output"] = {"$in": [re.compile(f"^{color}$", re.IGNORECASE) for color in preferred_pants]}
        if len(preferred_shoes)>0:
            query["shoes_output"] = {"$in": [re.compile(f"^{color}$", re.IGNORECASE) for color in preferred_shoes]}


        # Query the database
        matched_entries = list(collection.find(query, {"_id": 0})) 
        print("3")
        if not matched_entries:
            return jsonify({
                "status": "success",
                "message": "No matching entries found.",
                "data": []
            })
        
        processed_data = []
        for entry in matched_entries:
            processed_entry = {}
            for key, value in entry.items():
                if key.endswith('_output'):
                    new_key = key.replace('_output', '')  
                    processed_entry[new_key] = value
            processed_data.append(processed_entry)
        if Outfit == 'CASUAL':
            for entry in processed_data:
                if 'pant' in entry:
                    entry['jeans'] = entry.pop('pant')
        for i in processed_data:
            i["shoes"] = f"{Outfit}_{i['shoes']}"
        result_1=[]    
        if Style=='NO' or Style=='QUIRKY':
            for item in processed_data:
                 if item["belt"] == "BLACK":
                    new_item = item.copy()
                    new_item["belt"] = "BROWN"
                    result_1.append(new_item)
                 elif item["belt"] == "BROWN":
                    new_item = item.copy()
                    new_item["belt"] = "BLACK"
                    result_1.append(new_item)
        if Style=='PROFESSIONAL' or Style=='MINIMAL':
            for i in processed_data:
                if i['belt']=="BROWN":
                    i['belt']="BLACK"
            
        combine_data=processed_data+result_1
        return jsonify({
            "data": combine_data
        })

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
