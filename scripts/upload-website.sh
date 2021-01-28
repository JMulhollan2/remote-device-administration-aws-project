echo "Uploading website..."

aws s3 rm --recursive s3://prco304-website-static-host-bucket/
cd website
aws s3 sync . s3://prco304-website-static-host-bucket/
cd ..

echo "Website upload done."