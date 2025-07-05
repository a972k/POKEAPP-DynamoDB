import boto3
import time
from botocore.exceptions import ClientError

# congfiguration
AMI_ID = "ami-04999cd8f2624f834"  # Amazon linux 2 in us-west-2
INSTANCE_TYPE = "t2.micro"
KEY_NAME = "vockey"
SECURITY_GROUP_NAME = "pokemon-game-sg"
IAM_ROLE_NAME = "PokemonDynamoAccessRole"
REPO_URL = "https://github.com/a972k/POKEAPI-GAME.git"
GAME_SCRIPT = "main.py"
REGION = "us-east-1"

# client setup
ec2_client = boto3.client("ec2", region_name=REGION)
ec2_resource = boto3.resource("ec2", region_name=REGION)
iam_client = boto3.client("iam")
ec2_profile_client = boto3.client("iam", region_name=REGION)

# get default VPC
vpcs = ec2_client.describe_vpcs()
default_vpc_id = vpcs['Vpcs'][0]['VpcId']

# create security group
try:
    security_group = ec2_client.create_security_group(
        GroupName=SECURITY_GROUP_NAME,
        Description="Allow SSH access for Pokemon Game",
        VpcId=default_vpc_id
    )
    ec2_client.authorize_security_group_ingress(
        GroupId=security_group["GroupId"],
        IpPermissions=[{
            "IpProtocol": "tcp",
            "FromPort": 22,
            "ToPort": 22,
            "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
        }]
    )
    print(f"[+] Created security group: {SECURITY_GROUP_NAME}")
except ClientError as e:
    if "InvalidGroup.Duplicate" in str(e):
        print(f"[!] Security group '{SECURITY_GROUP_NAME}' already exists.")
        sg = ec2_client.describe_security_groups(GroupNames=[SECURITY_GROUP_NAME])
        security_group = {"GroupId": sg["SecurityGroups"][0]["GroupId"]}
    else:
        raise

# create IAM role for EC2 to access DynamoDB
assume_role_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "ec2.amazonaws.com"},
        "Action": "sts:AssumeRole"
    }]
}

try:
    iam_client.create_role(
        RoleName=IAM_ROLE_NAME,
        AssumeRolePolicyDocument=json.dumps(assume_role_policy)
    )
    iam_client.attach_role_policy(
        RoleName=IAM_ROLE_NAME,
        PolicyArn="arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
    )
    print(f"[+] IAM role '{IAM_ROLE_NAME}' created and policy attached.")
except ClientError as e:
    if "EntityAlreadyExists" in str(e):
        print(f"[!] IAM role '{IAM_ROLE_NAME}' already exists.")
    else:
        raise

# create instance profile for the IAM role
try:
    iam_client.create_instance_profile(InstanceProfileName=IAM_ROLE_NAME)
    time.sleep(3)
    iam_client.add_role_to_instance_profile(
        InstanceProfileName=IAM_ROLE_NAME,
        RoleName=IAM_ROLE_NAME
    )
    print(f"[+] Instance profile for '{IAM_ROLE_NAME}' created.")
except ClientError as e:
    if "EntityAlreadyExists" in str(e):
        print(f"[!] Instance profile '{IAM_ROLE_NAME}' already exists.")
    else:
        raise

# user data script to install dependencies and clone the game repository
user_data_script = f'''#!/bin/bash
yum update -y
yum install -y git python3 pip
pip3 install boto3
cd /home/ec2-user
git clone {REPO_URL}
echo "cd /home/ec2-user/POKEAPI-GAME" >> /home/ec2-user/.bashrc
echo "python3 {GAME_SCRIPT}" >> /home/ec2-user/.bashrc
'''

# lunch the EC2 instance with the created security group and IAM role
print("[*] Launching EC2 instance...")
instance = ec2_resource.create_instances(
    ImageId=AMI_ID,
    InstanceType=INSTANCE_TYPE,
    KeyName=KEY_NAME,
    MinCount=1,
    MaxCount=1,
    SecurityGroupIds=[security_group["GroupId"]],
    IamInstanceProfile={"Name": IAM_ROLE_NAME},
    UserData=user_data_script
)[0]

print("Waiting for instance to be in 'running' state...")
instance.wait_until_running()
instance.reload()

# uotput instance connesction info
print("\n✅ EC2 instance is running!")
print(f"Public DNS: {instance.public_dns_name}")
print(f"SSH command: ssh -i your-key.pem ec2-user@{instance.public_dns_name}")
print("The game will start automatically when you connect.\n")
