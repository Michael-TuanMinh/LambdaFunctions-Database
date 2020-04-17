import json

def lambda_handler(event, context):
    send_message(200, "Hello")
    return{
        'statusCode': 200
    }

    
def send_message(code, content):
    return {
        'statusCode': code,
        'body': json.dumps(content)
    }
