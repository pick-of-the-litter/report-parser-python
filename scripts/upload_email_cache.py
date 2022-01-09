#!/usr/bin/python
import json
import sys

from boto3 import resource

print("Opening data file")
file = open("cache_data.json")
data = json.load(file)

print(f"connecting to table: {sys.argv[1]}")
db = resource("dynamodb")
table = db.Table(sys.argv[1])

with table.batch_writer() as batch:
    for person in data:
        print(f"Adding {person['name']}")
        batch.put_item(
            Item={
                "id": person["name"],
                "Email": person["email"]
            }
        )