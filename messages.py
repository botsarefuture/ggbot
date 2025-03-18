import random
from datetime import datetime
import sys
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, JobQueue
from logger import _get_logger

from db import get_active_chats, log_button_press, db
from utils import get_ramdom_good_girl_emojis

logger = _get_logger()

# New function to save every incoming update to the DB.
async def save_every_update(update: Update, context: CallbackContext) -> None:
    """
    Save every incoming update to the DB.

    Parameters
    ----------
    update : Update
        The update object.
    context : CallbackContext
        The callback context.

    Returns
    -------
    None
    """
    logger.warning("Saving every update to the DB")
    logger.info(update.to_dict())
    logger.info(context)
    doc = {
        "chat_id": update.effective_chat.id if update.effective_chat else None,
        "user_id": update.effective_user.id if update.effective_user else None,
        "message_text": update.message.text if update.message else None,
        "callback_data": update.callback_query.data if update.callback_query else None,
        "time": datetime.now(),
        'update': update.to_dict()
    }
    db.messages.insert_one(doc)

def _load_kehut():
    """
    Load kehut from a file.

    Returns
    -------
    list
        List of kehut
    """
    with open("kehut.txt") as f:
        return f.readlines()

def get_last_kehu(chat_id: int) -> str:
    """
    Get the last kehu sent to this chat.

    Parameters
    ----------
    chat_id : int
        The chat ID to check.

    Returns
    -------
    str
        The last kehu sent or None if no previous kehu.
    """
    # Query MongoDB for the latest kehut document by time descending.
    doc = db.kehut.find_one({"chat_id": chat_id}, sort=[("time", -1)])
    return doc.get("kehu") if doc else None

async def send_good_girl(update: Update, context: CallbackContext) -> None:
    await save_every_update(update, context)  # new call
    """
    Send a message saying 'good girl' and random heart emojis.

    Parameters
    ----------
    update : Update
        Incoming update.
    context : CallbackContext
        Callback context.

    Returns
    -------
    None
    """
    chat_id = update.effective_chat.id
    logger.info("Sending a good girl message to chat_id %d", chat_id)
    await context.bot.send_message(chat_id=chat_id, text="Good girl! " + get_ramdom_good_girl_emojis())

async def goodgirl(update: Update, context: CallbackContext) -> None:
    await save_every_update(update, context)  # new call
    """
    Immediately send a good girl message.

    Parameters
    ----------
    update : Update
        Incoming update.
    context : CallbackContext
        Callback context.

    Returns
    -------
    None
    """
    await send_good_girl(update, context)

