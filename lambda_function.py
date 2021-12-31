import json
import urllib.request
import os
from pygeocoder import Geocoder
import googlemaps

def lambda_handler(event, context):
    
    sendMessage(event)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
    
def sendMessage(event):
    for message_event in json.loads(json.dumps(event))['events']:
        
        
        search_query = message_event['message']['text']
        gmaps = googlemaps.Client(key=os.environ['googlemap_api_key'])
        place_id = gmaps.geocode(search_query + " カレー")[0]["place_id"]
        search_result = "https://www.google.com/maps/place/?q=place_id:" + place_id
        
        url = 'https://api.line.me/v2/bot/message/reply'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ['line_api_token']
        }
        body = {
            'replyToken': message_event['replyToken'],
            'messages': [
                {
                    "type": "text",
                    "text": search_result,
                }
            ]
        }

        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), method='POST', headers=headers)
        with urllib.request.urlopen(req) as res:
            logger.info(res.read().decode("utf-8"))
