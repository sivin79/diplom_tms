import boto3
import os

client = boto3.client('rds')

response = client.describe_db_instances(
    DBInstanceIdentifier='database-flask-1',
)

DBInstance_Status = response['DBInstances'][0]['DBInstanceStatus']
endpoint = response['DBInstances'][0]['Endpoint']['Address']
status = response['DBInstances'][0]['DBInstanceStatus']
print("DBInstanceStatus = ", response['DBInstances'][0]['DBInstanceStatus'])
print("type = ", response['DBInstances'][0]['DBInstanceClass'])
print("Endpoint = ", response['DBInstances'][0]['Endpoint']['Address'])
print("-"*30)
# print(response)
