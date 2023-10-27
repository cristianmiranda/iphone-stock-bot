#!/usr/bin/python3

import boto3
import requests
import time

from datetime import datetime

# Initializing a DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('IPHONE15_STOCK')


def run(apple_url, bot_token, recipients):
    # bot_token = sys.argv[1]
    # recipients = json.loads(sys.argv[2])

    # Make a GET request to the URL
    response = requests.get(apple_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Load the JSON data from the response
        data = response.json()

        # Iterate over each store in the JSON data
        for store in data['body']['content']['pickupMessage']['stores']:
            store_name = store['storeName']
            zipCode = store['address']['postalCode']

            print(f"-------------------------------------")
            print(f"> {store_name} ({zipCode})")
            print(f"")

            for part, details in store['partsAvailability'].items():
                availability = details['pickupDisplay']
                model = details['messageTypes']['compact']['storePickupProductTitle']

                availability_icon = '🚫'
                if availability == 'available':
                    availability_icon = '✅'

                print(f"{availability_icon} {model} @ {zipCode} is {availability}")

                model_store_key = f"{model}@{store_name}"

                response = table.get_item(Key={'ID': model_store_key})
                db_item = response.get('Item')
                if db_item:
                    db_availability = db_item.get('availability')
                else:
                    db_availability = None

                if db_availability != availability:
                    print(f"Availability changed for {model} @ {zipCode}! Sending notification...")
                    table.put_item(
                        Item={
                            'ID': model_store_key,
                            'availability': availability
                        }
                    )

                    message = f"📱 {model}\n🏰 {store_name} ({zipCode})\n📍 {store['storeDistanceWithUnit']}\n{availability_icon} {availability.upper()}"

                    print(message)
                    telegram_bot_sendtext(message, bot_token, recipients)
    else:
        print(f"Failed to fetch the data. Status code: {response.status_code}")


def telegram_bot_sendtext(bot_message, bot_token, recipients):
    for bot_chatID in recipients:
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        print(response.json())


def handler(event, context):
    apple_url = event['apple_url']
    bot_token = event['bot_token']
    recipients = event['recipients']

    if apple_url:
        print(f"Using Apple URL: {apple_url}")

    if bot_token:
        print(f"Bot token received!")

    if recipients:
        print(f"Recipients: {recipients}")

    print("#1 - Checking iPhone 15 availability")
    run(apple_url=apple_url, bot_token=bot_token, recipients=recipients)

    time.sleep(30)

    print("#2 - Checking iPhone 15 availability")
    run(apple_url=apple_url, bot_token=bot_token, recipients=recipients)

    return { 'status' : 200, 'body' : 'Lambda executed successfully!' }
