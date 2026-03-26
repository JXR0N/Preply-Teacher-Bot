# ================= IMPORTS =================
#=========================================
from datetime import datetime
from telegram import Update
from telegram.error import InvalidToken
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from multiprocessing import Process
from running import *
from src.loadenvs import load_tg
#=========================================
#===========================================



#====bools====
is_bot_running = False
bot_process = None



# ================ COMMANDS =================
#=========================================

def tg_logs_dir():
    Path('tg_logs').mkdir(exist_ok=True)
    logger.info("TG_LOGS available")
def startbot():
    global bot_process
    bot_process = Process(target=start_preplybot)
    logger.info("the preply bot was started")
    bot_process.start()
    return True
def stopbot():
    global bot_process
    logger.info("the preply bot was stopped")
    bot_process.terminate()
    bot_process = False
    return False

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_bot_running
    if is_bot_running and bot_process.is_alive():
        await update.message.reply_text("the bot runs already")

    else:
        await update.message.reply_text("the preply bot was started")
        is_bot_running = True
        startbot()
        return is_bot_running



async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_bot_running
    if is_bot_running and bot_process.is_alive():
        await update.message.reply_text("the preply bot was stopped")
        stopbot()
        is_bot_running = False
        return is_bot_running
    else:
        await update.message.reply_text("the bot is already stopped")



async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong! I'm here'!")



async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_bot_running
    if is_bot_running and bot_process.is_alive():
        await update.message.reply_text("Botstatus: Online ✅")
    else:
        await update.message.reply_text("Botstatus: Offline ❌")
#=========================================
#===========================================





# ================ RESPONSES ================
#=========================================
async def handle_responses(text: str) -> str:
    return f" '{text}' is not a valid command!"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text


    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = await handle_responses(new_text)

        else:
            return
    else:
        response: str = await handle_responses(text)

    path = os.path.join('tg_logs', "tg_logs.txt")
    if not os.path.exists(path):
        with open(path, "x", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
                    f"\nuser: {update.message.from_user.full_name} in {message_type.capitalize()}chat: {text}"
                    "\nbotmessage:" + response)
    else:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"\n\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
                    f"\nuser: {update.message.from_user.full_name} in {message_type.capitalize()}chat: {text}"
                    "\nbotmessage:" + response)

    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}" )
#=========================================
#===========================================





# ================= MAIN PROGRAM =================
#=========================================

if __name__ == "__main__":
    try:
        TOKEN, BOT_USERNAME = load_tg()
        tg_logs_dir()
        app = Application.builder().token(TOKEN).build()

        # Commands
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("stop", stop_command))
        app.add_handler(CommandHandler("ping", ping_command))
        app.add_handler(CommandHandler("status", status_command))

        # Message
        app.add_handler(MessageHandler(filters.TEXT, handle_message))


        # Error
        app.add_error_handler(error)

        # Bot scans for input
        logger.info("scanning...")
        app.run_polling(poll_interval=3)

    except InvalidToken:
        logger.error(f"invalid token")
    except KeyboardInterrupt:
        logger.error("script was stopped")
        sys.exit(1)
    except Exception as e:
        logger.error(f"uknown error: {e}", exc_info=True)
        sys.exit(1)
