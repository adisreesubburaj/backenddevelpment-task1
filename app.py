from flask import Flask, request, jsonify, redirect
from pymongo import MongoClient
import string
import random

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["url_shortener"]
collection = db["urls"]

# Generate short code
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# ----------- SHORTEN ROUTE -----------
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.json
    long_url = data.get("long_url")

    if not long_url:
        return jsonify({"error": "long_url is required"}), 400

    short_code = generate_short_code()

    # Save to MongoDB
    collection.insert_one({
        "short_code": short_code,
        "long_url": long_url
    })

    return jsonify({
        "short_url": f"http://localhost:5000/{short_code}",
        "status": "success"
    })


@app.route('/<short_code>')
def redirect_to_long(short_code):
    entry = collection.find_one({"short_code": short_code})

    if entry:
        return redirect(entry["long_url"])   
    
    return jsonify({"error": "Short URL not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
