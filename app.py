from flask import Flask, request, jsonify, make_response
app = Flask(__name__)

items = [
  {"id": 1, "name": "Fluffy Socks"},
  {"id": 2, "name": "Black Jeans"},
  {"id": 3, "name": "Pink Sweater"},
  {"id": 4, "name": "Baggy White Shirt"},
  {"id": 5, "name": "Grey Shorts"},
]
@app.route("/inventory", methods=["GET"])
def get_items():
  return jsonify(items), 200

@app.route("/inventory/<int:id>", methods=["GET"])
def get_item(id):
  for item in items:
    if item["id"] == id:
      return jsonify(item), 200
  else:
    message = {"message": "Item not found!"}
    return jsonify(message), 404
    
@app.route("/inventory", methods=["POST"])
def add_item():
  data = request.get_json()
  new_id = max((i["id"] for i in items), default=0)+ 1
  new_item = {"id": new_id, "name": data["name"]}
  items.append(new_item)
  return jsonify(new_item), 200

@app.route("/inventory/<int:id>", methods=["PATCH"])
def update_item(id):
  # Gets the data sent from the request if its json?
  data = request.get_json()
  # Next iterates to the next thing automatically
  # Loops through each item in the items array and checks if the id in the same as the one in the url, if not it returns None
  item = next((i for i in items if i["id"] == id), None)
  # If there is no item with that ID, it returns an error message
  if not item:
    message = {"message": "Item not found!"}
    return jsonify(message), 404
  # If no data was sent retunr error messages
  if not data:
    return jsonify({"message":"Cannot return an empty field"}), 404
  # If data was sent but "name" wasn't there return error message
  if "name" not in data:
      return jsonify({"message":"The key 'name' must be in your request"}), 404
  else:
      return make_response(jsonify("Item updated", item, 200))
  
@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete_item(id):
  # Using global helps you delete the item from the whole list instead of making a new list in the function
  global items
  item = next((i for i in items if i["id"] == id))
  if not item:
    return jsonify({"message": "Item not found!"}), 404
  # Returns all remaining items that don't have the same id as the chosen one
  remainders = [i for i in items if i["id"] != id]
  return make_response(jsonify("Item deleted", remainders, 200))


  

          

