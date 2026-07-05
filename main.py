import argparse
import requests

BASE_URL = "http://127.0.0.1:5000/inventory"

# At each link, it runs the function defined in app.py
def show_items(args):
    # Gets the data found in the base url and diplays it after converting it to a python dictionary
    response = requests.get(BASE_URL)
    print(response.json())

def show_item(args):
    # Since you need the id to display a specific id it takes the id you typed in the terminal and adds it to the end of your url and runs it returning your item
    response = requests.get(f"{BASE_URL}/{args.id}")
    print(response.json())

def add_item(args):
    # Because you need to type in "name" to search through the api to add an item to your items list
    # The json part is used to make your data into a dictionary with the key name
    response = requests.post(BASE_URL, json={"name": args.name})
    try:
        print(response.json())
    except ValueError:
        # If Flask returned empty or invalid JSON
        print("Raw response:", response.text)

def update_item(args):
    response = requests.patch(f"{BASE_URL}/{args.id}", json={"name": args.name})
    print(response.json())

def delete_item(args):
    response = requests.delete(f"{BASE_URL}/{args.id}")
    print(response.json())

# Used to set up the CLI
parser = argparse.ArgumentParser(description="Inventory Management")

# Used to define multiple commands
subparsers = parser.add_subparsers()

parser_show_items = subparsers.add_parser("show-items", help="Show items")
parser_show_items.set_defaults(func=show_items)

parser_show_item = subparsers.add_parser("show-item", help="Show item")
parser_show_item.add_argument("--id", required=True, help="ID")
parser_show_item.set_defaults(func=show_item)

parser_add_item = subparsers.add_parser("add-item", help="Add item")
parser_add_item.add_argument("--name", required=True, help="Name")
parser_add_item.set_defaults(func=add_item)

parser_update_item = subparsers.add_parser("update-item", help="Update item")
parser_update_item.add_argument("--id", required=True, help="ID")
parser_update_item.add_argument("--name", required=True, help="Name")
parser_update_item.set_defaults(func=update_item)

parser_delete_item = subparsers.add_parser("delete-item", help="Delete item")
parser_delete_item.add_argument("--id", required=True, help="ID")
parser_delete_item.set_defaults(func=delete_item)

# Used to take what u typed in the terminal into a python object to make it executable
args = parser.parse_args()
# Checks if the .set_defaults() has the func defined if yes it runs the function then it runs the functions with its arguments
if hasattr(args, "func"):
    args.func(args)
# If the arguments are not set it'll run the help messages
else:
    parser.print_help()
