# Cognito
Holds the base CloudFormation config for the Cognito User Pool. 

* [user-pool.cf.yaml:](/cognito/user-pool.cf.yaml) Contains CloudFormation code for the user pool, also specifies the 'Pre sign up Lambda' which interacts with the DynamoDB table to create new users.