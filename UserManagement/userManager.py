import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')

    if event['httpMethod'] == 'PUT':
        if 'body' in event:
            receivedData = event['body']
            body = json.loads(receivedData)
            if 'Username' in body and 'Email' in body and 'Password' in body:
                receivedID = body['Username']
                user = table.get_item(Key={'ID':receivedID})
                if 'Item' in user and user['Item']:
                    return send_message(400, 'Username ' + receivedID + ' already exists')
                else:
                    new_user = {
                        'ID' : receivedID,
                        'Password': body['Password'],
                        'Email': body['Email']
                    }
                    table.put_item(
                        Item = new_user
                    )
                    
                    return send_message(200, "User registered successfully")
            else:
                return send_message(400, 'Username, Email, and Password cannot be empty')
        else :
            return send_message(400, 'Username, Email, and Password cannot be empty')
            
#update user
    elif event['httpMethod'] == 'POST':
        if 'body' in event:
            receivedData = event['body']
            body = json.loads(receivedData)
            if 'Username' in body and 'Password' in body and 'Email' in body:
                receivedID = body['Username']
                user = table.get_item(Key={'ID':receivedID})
                
                if 'Item' in user:

                    table.update_item(
                        Key = {
                            'ID' : receivedID
                        },
                        UpdateExpression = 'SET Email = :email, Password = :password',
                        ExpressionAttributeValues={
                            ':email':  body['Email'],
                            ':password':  body['Password']
                        }
                    )
                    
                    return send_message(200,  "User updated successfully")

                else:
                    return send_message(400, 'Couldnt find user ' + receivedID)
            else:
                return send_message(400, 'Username and Password cannot be empty')
        else :
            return send_message(400, 'Username and Password cannot be empty')
            
#Retrieve
    elif event['httpMethod'] == 'GET':
        
        if event['queryStringParameters']:
            params = event['queryStringParameters']
            if 'Username' in params and params['Username']:
                receivedID = params['Username']
                user = table.get_item(Key={'ID':receivedID})
                if 'Item' in user:
                    return send_message(200, str(user['Item']))
                    
                return send_message(400, 'Couldnt find user ' + receivedID)
            else:
                return send_message(400, 'Username cannot be empty')
        else :
            return send_message(400, 'Username cannot be empty')
    else:
        return send_message(400, 'Only support PUT, GET, POST request')

def send_message(code, message):
    return {
        'statusCode': code,
        'body': json.dumps(message)
    }
