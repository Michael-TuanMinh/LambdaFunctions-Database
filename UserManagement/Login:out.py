import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')
    
#login
    if event['httpMethod'] == 'PUT':
        if 'body' in event:
            recieveData = event['body']
            body = json.loads(recieveData)
            if 'Username' in body and 'Password' in body :
                receivedID = body['Username']
                receivedPassword = body['Password']
                user = table.get_item(Key={'ID':receivedID})
                if 'Item' in user:
                    item = user['Item']
                    if item['Password'] == receivedPassword:
                        table.update_item(
                            Key = {
                                'ID' : receivedID
                            },
                            UpdateExpression = 'SET mSession = :val',
                            ExpressionAttributeValues={
                                ':val': 'Online'
                            }
                        )
                        
                        return send_message(200, 'User ' + receivedID + ' logged in successfully')
                    else:
                        return send_message(400, 'Username or Password is not correct')
                else:
                    return send_message(400, 'User ' + receivedID + " doesnt exist")
            else:
                return send_message(400, 'Username and Password cannot be empty')
        else :
            return send_message(400, 'Missing data')
            

#logout
    elif event['httpMethod'] == 'GET':
        if event['queryStringParameters']:
            params = event['queryStringParameters']
            if 'Username' in params :
                receivedID = params['Username']
                user = table.get_item(Key={'ID':receivedID})
                if 'Item' in user:
                    table.update_item(
                        Key = {
                            'ID' : receivedID
                        },
                        UpdateExpression = 'SET mSession = :val',
                        ExpressionAttributeValues={
                            ':val': 'Offline'
                        }
                    )
                    
                    return send_message(200, "User logged out successfully")
                    
                else:
                    return send_message(400, 'Couldnt find user ' + receivedID)
            else:
                return send_message(400, 'Username cannot be empty')
        else :
            return send_message(400, 'Username cannot be empty')
    else:
        return send_message(400, 'Please use GET request')
        
def send_message(code, message):
    return {
        'statusCode': code,
        'body': json.dumps(message)
    }
