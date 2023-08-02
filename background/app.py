import boto3
import time
import os


QUEUE_URL = os.environ["SQS_URL"]
AWS_REGION = os.environ.get("AWS_REGION", "us-west-2")

session = boto3.Session(region_name=AWS_REGION)

sqs = session.client("sqs")

while True:
    try:
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            AttributeNames=["All"],
            MaxNumberOfMessages=1,
            MessageAttributeNames=["All"],
            VisibilityTimeout=30,
            WaitTimeSeconds=20,
        )

        if "Messages" in response:
            message = response["Messages"][0]
            receipt_handle = message["ReceiptHandle"]

            print("Body: %s" % message["Body"])
            if "Attributes" in message:
                print("Attributes: %s" % message["Attributes"])

            sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=receipt_handle)
        else:
            print("No messages to process.")
            time.sleep(1)
    except Exception as e:
        print("An error occurred: %s" % e)
        time.sleep(1)
