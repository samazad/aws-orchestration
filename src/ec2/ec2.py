class EC2:
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.ec2 """

    def create_key_pair(self, key_name):
        print('Creating a key pair with name ' + key_name)
        return self._client.create_key_pair(KeyName=key_name)

    def create_sg(self, sg_name, description, vpc_id):
        print('Creating SG ' + sg_name + ' for VPC ' + vpc_id)
        return self._client.create_security_group(
            GroupName=sg_name,
            Description=description,
            VpcId=vpc_id
        )

    def add_inbound_rule_to_sg(self, sg_id):
        print('Adding Inbound HTTP and SSH Rules to SG ' + sg_id)
        return self._client.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )

    def deploy_ec2_instance(self, image_id, key_name, min_count, max_count, sg_id, subnet_id, user_data):
        print("Launching EC2 Instance(s) within subnet " + subnet_id)
        self._client.run_instances(
            ImageId=image_id,
            KeyName=key_name,
            MinCount=min_count,
            MaxCount=max_count,
            InstanceType='t2.micro',
            SecurityGroupIds=[sg_id],
            SubnetId=subnet_id,
            UserData=user_data
            )