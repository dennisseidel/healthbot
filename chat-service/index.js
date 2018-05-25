'use strict';

function handlePost(request, response) {
  if (body.object === 'page') {
    batch.entry.forEach(function(entry) {
      let webhook_event = entry.messaging[0];
      console.log(webhook_event);
    });
    response.status(200).send('EVENT_RECEIVED');
  }
  response.sendStatus(404);
}

function handleGet(request, response) {
  // Your verify token. Should be a random string.
  let VERIFY_TOKEN = "<YOUR_VERIFY_TOKEN>"
    
  // Parse the query params
  let mode = request.query['hub.mode'];
  let token = request.query['hub.verify_token'];
  let challenge = request.query['hub.challenge'];

  if (mode && token) {
  
    // Checks the mode and token sent is correct
    if (mode === 'subscribe' && token === VERIFY_TOKEN) {
      // Responds with the challenge token from the request
      console.log('WEBHOOK_VERIFIED');
      response.status(200).send(challenge);
    
    } else {
      // Responds with '403 Forbidden' if verify tokens do not match
      response.sendStatus(403);      
    }
  }
}

exports.facebookhook = (request, response) => {
  let body = request.body;

  switch (request.method) {
    case 'GET':
      handleGet(request, response);
      break;
    case 'POST':
      handlePost(request, response);
      break;
    default:
      response.sendStatus(500).send({ error: 'Operation not implemented'});
      break;
  }
};