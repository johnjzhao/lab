S3_FILE_PATH="s3://gov-solutions-commissions-artifacts-${ENV}/artifactory/${MODULE_NAME}"


pwd
echo "Copying etl python folder to s3"
aws --profile=saml s3 cp python ${S3_FILE_PATH}/python --recursive
echo "Copying library folder to s3"
aws --profile=saml s3 cp library ${S3_FILE_PATH}/library --recursive
echo "Copying sql folder to s3"
aws --profile=saml s3 cp sql ${S3_FILE_PATH}/sql --recursive
echo "Copying test data folder to s3"
aws --profile=saml s3 cp test_data ${S3_FILE_PATH}/test_data --recursive