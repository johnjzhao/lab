# install aws cli first and configure it with credentials and default region
# the script will iterate over all US regions of AWS
for region in `aws ec2 describe-regions --filters "Name=endpoint,Values=*us*" --output text | cut -f4`
do
     echo -e "\nListing Instances in region:'$region'..."
     aws ec2 describe-instances --query "Reservations[*].Instances[*].{IP:PublicIpAddress,ID:InstanceId,Type:InstanceType,State:State.Name,Name:Tags[0].Value}" --output=table --region $region
done

aws s3 ls
aws ec2 --output text --query 'Vpcs[*].{VpcId:VpcId,Name:Tags[?Key==`Name`].Value|[0],CidrBlock:CidrBlock}' describe-vpcs
