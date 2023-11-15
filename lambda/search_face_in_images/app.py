import boto3
import os
import json

#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

collection_id = os.environ['COLLECTION_ID']
table_name = os.environ['table_name']
dynamodb = boto3.client('dynamodb')
client=boto3.client('rekognition', region_name = 'ap-northeast-1')

def lambda_handler(event, context):
    #get URI from UI
    uri = event['uri']
    
    #Search face in collection
    faces = rekogintion_search_faces(uri)
    
    #Get OBJ from DB
    
    db = dynamoDB_search(faces)

    
    #Create Obj to response
    obj = obj_responese(db, faces)
    
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(obj)
    }    
    return response
   

def rekogintion_search_faces(uri):
    uri = uri.split("/")
    bucket= uri[2]
    collectionId = collection_id
    fileName= uri[3] + "/" +uri[4]
    threshold = 70
    maxFaces=5
    response = client.search_faces_by_image(CollectionId=collectionId,
                                Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
                                FaceMatchThreshold=threshold,
                                MaxFaces=maxFaces)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response['FaceMatches']['Face']
        
def dynamoDB_search(faces):   
    # Define the list of values
    facesId = []
    for i in faces:
        facesId.append(i.FaceId)
    partition_key_values = facesId
    query_params = {
        'TableName': table_name,
        'KeyConditionExpression': 'FaceId IN (:pk_values)',
        'ExpressionAttributeValues': {
        ':pk_values': {'S': partition_key_values}
        }
    }
    response = dynamodb.query(**query_params) 
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response['Items']                         
        
class obj_to_responese:
  def __init__(self, faceId, boundingbox, name, uri):
        self.faceId = faceId 
        self.boundingbox = boundingbox 
        self.name = name 
        self.uri = uri 

def obj_responese(db, re):
    list_response = []
    for i in db:
        for y in re:
            if i.FaceID == y.FaceId:
                list_response.append(
                    obj_to_responese(
                        i['FaceID'],y['BoundingBox'],i['Name'],i['BucketLocation']
                    )
                ) 
                break
    return list_response            




  