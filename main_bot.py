from telethon import TelegramClient, events
import os
import asyncio
import difflib  # For similarity checking

api_id = 25112064
api_hash = 'a53b9f3489f19a3236a006c445766e92'
phone_number = '+91 6382773420'

client = TelegramClient('prakash_session', api_id, api_hash)

STATUS_FILE = 'bot_status.txt'
RESPONSES_FILE = 'responses.txt'

responses = {}

def get_bot_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            status = f.read().strip()
            return status == 'on'
    return False

def load_responses():
    global responses
    if not os.path.exists(RESPONSES_FILE):
        # Create the responses file with default content
        with open(RESPONSES_FILE, 'w') as f:
            f.write('hi:Hi, welcome to hell\n')
            f.write('hello:Hello there!\n')
    
    new_responses = {}
    with open(RESPONSES_FILE, 'r') as f:
        for line in f:
            if ':' in line:
                pattern, response = line.split(':', 1)
                new_responses[pattern.strip().lower()] = response.strip()

    responses = new_responses

async def check_for_updates():
    while True:
        load_responses()
        await asyncio.sleep(5)  # Wait for 5 seconds before checking again

def find_closest_response(message_text):
    # Find the closest response based on similarity
    closest_match = difflib.get_close_matches(message_text, responses.keys(), n=1)
    if closest_match:
        return responses[closest_match[0]]
    return None

@client.on(events.NewMessage)
async def handler(event):
    if get_bot_status():
        message_text = event.message.text.lower()
        response = responses.get(message_text)
        if response:
            await event.reply(response)
        else:
            # Try to find a similar response
            similar_response = find_closest_response(message_text)
            if similar_response:
                await event.reply(similar_response)
            else:
                await event.reply("Sorry, I don't understand that question.")

async def main():
    await client.start(phone_number)
    print("Main bot is connected")
    client.loop.create_task(check_for_updates())
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
