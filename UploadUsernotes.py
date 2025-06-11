import praw
import base64
import zlib
import json
import logging
from datetime import datetime
import config  # Your credentials
from prawcore.exceptions import Forbidden, TooManyRequests

# === Logging ===
logging.basicConfig(
    filename='error_log.txt',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
logger = logging.getLogger()

# === Reddit API Setup ===
reddit = praw.Reddit(
    client_id=config.source_client_id,
    client_secret=config.source_client_secret,
    username=config.source_username,
    password=config.source_password,
    user_agent=config.source_user_agent
)

# === Config ===
SUBREDDIT_NAME = 'ufos'
WIKI_PAGE = 'usernotes'

# === Functions ===

def backup_usernotes(subreddit):
    try:
        wiki = subreddit.wiki[WIKI_PAGE]
        today = datetime.now().strftime('%Y%m%d')
        backup_filename = f'usernotes_backup-{today}.txt'
        with open(backup_filename, 'w', encoding='utf-8') as f:
            f.write(wiki.content_md)
        print(f"Backup saved as {backup_filename}")
        return backup_filename, wiki.content_md
    except Forbidden:
        logger.error(f"Access denied to /r/{SUBREDDIT_NAME}/wiki/{WIKI_PAGE}")
    except TooManyRequests:
        logger.error("Rate limit exceeded. Exiting.")
        exit(1)
    except Exception as e:
        logger.error(f"Error downloading wiki page: {e}")
    return None, None

def compress_blob(json_str):
    try:
        compressed = zlib.compress(json_str.encode())
        encoded = base64.b64encode(compressed).decode()
        return encoded
    except Exception as e:
        logger.error(f"Compression failed: {e}")
        return None

def update_wiki(subreddit, new_content):
    try:
        subreddit.wiki[WIKI_PAGE].edit(new_content, reason="Updated via script")
        print(f"Successfully updated r/{SUBREDDIT_NAME}/wiki/{WIKI_PAGE}")
    except Exception as e:
        logger.error(f"Failed to update wiki page: {e}")

# === Main Script ===

subreddit = reddit.subreddit(SUBREDDIT_NAME)

# Step 1: Backup
backup_filename, original_wiki_content = backup_usernotes(subreddit)
if not original_wiki_content:
    print("Could not fetch original wiki content. Exiting.")
    exit(1)

# Step 2: Ask for new file
edited_filename = input("Enter the filename of the edited decompressed usernotes (e.g. decompressed_usernotes_edited.txt): ").strip()

try:
    with open(edited_filename, 'r', encoding='utf-8') as f:
        new_blob_json = f.read()
except FileNotFoundError:
    print(f"File not found: {edited_filename}")
    exit(1)

# Step 3: Compress and encode the blob
encoded_blob = compress_blob(new_blob_json)
if not encoded_blob:
    print("Compression failed. Exiting.")
    exit(1)

# Step 4: Replace the blob in the original wiki JSON
try:
    wiki_data = json.loads(original_wiki_content)
    wiki_data['blob'] = encoded_blob
    updated_content = json.dumps(wiki_data)
except Exception as e:
    print(f"Error preparing updated wiki content: {e}")
    logger.error(f"Error replacing blob: {e}")
    exit(1)

# Step 5: Upload
update_wiki(subreddit, updated_content)
