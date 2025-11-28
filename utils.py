import json
from datetime import datetime
from telethon import functions, types
from telethon.tl.types import InputUser, InputPhoneContact
from logger import logger

# --- Group Management ---

async def create_group(client, title, users):
    """
    Creates a new basic group with the specified users.
    users: list of usernames or user entities.
    """
    try:
        logger.info(f"Attempting to create group '{title}' with users: {users}")
        # Revert to CreateChatRequest
        result = await client(functions.messages.CreateChatRequest(
            users=users,
            title=title
        ))
        
        # Handle response which is typically messages.InvitedUsers
        chat = None
        if hasattr(result, 'chats') and result.chats:
            chat = result.chats[0]
        elif hasattr(result, 'updates') and hasattr(result.updates, 'chats') and result.updates.chats:
            chat = result.updates.chats[0]
            
        if chat:
            logger.info(f"Group '{title}' created successfully. ID: {chat.id}")
            return chat
        else:
            logger.error("Group created but could not retrieve chat entity from response.")
            logger.info(f"Response type: {type(result)}")
            return None

    except Exception as e:
        logger.error(f"Failed to create group: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None

async def edit_group_title(client, chat_id, new_title):
    """
    Edits the title of a group.
    """
    try:
        logger.info(f"Changing title of chat {chat_id} to '{new_title}'")
        await client(functions.messages.EditChatTitleRequest(
            chat_id=chat_id,
            title=new_title
        ))
        logger.info("Group title updated successfully.")
        return True
    except Exception as e:
        logger.error(f"Failed to edit group title: {e}")
        return False

async def delete_group(client, chat_id):
    """
    Deletes a group (for the current user).
    Note: For basic groups, this usually means deleting the history for oneself
    or kicking everyone if admin. Here we use delete_history which removes it for the user.
    """
    try:
        logger.info(f"Deleting group/chat {chat_id}")
        # This deletes the dialog for the user.
        await client.delete_dialog(chat_id) 
        logger.info("Group deleted/left successfully.")
        return True
    except Exception as e:
        logger.error(f"Failed to delete group: {e}")
        return False

# --- Contact Management ---

async def add_contact(client, phone, first_name, last_name=''):
    """
    Adds a user to contacts by phone number.
    """
    try:
        logger.info(f"Adding contact: {first_name} {last_name} ({phone})")
        result = await client(functions.contacts.ImportContactsRequest(
            contacts=[InputPhoneContact(
                client_id=0,
                phone=phone,
                first_name=first_name,
                last_name=last_name
            )]
        ))
        logger.info(f"Contact added: {result.users[0].id if result.users else 'No user found'}")
        return result
    except Exception as e:
        logger.error(f"Failed to add contact: {e}")
        return None

async def remove_contact(client, user_id):
    """
    Removes a user from contacts.
    """
    try:
        logger.info(f"Removing contact with ID: {user_id}")
        # We need the input user entity
        user = await client.get_input_entity(user_id)
        await client(functions.contacts.DeleteContactsRequest(id=[user]))
        logger.info("Contact removed successfully.")
        return True
    except Exception as e:
        logger.error(f"Failed to remove contact: {e}")
        return False

# --- Message Archiving ---

async def scrape_messages(client, chat_entity, limit=100):
    """
    Scrapes messages from a chat and returns them as a list of dictionaries.
    """
    try:
        logger.info(f"Scraping last {limit} messages from {chat_entity}...")
        messages_data = []
        
        async for message in client.iter_messages(chat_entity, limit=limit):
            if message.text: # Only save text messages for now
                msg_dict = {
                    'id': message.id,
                    'date': message.date.isoformat(),
                    'sender_id': message.sender_id,
                    'text': message.text,
                    'reply_to_msg_id': message.reply_to_msg_id,
                    'is_reply': message.is_reply
                }
                messages_data.append(msg_dict)
        
        logger.info(f"Scraped {len(messages_data)} messages.")
        return messages_data
    except Exception as e:
        logger.error(f"Failed to scrape messages: {e}")
        return []

def save_messages_to_file(messages, filename):
    """
    Saves the list of message dictionaries to a JSON file.
    """
    try:
        logger.info(f"Saving messages to {filename}...")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=4, ensure_ascii=False)
        logger.info("Messages saved successfully.")
    except Exception as e:
        logger.error(f"Failed to save messages: {e}")
