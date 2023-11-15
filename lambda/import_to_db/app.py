import json
import boto3
import re
import os

def lambda_handler(event, context):
    # data = json.loads(event['body'])
    tableName = os.environ('TableName')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)

    table.put_item(
        Item={
            'FaceID': event['FaceID'],
            'Name': event['Name'],
            'BucketLocation': event['BucketLocation'],
            'BoundingBox': event['BoundingBox']
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Data imported successfully'}),
    }