# DynamoDB Config
This directory holds the configuration for the DynamoDB table. Does not hold any data, simply the config for an empty table.

* [dynamodb.cf.yaml:](/dynamodb/dynamodb.cf.yaml) Holds the config for the DynamoDB table as well as the event source mapping which monitors the table for changes and sends any data change notifications to the `NgrokInform` Lambda.