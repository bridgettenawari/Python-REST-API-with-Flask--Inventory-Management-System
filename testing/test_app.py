from app import app

def test_get_items_returns():
  client = app.test_client()
  response = client.get("/inventory/1")
  assert response.status_code == 200
  assert response.get_json() == {
  "id": 1,
  "status": 1,
  "product": {
    "product_name": "Organic Almond Milk",
    "brands": "Silk",
    "ingredients_text": "Filtered water, almonds, cane sugar"
  }
  }