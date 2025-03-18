import logging
from telegram.ext import CommandHandler, CallbackQueryHandler, ApplicationBuilder, MessageHandler, filters, BaseHandler, ChatMemberHandler, ChatBoostHandler, ChatJoinRequestHandler, ChosenInlineResultHandler, PreCheckoutQueryHandler, PaidMediaPurchasedHandler, ApplicationHandlerStop, PrefixHandler, PollAnswerHandler



from db import init_db
from messages import start, praise, send_good_girl, button_handler, resume_chats, save_every_update
from logger import _get_logger

logger = _get_logger()


TOKEN = 'bot token' # The one you got from BotFather

def main() -> None:
    """
   Main function to start the bot.

    Returns
    -------
    None
    """
    init_db()  # This will handle migrations too
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("praise", praise))
    app.add_handler(CommandHandler("goodgirl", send_good_girl))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT, save_every_update))  # new call
    # also track every other update
    app.add_handler(MessageHandler(filters.ALL, save_every_update))  # new call
    app.add_handler(PollAnswerHandler(save_every_update))
    app.add_handler(ChatMemberHandler(save_every_update))
    app.add_handler(ChatBoostHandler(save_every_update))
    app.add_handler(ChatJoinRequestHandler(save_every_update))
    app.add_handler(ChosenInlineResultHandler(save_every_update))
    app.add_handler(PreCheckoutQueryHandler(save_every_update))
    app.add_handler(PaidMediaPurchasedHandler(save_every_update))
    
            
    app.job_queue.run_once(resume_chats, 1, data=app)
    logger.info("Starting the bot polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