async def send_praise_message(bot, chat_id: int) -> None:
    """
    Send a praise message with buttons to a specific chat.

    Parameters
    ----------
    bot : Bot
        The telegram bot instance.
    chat_id : int
        The chat ID to send the message to.

    Returns
    -------
    None
    """
    logger.info("Sending praise message to chat_id %d", chat_id)
    chat = await bot.get_chat(chat_id)
    is_private = chat.type == "private"
    reply_markup = None
    if is_private:
        keyboard = [
            [
                InlineKeyboardButton("Kiitos", callback_data="yes_i_am"),
                InlineKeyboardButton("💞 Kehu lisää", callback_data="more_praise"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    
    last_kehu = get_last_kehu(chat_id)
    kehut = _load_kehut()
    kehu = random.choice(kehut)
    while kehu == last_kehu and len(kehut) > 1:
        kehu = random.choice(kehut)
    
    # Insert new kehu document into MongoDB
    db.kehut.insert_one({
        "chat_id": chat_id,
        "kehu": kehu,
        "time": datetime.now(),
        "last_kehu": last_kehu
    })
        
    await bot.send_message(
        chat_id=chat_id,
        text=kehu,
        reply_markup=reply_markup,
    )

async def scheduled_good_girl(context: CallbackContext) -> None:
    """
    Send a scheduled good girl message using job context.
    
    Parameters
    ----------
    context : CallbackContext
        The job context containing chat_id.
    
    Returns
    -------
    None
    """
    chat_id = context.job.data  # chat_id is passed directly as data
    logger.info("Sending scheduled good girl message to chat_id %d", chat_id)
    await context.bot.send_message(chat_id=chat_id, text="Good girl! " + get_ramdom_good_girl_emojis())

def schedule_message(job_queue: JobQueue, chat_id: int) -> None:
    """
    Schedule the next message.

    Parameters
    ----------
    job_queue : JobQueue
        The job queue instance.
    chat_id : int
        Unique identifier for the target chat.

    Returns
    -------
    None
    """
    delay = random.randint(1, 10) * 60  # changed to fixed 5 minutes delay (300 seconds)
    delay_1 = random.randint(1, 10) * 60  # changed to fixed 5 minutes delay (300 seconds)
    if delay == delay_1:
        delay_1 += 60
    logger.info("Scheduling message for chat_id %d with delay %d seconds", chat_id, delay)
    job_queue.run_once(send_gender_message, delay, data={"chat_id": chat_id, "job_queue": job_queue})
    job_queue.run_once(scheduled_good_girl, delay_1, data=chat_id)

async def send_gender_message(context: CallbackContext) -> None:
    """
    Send a gender euphoria message with inline buttons from job context.

    Parameters
    ----------
    context : CallbackContext
        The job context.

    Returns
    -------
    None
    """
    data = context.job.data  # expects a dict
    chat_id = data["chat_id"]
    job_queue = data["job_queue"]
    logger.info("Sending scheduled message to chat_id %d", chat_id)
    await send_praise_message(context.bot, chat_id)
    schedule_message(job_queue, chat_id)

async def resume_chats(app) -> None:
    """
    Resume scheduling for all active chats.

    Parameters
    ----------
    app : Application
        The telegram bot application instance.

    Returns
    -------
    None
    """
    active_chats = get_active_chats()
    logger.info("Resuming messages for %d chats", len(active_chats))
    for chat_id in active_chats:
        schedule_message(app.job_queue, chat_id)

async def button_handler(update: Update, context: CallbackContext) -> None:
    await save_every_update(update, context)  # new call
    """
    Handle button presses and route them accordingly.

    Parameters
    ----------
    update : Update
        Incoming update.
    context : CallbackContext
        Callback context.

    Returns
    -------
    None
    """
    query = update.callback_query
    await query.answer()
    
    log_button_press(
        update.effective_chat.id,
        query.data,
        query.message.message_id
    )
    logger.info("Button pressed - chat_id: %d, data: %s, message_id: %d",
                update.effective_chat.id,
                query.data,
                query.message.message_id)
    if query.data == "more_praise":
        await query.edit_message_reply_markup(reply_markup=None)
        await send_praise_message(context.bot, update.effective_chat.id)
    elif query.data == "yes_i_am":
        responses = [
            "Oleppas hyvä. 💖",
            "Totta puhut, maailma on onnekas saadessaan sinut tänne! ✨",
            "Sinun kauneutesi ja voimasi säteilevät kaikkialle. Älä koskaan unohda sitä. 💕",
            "Olet enemmän kuin tarpeeksi – olet täydellinen juuri sellaisena kuin olet! 💅",
            "Sinussa on jotain ainutlaatuista ja ihanaa, eikä kukaan voi ottaa sitä pois. 🌸"
        ]
        response = random.choice(responses)
        current_text = query.message.text
        new_text = f"{response}\n\n{current_text}"
        await query.edit_message_text(text=new_text)

async def start(update: Update, context: CallbackContext) -> None:
    await save_every_update(update, context)  # new call
    """
    Start command handler to initiate the message schedule.

    Parameters
    ----------
    update : Update
        Incoming update.
    context : CallbackContext
        Callback context.

    Returns
    -------
    None
    """
    chat_id = update.effective_chat.id
    await update.message.reply_text("The good girl bot has been activated.\n You can use commands /praise and /goodgirl to receive messages. You also receive one praise automatically every 15 to 60 minutes.")
    
    logger.info("Chat started - chat_id: %d", chat_id)  
    
    
    # Import locally to avoid circular dependencies.
    from db import save_chat  
    save_chat(chat_id)
    schedule_message(context.job_queue, chat_id)

async def praise(update: Update, context: CallbackContext) -> None:
    await save_every_update(update, context)  # new call
    """
    Immediately send a praise message with buttons.

    Parameters
    ----------
    update : Update
        Incoming update.
    context : CallbackContext
        Callback context.

    Returns
    -------
    None
    """
    await send_praise_message(context.bot, update.effective_chat.id)


