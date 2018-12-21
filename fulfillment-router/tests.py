import unittest
import json
import boto3
from decimal import Decimal
from moto import mock_dynamodb2
from handler import webhook
from bmi import bmi


class TestHandler(unittest.TestCase):
    """ Test handler methods """

    def test_webhook_unkown_action(self):
        """ Test that webhook returns 500 for unkown action """
        event = {
            "body": json.dumps({
                "queryResult": {
                    "action": "1manage_bmi"
                }})
        }
        context = {}
        resp = webhook(event, context)
        self.assertEqual(resp["statusCode"], 500)
        self.assertEqual(resp["body"], json.dumps({}))

    def test_webhook_empty_event(self):
        """ Test that webhook return 500 for empty body/action in event """
        event = {
            'body': json.dumps({})
        }
        context = {}
        resp = webhook(event, context)
        self.assertEqual(resp["statusCode"], 500)
        self.assertEqual(resp["body"], json.dumps({}))

    # def test_webhook_exsting_action(self):
    #     event = {
    #         'body': json.dumps({
    #             "queryResult": {
    #                 "action": "manage_bmi"
    #             }})
    #     }
    #     context = {}
    #     resp = webhook(event, context)
    #     self.assertEqual(resp["statusCode"], 200)
    #     self.assertEqual(resp["body"], json.dumps({
    #         "fulfillmentText": "Your BMI is 24.8. Provide me with your current height and weight to update your BMI."
    #     }))

    def test_get_bmi_for_nonexisting_user(self):
        body = {
            "responseId": "b3b8a9a9-8a11-4f70-a654-458a0cbd0524",
            "queryResult": {
                "queryText": "I weigh 77.3 kg and I am 177 cm",
                "action": "ManageBMI.Recalculate",
                "parameters": {
                    "height": {
                        "amount": 177.0,
                        "unit": "cm"
                    },
                    "weight": {
                        "amount": 77.3,
                        "unit": "kg"
                    },
                    "age": ""
                },
            },
            "originalDetectIntentRequest": {
                "payload": {
                        },
            },
            "session": "projects/trusty-acre-156607/agent/sessions/aef722b8-60f8-4687-9626-e1542ef459cc"
        }
        resp = bmi.get_bmi(body)
        self.assertEqual(resp["statusCode"], 200)
        self.assertEqual(resp["body"]["fulfillmentText"],
                        "Please provide me with your current height and weight to calculate your BMI.")

    @mock_dynamodb2
    def test_get_bmi_for_existing_user(self):
        """ Tests the getting of the bmi """
        table_name='healthbot-profile'
        dynamodb=boto3.resource('dynamodb', 'us-east-1')

        table=dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'profile_id',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'bmi',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'weight',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'height',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'age',
                    'AttributeType': 'N'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        profile = {
            'profile_id': '1416117775147560',
            'bmi': Decimal('24.7'),
            'weight': Decimal('77.3'),
            'height': Decimal('177'),
        }
        table.put_item(Item=profile)
        table = dynamodb.Table(table_name)
        response = table.get_item(
            Key={
                'profile_id': '123'
            }
        )
        if 'Item' in response:
            item = response['Item']
            self.assertTrue("profile_id" in item)
            self.assertEqual(item["profile_id"], "123")

        body = {
            "responseId": "b3b8a9a9-8a11-4f70-a654-458a0cbd0524",
            "queryResult": {
                "queryText": "I weigh 77.3 kg and I am 177 cm",
                "action": "ManageBMI.Recalculate",
                "parameters": {
                    "height": {
                        "amount": 177.0,
                        "unit": "cm"
                    },
                    "weight": {
                        "amount": 77.3,
                        "unit": "kg"
                    },
                    "age": ""
                },
            },
            "originalDetectIntentRequest": {
                "source": "facebook",
                "payload": {
                    "data": {
                        "sender": {
                            "id": "1416117775147560"
                        },
                        "recipient": {
                            "id": "1366946360061315"
                        },
                        "message": {
                            "mid": "mid.$cAATbO1Xo1-VqIYHpEVj8DygzD9PN",
                            "text": "I weigh 77.3 kg and I am 177 cm",
                            "seq": 24709.0
                        },
                        "timestamp": 1.528743895313E12
                    },
                    "source": "facebook"
                }
            },
            "session": "projects/trusty-acre-156607/agent/sessions/aef722b8-60f8-4687-9626-e1542ef459cc"
        }
        resp = bmi.get_bmi(body)
        self.assertEqual(resp["statusCode"], 200)
        self.assertEqual(resp["body"]["fulfillmentText"],
                        "Your BMI is 24.7. Provide me with your current height and weight to update your BMI.")

    @mock_dynamodb2
    def test_calculate_bmi(self):
        """ Test the bmi calculation """
        # pepare environment
        table_name='healthbot-profile'
        dynamodb=boto3.resource('dynamodb', 'us-east-1')

        table=dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'profile_id',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'bmi',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'weight',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'height',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'age',
                    'AttributeType': 'N'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        body = {
            "responseId": "2f218b05-ea6d-4c9e-abeb-7fc1b4bb7091",
            "queryResult": {
                "queryText": "I weight 77 kg and I am 177 cm",
                "action": "ManageBMI.Recalculate",
                "parameters": {
                    "height": {
                        "amount": 177,
                        "unit": "cm"
                    },
                    "weight": {
                        "amount": 77,
                        "unit": "kg"
                    },
                    "age": ""
                },
                "outputContexts": [
                    {
                        "name": "projects/trusty-acre-156607/agent/sessions/49fef680-7f0e-a6f8-d62e-6195b50d6170/contexts/managebmi-followup",
                        "lifespanCount": 1,
                        "parameters": {
                            "height.original": "177 cm",
                            "weight.original": "77 kg",
                            "weight": {
                                "amount": 77,
                                "unit": "kg"
                            },
                            "age.original": "",
                            "age": "",
                            "height": {
                                "amount": 177,
                                "unit": "cm"
                            }
                        }
                    }
                ],
                "intent": {
                    "name": "projects/trusty-acre-156607/agent/intents/987ce242-7704-4baf-bf9c-846fdbe57f46",
                    "displayName": "Recalculate"
                },
                "intentDetectionConfidence": 0.91,
                "diagnosticInfo": {},
                "languageCode": "en"
            },
            "originalDetectIntentRequest": {
                "source": "facebook",
                "payload": {
                    "data": {
                        "sender": {
                            "id": "1416117775147560"
                        },
                        "recipient": {
                            "id": "1366946360061315"
                        },
                        "message": {
                            "mid": "mid.$cAATbO1Xo1-VqIYHpEVj8DygzD9PN",
                            "text": "I weigh 77.3 kg and I am 177 cm",
                            "seq": 24709.0
                        },
                        "timestamp": 1.528743895313E12
                    },
                    "source": "facebook"
                }
            },
            "session": "projects/trusty-acre-156607/agent/sessions/49fef680-7f0e-a6f8-d62e-6195b50d6170"
        }

        resp = bmi.calculate_bmi(body)
        self.assertEqual(resp["statusCode"], 200)
        self.assertEqual(resp["body"]["fulfillmentText"],
                         "Your current BMI is 24.6")

        # get data from dynamodb
        response = table.get_item(
            Key={
                'profile_id': body["originalDetectIntentRequest"]["payload"]["data"]["sender"]["id"]
            }
        )
        if 'Item' in response:
            item = response['Item']
            self.assertTrue("profile_id" in item)
            self.assertEqual(item["bmi"], Decimal('24.577867151840145'))

if __name__ == '__main__':
    unittest.main()
