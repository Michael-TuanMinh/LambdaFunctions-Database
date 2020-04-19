import json
import datetime
import boto3
import decimal

events = ["GameInstalled", "GameDeleted", "GameStart", "GameOver",  "ItemPurchased"]

def check_event(name):
    for i in events:
        if i == name:
            return True
    return False

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Events')

    if event['httpMethod'] == 'PUT':
        if 'body' in event:
            recievedData = event['body']
            body = json.loads(recievedData)
            if 'GameName' in body and 'Username' in body and 'EventName' in body and 'EventParameter' in body:
                
                usersTable = dynamodb.Table('Users')
                gamesTable = dynamodb.Table('RemoteSettings')
                
                user = usersTable.get_item(Key={'ID':body['Username']})
                if not 'Item' in user:
                    return send_message(400, 'Couldnt find user ' + body['Username'])
                    
                game = gamesTable.get_item(Key={'game_name':body['GameName']})
                if not 'Item' in game:
                    return send_message(400, 'Couldnt find game ' + body['GameName'])
                    
                if not check_event(body['EventName']):
                    return send_message(400, 'Event ' + body['EventName'] + ' is not defined')
                else:
                    time = datetime.datetime.now() - datetime.timedelta(hours = 5)
                    item = {
                    'Time': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'GameName':  body['GameName'],
                    'Username':  body['Username'],
                    'EventName': body['EventName'],
                    'EventParameter': body['EventParameter']
                }
                table.put_item(
                    Item = item
                )
                return send_message(200, 'Event updated successfully')

            else:
                return send_message(400, 'GameName, Username, EventName, and EventParameter cant be empty')
        else :
            return send_message(400, 'Body cant be empty')
            
    elif event['httpMethod'] == 'GET':
        
        return send_message(200, table.scan())
            
    else:
        return send_message(400, 'Only GET and POST are supported')

def send_message(code, message):
    return {
        'statusCode': code,
        'body': json.dumps(message, cls = DecimalEncoder)
    }

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
