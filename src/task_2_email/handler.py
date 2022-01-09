import json
import logging
import os

from boto3 import client

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TEMPLATE_NAME = os.environ.get("TEMPLATE_NAME")


def handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))
    message = json.loads(event['Records'][0]['Sns']['Message'])

    ses = client("ses")

    contact = list(message.keys())[0]
    # email = message[contact]["email"]
    applications = message[contact]["applications"]

    response = ses.send_templated_email(
        Destination={
            'ToAddresses': [
                "amurphy9956@live.com",
            ]
        },
        ReplyToAddresses=[
            'ashley.murphy@bp.com',
        ],
        Source="ashley.murphy@bp.com",
        Template=TEMPLATE_NAME,
        ConfigurationSetName="ash",
        TemplateData=json.dumps({
            "contact": contact,
            "sender": "Ash Murphy",
            "applications": [{"application": app} for app in applications]
        })
    )

    logger.info(response)

    return message
