from telethon import TelegramClient, events, Button

# Replace with your control bot token
api_id = 25112064  # You need to use your own API ID
api_hash = 'a53b9f3489f19a3236a006c445766e92'  # You need to use your own API hash
control_bot_token = '6871404184:AAHdZ4hWQblSrYmlk36uSslK5RgJFTtxP5c'

client = TelegramClient('prakash_session', api_id, api_hash)

@client.on(events.NewMessage(pattern='/start'))
async def start_command(event):
    with open('bot_status.txt', 'w') as f:
        f.write('on')
    await event.reply('Main bot has been turned ON.')

@client.on(events.NewMessage(pattern='/stop'))
async def stop_command(event):
    with open('bot_status.txt', 'w') as f:
        f.write('off')
    await event.reply('Main bot has been turned OFF.')

@client.on(events.NewMessage(pattern='/addresponse'))
async def add_response_command(event):
    await event.reply(
        'Please send the response in the format:\n`pattern:response`\nFor example:\n`hi:Hello there!`',
        buttons=[Button.inline('Cancel', b'cancel_add')]
    )

@client.on(events.NewMessage)
async def handle_response_addition(event):
    if event.text.startswith('cancel_add'):
        await event.reply('Response addition canceled.')
    elif ':' in event.text:
        response_text = event.text.split(':', 1)
        if len(response_text) == 2:
            pattern, response = response_text
            pattern = pattern.strip().lower()
            response = response.strip()

            # Update the responses file
            with open('responses.txt', 'a') as f:
                f.write(f'{pattern}:{response}\n')
            
            await event.reply(f'Success! Response added: `{pattern}` -> `{response}`')
            # Optionally notify the main bot or refresh its responses list

async def main():
    await client.start(bot_token=control_bot_token)
    print("Control bot is connected")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
