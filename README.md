# Final Year Project - James Mulholland

## Remote device tracking and administration

This repository holds the entire codebase for my dissertation project, completed in early 2019. 
The goal of this project was to create a system that was able to securely administrate Desktop computers, with only Windows originally supported. This was achieved by two main areas of the project. 
* The Windows application, written in Python and run as a Windows service, listening for communication from the central system hosted on AWS. Able to perform actions such as remote locking of a device, remote shutdown, and remote wiping. 
* The central system hosted on AWS. Handles front end administration portal, holds the main DB using DynamoDB, APIs and Lambdas for device communication and front-end activity, as well as other various services used by the  application on AWS.

## Directory of resources

* [APIs:](/api/) This directory holds all of the CloudFormation/swagger files required to deploy the API stack. This is deployed as part of a nested stack from inside the main cloudformation directory.
* [Cloudformation:](/cloudformation/) This directory holds the bootstrap and root templates for all CloudFormation code deployed by the project.
* [Cognito:](/cognito/) This directory holds the CloudFormation configuration for the cognito user pool that stored all user credentials for the service.
* [Desktop Application:](/desktop-application/) This directory holds all of the Python code written for the desktop application. This is split into a build folder used during the application build process, a directory of current builds (currently only V1), all of the uncompiled Python files used, and some useful scripts used for the build process as well as debugging.
* [DynamoDB:](/dynamodb/) This directory holds the CloudFormation configuration for the base DynamoDB table used by the central application.
* [Lambda:](/lambda/) This directory holds both the Lambda CloudFormation code used to deploy all respective Lambdas, but also all of the individual Lambda applications. A more detailed explanation of each Lambda is present in the directory.
* [S3:](/s3/) This directory holds the CloudFormation code to deploy the website S3 bucket, as well as access policies for the bucket.
* [Scripts:](/scripts/) This directory contains deployment scripts used to deploy the application stack to AWS, as well as upload the website to the S3 website hosting bucket.
* [Tests:](/tests/) This directory holds some beta automated deployment test scripts that test basic API function. A more mature version would have been integrated into a deployment CodePipeline if time had permit to create one.
* [Utility Scripts:](/UtilityScripts/) Extra credit. Contains some of the older versions / POCs of code written to showcase functionality.
* [Website:](/website/) Contains the entire website structure that is hosted on S3, including all css, javascript, HTML and images.

## Grade

I achieved 73% in this project. Comments included praise for the ingenuity of the system but felt that being a CIS degree, more emphasis should have been placed on security aspects of the project rather than the main system hosted on AWS.
