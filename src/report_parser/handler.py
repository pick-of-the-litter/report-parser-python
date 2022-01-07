import json
import logging
from io import BytesIO
import pandas as pd
import os


from boto3 import client, resource

logger = logging.getLogger()
logger.setLevel(logging.INFO)


TASK1_TOPIC_ARN=os.environ.get("TASK1_TOPIC_ARN")
TASK2_TOPIC_ARN=os.environ.get("TASK2_TOPIC_ARN")
TASK3_TOPIC_ARN=os.environ.get("TASK3_TOPIC_ARN")
TASK4_TOPIC_ARN=os.environ.get("TASK4_TOPIC_ARN")
TASK5_TOPIC_ARN=os.environ.get("TASK5_TOPIC_ARN")
EMAIL_LOOKUP_TABLE=os.environ.get("EMAIL_LOOKUP_TABLE")


def handler(event, context):
    # connect to s3 and pull the file
    logger.info(event)
    s3 = resource("s3")
    db = client("dynamodb")
    s3_data=event["Records"][0]["s3"]
    response=s3.Object(s3_data["bucket"]["name"], s3_data["object"]["key"]).get()
    logger.info(response)
    
    excel_file = BytesIO(response["Body"].read())
    task_two = pd.read_excel(excel_file, sheet_name="Task2", usecols=["Service Portfolio Owned by", "Service Portfolio"])

    #create list of apps assigned top each person
    dedupe_map = {}
    for app, owner in task_two.values:
        if owner in dedupe_map:
            dedupe_map[owner]["applications"].append(app)
        else:
            dedupe_map[owner] = {
                "applications": [app],
                "email": get_email(owner, db)
            }
    
    logger.info(dedupe_map)

    sns = resource('sns')
    topic = sns.Topic(TASK2_TOPIC_ARN)

    for owner, values in dedupe_map.items():
        response=topic.publish(
            Message=json.dumps({
                owner: values
            })
        )

        logger.info(response)

    pass

def get_email(owner, db):
    item = db.get_item(
        Key={
            "id": {
                "S": "Verma, Steevan"
            }
        },
        TableName="reports-parser-ContactTable-TNF6F0FU8GUA",
        ProjectionExpression="Email"
    )

    return item["Item"]["Email"]["S"]
