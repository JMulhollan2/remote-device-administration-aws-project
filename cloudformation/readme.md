# CloudFormation
Holds the CloudFormation bootstrap and master stack that deploys all nested stacks (API, Lambda, Cognito etc.).

* [bootstrap.cf.yaml:](/cloudformation/bootstrap.cf.yaml) Holds the CloudFormation config to deploy some initial, bootstrap services to the environment, such as a package bucket for main deployment.
* [master-template.cf.yaml:](/cloudformation/master-template.yaml) Holds the CloudFormation config that deploys the master CloudFormation stack, in turn deploying each nested stack (API, Cognito, Lambda, DynamoDB, S3, etc).