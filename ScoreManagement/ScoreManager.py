import json
import boto3


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    scoreTable = dynamodb.Table("Score")
    
    if event['httpMethod'] == 'GET':
        if 'queryStringParameters' in event:
            params = event['queryStringParameters']
            if 'GameName' in params and 'Username' in params:
                gameName = params['GameName']
                user = params['Username']
                key = gameName + ': ' +  user
                data = scoreTable.get_item(Key={'Key': key})
                if 'Item' in data:
                    message = data['Item']
                    return send_message(200, str(message))
                else:
                    return send_message(400, 'Cant find ' + user + ' in game ' + gameName)
            else:
                return send_message(400, 'GameName and Username cant be empty')
        else:
            return send_message(400, 'Parameters cant be empty')
    
    elif event['httpMethod'] == 'PUT':
        if 'body' in event:
            receivedData = event['body']
            body = json.loads(receivedData)
            if 'GameName' in body and 'Username' in body and 'Score' in body:
                gameName = body['GameName']
                user = body['Username']
                key = gameName + ': ' + user
                data = scoreTable.get_item(Key={'Key': key})
                usersTable = dynamodb.Table('Users')
                #check user
                mUser = usersTable.get_item(Key={'ID': user})
                if not 'Item' in mUser:
                    return send_message(400, 'Couldnt find user ' + user)
                gamesTable = dynamodb.Table('RemoteSettings')
                #check game
                mGame = gamesTable.get_item(Key={'game_name': gameName})
                if not 'Item' in mGame:
                    return send_message(400, 'Couldnt find game ' + gameName)
                
                if 'Item' in data:
                    scoreTable.update_item(
                        Key = {
                            'Key' : key
                        },
                        UpdateExpression = 'SET Score = :val',
                        ExpressionAttributeValues={
                            ':val': body['Score']
                        }
                    )
                    
                    return send_message(200, 'Updated score succesfully')
                else:
                    newUser = {
                        'Key' : key,
                        'Score': body['Score']
                    }
                    scoreTable.put_item(
                        Item = newUser
                    )
                    return send_message(200, 'Updated score succesfully')
            else:
                return send_message(400, 'Username, GameName, Score cant be empty')
        else:
            return send_message(400, 'Username, GameName, Score cant be empty')
    else:
        return send_message(400, 'Only GET, PUT request are supported')
                    

def send_message(code, message):
    return{
        'statusCode' : code,
        'body': json.dumps(message)
    }
