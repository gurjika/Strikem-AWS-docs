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

        player_1_id = message['player_1_id']
        player_2_id = message['player_2_id']

        delete_query = """
            DELETE FROM Invitation
            WHERE (player_inviting = %s AND player_invited = %s)
            OR (player_inviting = %s AND player_invited = %s)
        """

        cursor.execute(delete_query, (player_2_id, player_1_id, player_1_id, player_2_id))

        conn.commit()
    return {
        'statusCode': 200,
        'body': f'deleted finished invitations'
    }