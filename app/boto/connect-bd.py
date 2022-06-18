import mysql.connector
import sys
import boto3
import os

ENDPOINT = "database-flask-1.cu2nc81c600u.eu-west-1.rds.amazonaws.com"
PORT = "3306"
USER = "root"
REGION = "eu-west-1"
DBNAME = "posts"
PASSWD = os.environ['PASSWD']


# gets the credentials from .aws/credentials
session = boto3.Session(profile_name='default')
client = session.client('rds')

token = client.generate_db_auth_token(
    DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

try:
    conn = mysql.connector.connect(
        host=ENDPOINT, user=USER, passwd=PASSWD, port=PORT, database=DBNAME, ssl_ca='SSLCERTIFICATE')
    cur = conn.cursor()
    cur.execute("""SELECT * from posts where id = 4""")
    query_results = cur.fetchall()
    print(query_results)
except Exception as e:
    print("Database connection failed due to {}".format(e))
