class VPC:
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.ec2 """

    def create_vpc(self):
        print('Creating the VPC ...')
        return self._client.create_vpc(CidrBlock='10.0.0.0/16')

    def add_name_tag(self, resource_id, resource_name):
        return self._client.create_tags(
            Resources=[resource_id],
            Tags=[{
                'Key': 'Name',
                'Value': resource_name
            }]
        )

    def create_igw(self):
        print('Creating an IGW ...')
        return self._client.create_internet_gateway()

    def attach_igw_to_vpc(self, igw_id, vpc_id):
        print('Attaching IGW ' + igw_id + ' to VPC ' + vpc_id)
        return self._client.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)

    def create_subnet(self, vpc_id, cidr_block):
        print('Creating a subnet for VPC ' + vpc_id + ' with CIDR Block ' + cidr_block)
        return self._client.create_subnet(VpcId=vpc_id, CidrBlock=cidr_block)

    def create_public_rt(self, vpc_id):
        print('Creating Public RT ...')
        return self._client.create_route_table(VpcId=vpc_id)

    def add_def_route(self, rt_id, igw_id):
        print('Adding default route pointing to IGW ' + igw_id + ' in public RT ' + rt_id)
        return self._client.create_route(
            RouteTableId=rt_id,
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=igw_id
        )

    def associate_subnet_with_rt(self, subnet_id, rt_id):
        print('Associating subnet ' + subnet_id + ' with RT ' + rt_id)
        return self._client.associate_route_table(SubnetId=subnet_id, RouteTableId=rt_id)

    def allow_auto_assign_ip_address_for_subnet(self, subnet_id):
        return self._client.modify_subnet_attribute(SubnetId=subnet_id, MapPublicIpOnLaunch={'Value': True})
