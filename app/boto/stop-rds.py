import boto3

client = boto3.client('rds')

response = client.stop_db_instance(
    DBInstanceIdentifier='database-flask-1'
)

print(response)
