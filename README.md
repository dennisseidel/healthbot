alternative: 
- stateless functions that call out to the "data lake / brain" in the fullfillment
  - but this way the info cannot be use within the dialogflow


mange bmi -> calls fullfillment

fullfilment checks for intent (switch intent='manage_bmi') this then calls lambda function manageBmi(request) -> publish message on pubsub/kinesis ?:
* this then check for a existing profile for this person
* if no bmi date exists: reply: "Tell me your hight, weight and age."
* if bmi data exist: reply: "Your current BMI is 25.0 tell me your current stats to update" + context BMI exists

lambdaFunction update_bmi: 


start with a simple application -> full firbases function 

dialogflow -> interface / agent
firebase -> dispatcher 
lambda -> function (business function, manage state e.g. profile - add somethign / get something / adds context)