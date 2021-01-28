echo ""
echo "Uploading bootstrap..."

aws cloudformation deploy \
 --stack-name prco304-bootstrap \
 --template-file cloudformation/bootstrap.cf.yaml \
 --capabilities CAPABILITY_IAM

echo "Bootstrap phase done."
echo ""
echo "Uploading templates..."

aws cloudformation package \
 --s3-bucket=prco304-bootstrap-bucket \
 --template-file cloudformation/master-template.yaml \
 --output-template-file dist/master-template.yaml

aws cloudformation deploy \
 --stack-name prco304-master-stack \
 --template-file dist/master-template.yaml \
 --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM

echo "Template phase done."
echo ""
echo "Running configuration scripts...."

sh scripts/upload-website.sh

echo "Configuration script phase done."