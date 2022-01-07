import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))
    message = event['Records'][0]['Sns']['Message']
    logger.info("From SNS: " + message)
    return message