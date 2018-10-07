from src.ec2.vpc import VPC
from src.client_locator import EC2Client


def main():
    # Create an EC2 Client Connection to AWS
    ec2_client = EC2Client().get_client()
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
    igw_attach_response = vpc.attach_igw_to_vpc(igw_id, vpc_id)


if __name__ == '__main__':
    main()