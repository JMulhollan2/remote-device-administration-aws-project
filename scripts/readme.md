# Deployment Scripts
This directory holds all deployment scripts for deploying the system to AWS.

* [deploy-stack.sh:](/scripts/deploy-stack.sh) Shell script for deploying system bootstrap, main CloudFormation templates, and uploading the website files to the website bucket.
* [upload-website.sh:](/scripts/upload-website.sh) Shell script to delete websitebucket contents and upload new website files, for quick and easy testing of changes to website code.