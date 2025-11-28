from telethon import TelegramClient
import config
from logger import logger
import utils
import asyncio

# Initialize the client
client = TelegramClient(config.SESSION_NAME, config.API_ID, config.API_HASH)

async def main():
    logger.info("Starting Telegram Agent...")
    await client.start()
    
    me = await client.get_me()
    logger.info(f"Logged in as: {me.first_name} (@{me.username})")

    # --- Example Usage Area ---
    # Uncomment the functions you want to run or add your logic here.

    # 1. Create a Group (Requires a username to add, e.g., 'some_friend')
    # group = await utils.create_group(client, "Circle AI Test Group", ["some_username"])
    
    # 2. Scrape Messages for AI Training
    # target_chat = 'me' # 'me' is Saved Messages. You can use a group ID or username.
    # messages = await utils.scrape_messages(client, target_chat, limit=50)
    # utils.save_messages_to_file(messages, 'training_data.json')

    # 3. Add Contact
    # await utils.add_contact(client, "+123456789", "John", "Doe")

    logger.info("Main execution finished. Keeping client alive for listening if needed...")
    # await client.run_until_disconnected() # Uncomment if you want to listen for events

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
