"""
Module for MongoDB operations for goodGirlBot.

This module sets up the MongoDB connection and provides functions
to migrate the database and perform CRUD operations.
"""

from datetime import datetime
from pymongo import MongoClient
from logger import _get_logger

logger = _get_logger()

# Initialize MongoDB client and database
client = MongoClient('mongodb://localhost:27017')
db = client["bot_data"]

def _migrate_db():
    """
    Perform database migrations for MongoDB.

    This function updates documents in the 'kehut' collection that lack
    the 'last_kehu' field by setting it to None.

    Returns
    -------
    None
    """
    result = db.kehut.update_many(
        {"last_kehu": {"$exists": False}},
        {"$set": {"last_kehu": None}}
    )
    logger.info("Migrated %d documents in 'kehut' collection", result.modified_count)

def init_db():
    """
    Initialize the MongoDB database with required indexes.

    This function creates a unique index for active_chats and ensures
    collections exist.

    Returns
    -------
    None
    """
    db.active_chats.create_index("chat_id", unique=True)
    # Optionally, create indexes for other collections if needed.
    _migrate_db()

def save_chat(chat_id: int):
    """
    Save chat_id to MongoDB.

    Parameters
    ----------
    chat_id : int
        The chat ID to save.

    Returns
    -------
    None
    """
    db.active_chats.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_id": chat_id, "is_active": True}},
        upsert=True
    )

def get_active_chats():
    """
    Get all active chat IDs from MongoDB.

    Returns
    -------
    list
        List of active chat IDs.
    """
    cursor = db.active_chats.find({"is_active": True}, {"chat_id": 1, "_id": 0})
    return [doc["chat_id"] for doc in cursor]

def log_button_press(chat_id: int, button_data: str, message_id: int):
    """
    Log button press to MongoDB.

    Parameters
    ----------
    chat_id : int
        The chat ID.
    button_data : str
        The callback data from button.
    message_id : int
        The message ID that contained the button.

    Returns
    -------
    None
    """
    db.button_presses.insert_one({
        "chat_id": chat_id,
        "button_data": button_data,
        "message_id": message_id,
        "time": datetime.now()
    })
