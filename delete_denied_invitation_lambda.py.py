import json
import mysql.connector


conn = mysql.connector.connect(
    host="your-rds-endpoint.amazonaws.com",
    user="your_username",
    password="your_password",
    database="your_database"
)

cursor = conn.cursor()

def lambda_handler(event, context):
    for record in event['Records']:
        record = event['Records'][0]
        body = json.loads(record['body'])

        message = json.loads(body['Message'])

        nid = message['nid']

        cursor.execute("DELETE FROM poolstore_invitationdenied WHERE id=%s", (nid,))

        cursor.commit()
    return {
        'statusCode': 200,
        'body': f'nid: {nid}'
    }