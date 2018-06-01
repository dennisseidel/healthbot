import json
import math

# TEST how to git rebase to change past commits

def calculate_bmi(event, context):

    print(event)

    weight = float(event['currentIntent']['slots']['Weight'])
    height = float(event['currentIntent']['slots']['Height'])
    height_unit = event['currentIntent']['slots']['HeightUnit']
    height_unit = height_unit.strip()
    age = float(event['currentIntent']['slots']['Age'])
    
    print(height_unit)
    
    if height_unit=='cm':
        height= height/100
        height_unit= 'm'

    print(weight)
    print(age)
    bmi = weight / math.pow(height, 2)
    # check the session data before replying if there has been a BMI before give the user feedback on his improvement.
    response = {
        "sessionAttributes": event['sessionAttributes'],
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": "Your BMI is " + str(round(bmi, 2)) + ".",
            }
        }
    }

    return response

def ckeck_bmi(event, context):
    # check if ther is allready a user profile

    print(event)

    session_attributes = event["sessionAttributes"]
    session_attributes["userBmi"] = "25,2"
    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Delegate",
            "slots": event["dialogAction"]["slots"]
        }
    }
    return response
