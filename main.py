import argparse
from app import get_items, get_item, add_item, update_item, delete_item
# Sets up the CLI
parser = argparse.ArgumentParser(description="Inventory Management")
# Allows us to define multiple commands
subparsers = parser.add_subparsers()

# Create a new command
parser_add_item = subparsers.add_parser("show-items", help="Show items")
parser_add_item.set_defaults(func=get_items)

parser_add_item = subparsers.add_parser("show-item", help="Show item")
parser_add_item.add_argument("--id", required=True, help="ID")
parser_add_item.set_defaults(func=get_item)

parser_add_item = subparsers.add_parser("add-item", help="Add item")
parser_add_item.add_argument("--name", required=True, help="Name")
parser_add_item.set_defaults(func=add_item)

parser_add_item = subparsers.add_parser("update-item", help="Update item")
parser_add_item.add_argument("--id", required=True, help="ID")
parser_add_item.add_argument("--name", required=True, help="Name")
parser_add_item.set_defaults(func=update_item)

parser_add_item = subparsers.add_parser("delete-item", help="Delete item")
parser_add_item.add_argument("--id", required=True, help="ID")
parser_add_item.set_defaults(func=delete_item)

args = parser.parse_args()
if hasattr(args, "func"):
  args.func(args)
else:
  parser.print_help()