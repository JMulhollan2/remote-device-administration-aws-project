# API Configuration
This  directory holds all API configuration, as Swagger and CloudFormation config.

* [apis.cf.yaml:](/api/apis.cf.yaml) Holds the CloudFormation config for the API nested stack, deploys the Desktop API and Web API.
* [desktop-api.yaml:](/api/desktop-api.yaml) Holds the config for the desktop API. Contains context/methods to allow the desktop app to contact the main system to create new devices (upon first activation), update the main DB on status of the device, etc.
* [web-api.yaml:](/api/web-api.yaml) Holds the config for the web API. Contains context/methods to pull/push data to the DynamoDB table using Cognito as an authenticator.