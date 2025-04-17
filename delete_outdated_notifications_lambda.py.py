import json
import mysql.connector




def lambda_handler(event, context):

    conn = mysql.connector.connect(
        host="your-rds-endpoint.amazonaws.com",
        user="your_username",
        password="your_password",
        database="your_database"
    )

    cursor = conn.cursor()

    delete_query = """
        DELETE FROM Notification
        WHERE timestamp < NOW() - INTERVAL 5 DAY
    """

    cursor.execute(delete_query)
    conn.commit()

    return {
        'statusCode': 200,
        'body': f'deleted finished invitations'
    } 