import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('RemoteSettings')
    
    if event['httpMethod'] == 'GET':
        if 'queryStringParameters' in event:
            params = event['queryStringParameters']
            if 'GameName' in params:
                mGameName = params['GameName']
                response = table.get_item(Key = {'game_name': mGameName})
                if 'Item' in response:
                    item = response['Item']
                    item = str(item)
                    return send_message(200, item)
                else:
                    return send_message(400, 'Couldnt find ' + mGameName)
            else:
                return send_message(400, 'Request GameName params')
                
    elif event['httpMethod'] == 'PUT':
        if 'body' in event:
            recieveData = event['body']
            body = json.loads(recieveData)
            if 'GameName' in body and 'Property' in body and 'Value' in body:
                mGameName = body['GameName']
                response = table.get_item(Key={'game_name':mGameName})
                if 'Item' in response:
                    mGameProperty = body['Property']
                    mGameValue = body['Value']
                    table.update_item(
                        Key = {
                            'game_name' : mGameName
                        },
                        UpdateExpression = 'SET ' + mGameProperty + ' = :val',
                        ExpressionAttributeValues={
                            ':val': mGameValue
                        }
                    )
                    return send_message(200, '{"result": "' + mGameName + ' updated '  + mGameProperty + ' successfully"}')
                else :
                    return send_message(400, 'Couldnt find ' + mGameName)
            else :
                return send_message(400, 'Missing Game Name, Property, or Value')
                
        else :
            return send_message(400, 'Recieved Data is Empty')

   
def send_message(code, message):
    return {
        'statusCode': code,
        'body': json.dumps(message)
    }
