import json

from bmi import bmi


def route(argument):
    switcher = {
        "manage_bmi": bmi.get_bmi,
        "ManageBMI.Recalculate": bmi.calculate_bmi
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument, lambda event: {
        "statusCode": 500,
        "body": {}
    })
    # Execute the function
    return func

def webhook(event, context):
    print(json.dumps(event, indent=4))
    body = json.loads(event['body'])
    # look into event & find action / intent
    try:
        action =body["queryResult"]["action"]
    except KeyError:
        return {
            "statusCode": 500,
            "body": json.dumps({})
        } 
    # publish event
    
    # get handler/agent for action/intent
    agent = route(action)
    # call agent with event
    response = agent(body)
    # reply 
    response = {
        "statusCode": response["statusCode"],
        "body": json.dumps(response["body"])
    }

    return response

