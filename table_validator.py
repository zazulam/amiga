import boto3
import os

dynamo = boto3.client('dynamodb')
table_name = os.environ['SPOTIFY_TABLE_NAME']


def validate_table():
    tables = dynamo.list_tables()

    if table_name in tables['TableNames']:
        return True
    else:
        return create_table()
    
def create_table():
    try:
        resource = dynamo.create_table(
            TableName = table_name,
            AttributeDefinitions=[
                {
                    'AttributeName':'Track_Id',
                    'AttributeType':'S'
                },
            ],
            KeySchema=[
                {
                    'AttributeName':'Track_Id',
                    'KeyType':'HASH'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5,
            }
        )
        
        dynamo.get_waiter('table_exists').wait(TableName=table_name)
        
        return True
    except Exception as ex:
        print("Error on creating table: ",ex)
        return False
