from flask import Flask, request, jsonify
from flask_cors import CORS
from price_logic import get_price_range
from db import init_db, get_cached_price, save_price

app = Flask(__name__)
CORS(app)
init_db()

@app.route("/price", methods=["GET"])
def get_price():
    crop = request.args.get("crop")
    market = request.args.get("market")

    if not crop or not market:
        return jsonify({"error": "crop and market are required"}), 400

    crop = crop.lower().strip()
    market = market.lower().strip()

    cached = get_cached_price(crop, market)
    if cached:
        return jsonify(cached), 200

    try:
        result = get_price_range(crop, market)
    except FileNotFoundError as e:
        return jsonify({"error": f"Data file not found: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

    if not result:
        return jsonify({"error": f"No price data found for {crop} in {market}"}), 404

    save_price(crop, market, result)
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)
