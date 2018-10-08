from src.client_locator import EC2Client
from src.ec2.vpc import VPC
from src.ec2.ec2 import EC2


def main():
    # Create an EC2 Client Connection to AWS
    ec2_client = EC2Client().get_client()

    # VPC
    vpc = VPC(ec2_client)

    # Create the VPC
    vpc_response = vpc.create_vpc()
    print('VPC created: ' + str(vpc_response))

    # Add name tag to the VPC
    vpc_name = 'Sam-VPC'
    vpc_id = vpc_response['Vpc']['VpcId']
    vpc.add_name_tag(vpc_id, vpc_name)
    print('Added ' + vpc_name + ' tag to ' + vpc_id + ' VPC')

    # Create an IGW
    igw_response = vpc.create_igw()
    igw_id = igw_response['InternetGateway']['InternetGatewayId']

    # Attaching the IGW to the VPC
    vpc.attach_igw_to_vpc(igw_id, vpc_id)

    # Create public subnet
    public_subnet_response = vpc.create_subnet(vpc_id, '10.0.1.0/24')
    print('Public Subnet Created: ' + str(public_subnet_response))
    public_subnet_id = public_subnet_response['Subnet']['SubnetId']

    # Name the public subnet
    public_subnet_name = 'Sam-Public-Subnet'
    vpc.add_name_tag(public_subnet_id, public_subnet_name)

    # Create a RT for the Public subnets, reserving default RT for Private subnets
    public_rt_response = vpc.create_public_rt(vpc_id)
    print('Public RT created: ' + str(public_rt_response))
    rt_id = public_rt_response['RouteTable']['RouteTableId']

    # Adding default route pointing to the IGW in Public RT
    vpc.add_def_route(rt_id, igw_id)

    # Associate Public Subnet with Public RT
    vpc.associate_subnet_with_rt(public_subnet_id, rt_id)

    # Allow auto-assign public ip for subnet
    vpc.allow_auto_assign_ip_address_for_subnet(public_subnet_id)

    # Create private subnet
    private_subnet_response = vpc.create_subnet(vpc_id, '10.0.2.0/24')
    print('Private Subnet Created: ' + str(private_subnet_response))
    private_subnet_id = private_subnet_response['Subnet']['SubnetId']

    # Name the private subnet
    private_subnet_name = 'Sam-Private-Subnet'
    vpc.add_name_tag(private_subnet_id, private_subnet_name)

    # EC2 Instances
    ec2 = EC2(ec2_client)

    # Create a Key Pair
    key_pair_name = 'sam-key'
    key_pair_response = ec2.create_key_pair(key_pair_name)
    print('Created Key Pair with name ' + key_pair_name + ': ' + str(key_pair_response))

    # Create SG for Public EC2 Instance
    public_sg_name = 'Sam-Public-SG'
    public_sg_desc = 'Public SG'
    public_sg_response = ec2.create_sg(public_sg_name, public_sg_desc, vpc_id)
    public_sg_id = public_sg_response['GroupId']

    # Adding Inbound HTTP and SSH Rules to Public SG
    ec2.add_inbound_rule_to_sg(public_sg_id)

    # Creating User Data for Public EC2 Instance
    user_data = """#!/bin/bash
                yum update -y
                yum install -y httpd
                systemctl enable httpd
                systemctl start httpd
                echo "<html><body><h1>Welcome to Sam Web-Page</h1></body></html>" > /var/www/html/index.html"""

    # Deploy Public EC2 Instance
    ami_id = 'ami-0e6d2e8684d4ccb3e'
    print("Deploying Public EC2 Instance")
    ec2.deploy_ec2_instance(ami_id, key_pair_name, 1, 1, public_sg_id, public_subnet_id, user_data)

    # Create SG for Private EC2 Instance
    private_sg_name = 'Sam-Private-SG'
    private_sg_desc = 'Private SG'
    private_sg_response = ec2.create_sg(private_sg_name, private_sg_desc, vpc_id)
    private_sg_id = private_sg_response['GroupId']

    # Add Inbound HTTP and SSH Rules to Private SG
    ec2.add_inbound_rule_to_sg(private_sg_id)

    # Deploy Private EC2 Instance
    print("Deploying Private EC2 Instance")
    ec2.deploy_ec2_instance('ami-0e6d2e8684d4ccb3e', key_pair_name, 1, 1, private_sg_id, private_subnet_id, """""")


if __name__ == '__main__':
    main()