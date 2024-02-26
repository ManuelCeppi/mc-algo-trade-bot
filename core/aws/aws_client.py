import logging
import os
import boto3

class AWSClient:
    def __init__(self):
        self.__sns_client = boto3.client(
            "sns",
            aws_access_key_id=os.environ.get('AWS_USER_ACCESS_KEY'), 
            aws_secret_access_key=os.environ.get('AWS_USER_SECRET_KEY'),
            region_name="eu-central-1"
        )

    def send_message(self, message):
        try:
            self.__sns_client.publish(
                Message=message,
                TopicArn=os.environ.get('SNS_TOPIC_ARN'),
            )
        except Exception as e:
            logging.error("Error publishing message to %s: %s.", os.environ.get('SNS_TOPIC_ARN'), e)