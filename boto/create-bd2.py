import mysql.connector
import boto3
import os

ENDPOINT = "database-flask-02.cu2nc81c600u.eu-west-1.rds.amazonaws.com"
PORT = "3306"
USER = "root"
REGION = "eu-west-1"
DBNAME = "posts"

PASSWD = os.environ['PASSWD']

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
