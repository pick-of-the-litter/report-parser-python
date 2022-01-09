import json
import logging
import pandas as pd
import os


from boto3 import client, resource
from io import BytesIO


logger = logging.getLogger()
logger.setLevel(logging.INFO)


TASK1_TOPIC_ARN = os.environ.get("TASK1_TOPIC_ARN")
TASK2_TOPIC_ARN = os.environ.get("TASK2_TOPIC_ARN")
TASK3_TOPIC_ARN = os.environ.get("TASK3_TOPIC_ARN")
TASK4_TOPIC_ARN = os.environ.get("TASK4_TOPIC_ARN")
TASK5_TOPIC_ARN = os.environ.get("TASK5_TOPIC_ARN")
EMAIL_LOOKUP_TABLE = os.environ.get("EMAIL_LOOKUP_TABLE")


def handler(event, context):
    try:
        logger.info(f"Handling event: {event}")
        s3 = resource("s3")
        db = client("dynamodb")
        s3_data = event["Records"][0]["s3"]
        response = s3.Object(
            s3_data["bucket"]["name"],
            s3_data["object"]["key"]
        ).get()
        logger.info(response)

        excel_file = BytesIO(response["Body"].read())
        parse_task_two(db, excel_file)
    except Exception as e:
        logger.error(f"The following error occurred: \n{repr(e)}")
        return {
            "headers": {"Content-Type": "application/json"},
            "statusCode": 500,
            "body": json.dumps({"message": "Error occurred please contact an admin."}),
        }

    return {
        "headers": {"Content-Type": "application/json"},
        "statusCode": 200,
        "body": json.dumps({"message": "Report finished parsing"}),
    }


def parse_task_two(db, excel_file):
    task_two = pd.read_excel(excel_file, sheet_name="Task2", usecols=[
                             "Service Portfolio Owned by", "Service Portfolio"])

    sns = resource("sns")
    # create list of apps assigned top each person
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

    topic = sns.Topic(TASK2_TOPIC_ARN)

    for owner, values in dedupe_map.items():
        message = json.dumps({
            owner: values
        })
        logger.info(f"Publishing: {message}")
        response = topic.publish(
            Message=message
        )

        logger.info(f"Published message with response: {response}")


def get_email(owner, db):
    item = db.get_item(
        Key={
            "id": {
                "S": owner
            }
        },
        TableName=EMAIL_LOOKUP_TABLE,
        ProjectionExpression="Email"
    )

    # return item["Item"]["Email"]["S"]
    return "amurphy9956@live.com"
