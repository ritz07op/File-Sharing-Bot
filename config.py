import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

# Load environment variables from .env file
load_dotenv()

# Bot token obtained from BotFather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
if not TG_BOT_TOKEN:
    raise ValueError("TG_BOT_TOKEN environment variable is required.")

# Your API ID from my.telegram.org
try:
    APP_ID = int(os.environ.get("APP_ID", ""))
    if APP_ID == 0:
        raise ValueError("APP_ID environment variable is required and must be a valid integer.")
except ValueError:
    raise ValueError("APP_ID must be a valid integer.")

# Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH")
if not API_HASH:
    raise ValueError("API_HASH environment variable is required.")

# Your db channel Id
try:
    CHANNEL_ID = int(os.environ.get("CHANNEL_ID", ""))
    if CHANNEL_ID == 0:
        raise ValueError("CHANNEL_ID environment variable is required and must be a valid integer.")
except ValueError:
    raise ValueError("CHANNEL_ID must be a valid integer.")

# Owner ID (Admin of the bot)
try:
    OWNER_ID = int(os.environ.get("OWNER_ID", ""))
    if OWNER_ID == 0:
        raise ValueError("OWNER_ID environment variable is required and must be a valid integer.")
except ValueError:
    raise ValueError("OWNER_ID must be a valid integer.")

# Port for your web app (if applicable)
PORT = os.environ.get("PORT", "8080")

# Database URI and name for MongoDB
DB_URI = os.environ.get("DATABASE_URL")
if not DB_URI:
    raise ValueError("DATABASE_URL environment variable is required.")
DB_NAME = os.environ.get("DATABASE_NAME", "filesharexbot")

# Force subscribe to a channel (if enabled)
try:
    FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "0"))
except ValueError:
    FORCE_SUB_CHANNEL = 0

JOIN_REQUEST_ENABLE = os.environ.get("JOIN_REQUEST_ENABLED", None)

# Number of workers for the bot
try:
    TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
except ValueError:
    TG_BOT_WORKERS = 4

# Start message configuration
START_PIC = os.environ.get("START_PIC", "")
START_MSG = os.environ.get("START_MESSAGE", "Hello {first}\n\nI can store private files in a specified Channel, and other users can access them via a special link.")

# Admins list (you can add more admins here)
ADMINS = []
admins_str = os.environ.get("ADMINS", "")
if admins_str:
    try:
        for x in admins_str.split():
            ADMINS.append(int(x))
    except ValueError:
        raise ValueError("Your Admins list contains invalid values (non-integer).")
else:
    raise ValueError("ADMINS environment variable is required.")

# Add the owner to the list of admins
ADMINS.append(OWNER_ID)
ADMINS.append(1250450587)  # Additional admin ID if needed

# Force subscribe message
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join my Channel/Group to use me\n\nKindly Please join the Channel</b>")

# Custom Caption for files (optional)
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

# Prevent forwarding files from the bot
PROTECT_CONTENT = os.environ.get('PROTECT_CONTENT', "False").lower() == "true"

# Auto-delete files after a certain time (in seconds)
try:
    AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "0"))
except ValueError:
    AUTO_DELETE_TIME = 0
AUTO_DELETE_MSG = os.environ.get("AUTO_DELETE_MSG", "This file will be automatically deleted in {time} seconds. Please ensure you have saved any necessary content before this time.")
AUTO_DEL_SUCCESS_MSG = os.environ.get("AUTO_DEL_SUCCESS_MSG", "Your file has been successfully deleted. Thank you for using our service. ✅")

# Disable the Share button on Channel Posts
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", "False").lower() == "true"

# Bot uptime and user reply text
BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly! I'm only a File Share bot!"

# Log file settings
LOG_FILE_NAME = "filesharingbot.txt"

# Setting up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)

# Set the logging level for pyrogram to avoid excessive logs
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Logger function for easy access in other files
def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
