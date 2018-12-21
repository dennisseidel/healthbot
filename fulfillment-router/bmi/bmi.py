import json
import math
import boto3
from decimal import Decimal

def get_bmi(body):
    # identify the source
    if body.get('originalDetectIntentRequest', {}).get('source', {}) == 'facebook':
        # get the id of the user (dependents on the input channel) / currently only use facebook
        id = body["originalDetectIntentRequest"]["payload"]["data"]["sender"]["id"]
        # check if there is allready a bmi in the database for the id
        table_name = 'healthbot-profile'
        dynamodb = boto3.resource('dynamodb', 'us-east-1')
        table = dynamodb.Table(table_name)
        response = table.get_item(
            Key={
                'profile_id': id
            }
        )
        if 'Item' in response:
            item = response['Item']
            bmi = item['bmi']
            fulfillment_text = f"Your BMI is {bmi}. Provide me with your current height and weight to update your BMI."
        else:
            fulfillment_text = "It is your first time here, please provide me with your current height and weight to calculate your BMI."
        return {
            "statusCode": 200,
            "body": {
                "fulfillmentText": fulfillment_text,
            }
        }
    else:
        return {
            "statusCode": 200,
            "body": {
                "fulfillmentText": "Please provide me with your current height and weight to calculate your BMI.",
            }
        }


def calculate_bmi(body):
    weight = body["queryResult"]["parameters"]["weight"]["amount"]
    height = body["queryResult"]["parameters"]["height"]["amount"]
    height_in_meter = float(height)/100
    bmi = float(weight) / math.pow(height_in_meter, 2)

    # save to db
    if body.get('originalDetectIntentRequest', {}).get('source', {}) == 'facebook':
        # get the id of the user (dependents on the input channel) / currently only use facebook
        id = body["originalDetectIntentRequest"]["payload"]["data"]["sender"]["id"]
        table_name = 'healthbot-profile'
        dynamodb = boto3.resource('dynamodb', 'us-east-1')
        table = dynamodb.Table(table_name)
        response = table.update_item(
                Key={
                    'profile_id': id
                },
                UpdateExpression="set bmi=:bmi, weight=:weight, height=:height",
                ExpressionAttributeValues={
                    ':bmi': Decimal(str(bmi)),
                    ':weight': Decimal(str(weight)),
                    ':height': Decimal(str(height))
                },
            )

    return {
        "statusCode": 200,
        "body": {
            "fulfillmentText": f"Your current BMI is {bmi:.1f}"
        }
    }
