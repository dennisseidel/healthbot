'use strict';

const functions = require('firebase-functions');
const { WebhookClient } = require('dialogflow-fulfillment');
const { Card, Suggestion } = require('dialogflow-fulfillment');
const Datastore = require('@google-cloud/datastore');

process.env.DEBUG = 'dialogflow:debug';

exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response});
  console.log(`Request headers: ${JSON.stringify(request.headers)}`);
  console.log(`Request body: ${JSON.stringify(request.body)}`)

  function manageBmi(agent) {
    // console.log(JSON.stringify(agent.originalRequest));
    // identify the caller (e.g. facebook) and the caller id 
    let userId = agent.originalRequest.payload.data.sender.id;
    console.log(`UserID: ${userId}`)
    // look up the profile in the to see if there is already a BMI calculated -> use dynamodb or google bigtable? only for analytics not OTP https://de.slideshare.net/dragan10/you-might-payingtoomuchforbigquery
    const datastore = Datastore();
    
    agent.add('Thank you for the question.');
  }

  let intentMap = new Map();
  intentMap.set('manage_bmi', manageBmi);
  agent.handleRequest(intentMap); 
})