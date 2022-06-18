import boto3

client = boto3.client('rds')

response = client.create_db_instance(
    AllocatedStorage=5,
    DBInstanceClass='db.t2.micro',
    DBInstanceIdentifier='database-flask-2',
    Engine='MySQL',
    MasterUserPassword='PASSWORD_FOR RDS',
    MasterUsername='root',
    VpcSecurityGroupIds=[
        'sg-0bc5bd0b7573fa725',
    ]


)

print(response)
