import mysql.connector
import boto3
import os
import time

db_identifier = 'database-flask-2'
PASSWD = os.environ['PASSWD']

client = boto3.client('rds')

response = client.create_db_instance(
    AllocatedStorage=5,
    DBInstanceClass='db.t2.micro',
    DBInstanceIdentifier=db_identifier,
    Engine='MySQL',
    MasterUserPassword=PASSWD,
    MasterUsername='root',
    VpcSecurityGroupIds=[
        'sg-0bc5bd0b7573fa725',
    ]
)

print(response)


def db_inst_status(db_id):
    client = boto3.client('rds')
    response = client.describe_db_instances(
        DBInstanceIdentifier=db_id,)
    DBInstanceStatus = response['DBInstances'][0]['DBInstanceStatus']
    return DBInstanceStatus


while db_inst_status(db_identifier) != 'available':
    print("Creating RDS. Waiting 30 sec...")
    time.sleep(30)


client = boto3.client('rds')

response = client.describe_db_instances(
    DBInstanceIdentifier=db_identifier,
)

ENDPOINT = response['DBInstances'][0]['Endpoint']['Address']

PORT = "3306"
USER = "root"
REGION = "eu-west-1"
DBNAME = "posts"


# gets the credentials from .aws/credentials
session = boto3.Session(profile_name='default')
client = session.client('rds')


try:
    conn = mysql.connector.connect(
        host=ENDPOINT, user=USER, passwd=PASSWD, port=PORT, ssl_ca='SSLCERTIFICATE')
    cur = conn.cursor()
    cur.execute("""CREATE DATABASE posts""")

except Exception as e:
    print("Database connection failed due to {}".format(e))


try:
    conn = mysql.connector.connect(
        host=ENDPOINT, user=USER, passwd=PASSWD, port=PORT, database=DBNAME, ssl_ca='SSLCERTIFICATE')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE `posts`.`posts` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    `title` VARCHAR(45) NOT NULL,
                    `content` VARCHAR(45) NOT NULL,
                    PRIMARY KEY (`id`))""")
except Exception as e:
    print("Creatin table failed due to {}".format(e))

command = 'curl -X POST https://api.telegram.org/bot$BotToken/sendMessage -d \
    chat_id=$ChatId -d \
    text="{} is ready"'.format(db_identifier)
os.system(command)
print(db_identifier, "is ready.")
