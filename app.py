from flask import Flask, request, jsonify # Used to get data input by user
import requests # Used for API requests
app = Flask(__name__)

items = [
  {
  "id": 1,
  "status": 1,
  "product": {
    "product_name": "Organic Almond Milk",
    "brands": "Silk",
    "ingredients_text": "Filtered water, almonds, cane sugar"
  }
  }
]
@app.route("/inventory", methods=["GET"])
def get_items():
  return jsonify(items), 200

@app.route("/inventory/<int:id>", methods=["GET"])
def get_item(id): 
  # Return the error message outside a loop otherwise it will check the first item then immediately return an error
  for item in items:
    if item["id"] == id:
      return jsonify(item), 200
  return jsonify({"message": "Item not found!"}), 404
    
@app.route("/inventory", methods=["POST"])
def add_item():
  data = request.get_json()
  if not data or "name" not in data:
    return jsonify({"message":"The key 'name' must be in your request"}), 400

  new_id = max((i["id"] for i in items), default=0)+ 1
  new_item = {"id": new_id}

  # Searches through the API using the name the user typed in and the &json=1 ensures data comes back in json format
  url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={data['name']}&json=1"
  try:
    response = requests.get(url, timeout=5)

    if response.status_code == 200 and "application/json" in response.headers.get("Content-Type", ""):
      try:
        product_data = response.json()

        if product_data.get("products"):
          product = product_data["products"][0]
          new_item.update({
              "status": 1,
              "message": "Product found via OpenFoodFacts",
              "product": {
                  "product_name": product.get("product_name", data["name"]),
                  "brands": product.get("brands", "Unknown"),
                  "ingredients_text": product.get("ingredients_text", "Not available")
              }
              })
        else:
          new_item.update({
            "status": 0,
            "message": "No product found in OpenFoodFacts",
            "product": {
              "product_name": data["name"],
              "brands": "Unknown",
              "ingredients_text": "Not available"
              }
              })
      except ValueError as e:
        app.logger.error(f"OpenFoodFacts JSON error: {e}")
        app.logger.error(f"Raw response text: {response.text}")
        new_item.update({
          "status": 0,
          "message": "Invalid JSON from OpenFoodFacts",
          "product": {
            "product_name": data["name"],
            "brands": "Unknown",
            "ingredients_text": "Not available"
            }
            })
      else:
            raise ValueError(f"Bad response: {response.status_code} {response.headers.get('Content-Type')}")

  except Exception as e:
        app.logger.error(f"OpenFoodFacts request error: {e}")
        new_item.update({
          "status": 0,
          "message": "OpenFoodFacts API unavailable",
          "product": {
            "product_name": data["name"],
            "brands": "Unknown",
            "ingredients_text": "Not available"
            }
            })

  print("New item being returned:", new_item, flush=True)

  items.append(new_item)
  return jsonify(new_item), 201

@app.route("/inventory/<int:id>", methods=["PATCH"])
def update_item(id):
  # Gets the data sent from the request if its json?
  data = request.get_json()
  # Next iterates to the next thing automatically
  # Loops through each item in the items array and checks if the id in the same as the one in the url, if not it returns None
  item = next((i for i in items if i["id"] == id), None)
  # If there is no item with that ID, it returns an error message
  if not item:
    return jsonify({"message": "Item not found!"}), 404
  # If no data was sent retunr error messages
  if not data or "name" not in data:
    return jsonify({"message":"The key 'name' must be in your request"}), 400

  item["product"]["product_name"] = data["name"] # Sets the products name to the name the user typed in
  return jsonify({"message": "Item updated", "item": item}), 200
  
@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete_item(id):
  # Using global helps you delete the item from the whole list instead of making a new list in the function
  global items
  item = next((i for i in items if i["id"] == id), None)
  if not item:
    return jsonify({"message": "Item not found!"}), 404
  # Returns all remaining items that don't have the same id as the chosen one
  items = [i for i in items if i["id"] != id] # where global is relevant
  return jsonify({"message": "Item deleted", "remaining_items": items}), 200
