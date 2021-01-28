# Lambdas
This directory holds all lambda code for the desktop communication and web lambdas, as well as the associated cloudformation code to deploy them.

* [lambdas.cf.yaml:](/lambda/lambdas.cf.yaml) Holds the CloudFormation configuration for all lambdas and permissions. Held as a nested stack.
* [Desktop App Communication:](/lambda/desktop) Holds all the lambdas that interact with the desktop application.
  * [desktop-add-device-api-lambda:](/lambda/desktop/desktop-add-device-api-lambda) Lambda that handles adding a new device to a user when the desktop application configuration manager is run. Runs validation to ensure no primary key (name) duplication etc.
  * [desktop-get-device-data-lambda:](/lambda/desktop/desktop-get-device-data-lambda) This Lambda returns device data to the desktop application and is the main source of a device gathering command data (e.g. Checks the device entry in the table and sees that "ShutdownEnabled" is true)
  * [desktop-modify-device-api-lambda:](/lambda/desktop/desktop-get-device-data-lambda) This Lambda handles all changes to device data in the DynamoDB table, such as updating a device's "ShutdownEnabled" attribute to True.
  * [dynamodb-ngrok-inform-lambda:](/lambda/desktop/desktop-get-device-data-lambda) This lambda monitors any changes to the DynamoDB table (using native integration) and will send pings to a device if any changes are made to the table (e.g. "ShutdownEnabled" changing to True). This ping to a device's ngrok API will then let the device know to make a GET request to check device table data for any instructions.
* [Web App:](/lambda/web) Holds all the lambdas that interact with the web app.
  * [cognito-sign-up-lambda:](/lambda/web/cognito-sign-up-lambda) Configured as a Cognito "PreSignUpLambda" meaning when a request is sent to Congito to add a user, a user in DynamoDB is also created (minus authentication credentials).
  * [web-api-lambda:](/lambda/web/web-api-lambda) Sends data from DynamoDB (username, device data etc.) to the web console after authentication.
  * [web-modify-table-lambda:](/lambda/web/web-modify-table-lambda) Lambda that handles all API requests from the web console to modify table data, mainly device info. E.g. Changing a device name, setting a device to remotely wipe, etc.

  