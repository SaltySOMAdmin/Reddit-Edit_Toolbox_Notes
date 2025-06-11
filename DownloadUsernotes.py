import praw
import base64
import zlib
import json
import logging
import config  # Your credentials

from prawcore.exceptions import Forbidden, TooManyRequests

# Set up logging
logging.basicConfig(
    filename='error_log.txt',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s'
)
logger = logging.getLogger()

# Config
NOTES_FILE_PATH = 'usernotes.txt'            # Raw wiki page markdown
DECOMPRESSED_NOTES_PATH = 'decompressed_usernotes.txt'  # Decompressed JSON text
SUBREDDITS_LIST = ['ufos']

# Reddit API credentials
reddit = praw.Reddit(
    client_id=config.source_client_id,
    client_secret=config.source_client_secret,
    username=config.source_username,
    password=config.source_password,
    user_agent=config.source_user_agent
)

# Start definitions
def save_usernotes(reddit, subreddit_name):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        usernotes_page = subreddit.wiki['usernotes']
        with open(NOTES_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(usernotes_page.content_md)
        logger.info(f"Saved wiki content for r/{subreddit_name}")
        return usernotes_page.content_md
    except Forbidden:
        logger.error(f"Access denied to r/{subreddit_name}/wiki/usernotes")
    except TooManyRequests:
        logger.error("Rate limit exceeded. Exiting.")
        exit(1)
    except Exception as e:
        logger.error(f"Error fetching usernotes for r/{subreddit_name}: {e}")
    return None


def decompress_notes(notes_blob):
    try:
        decoded = base64.b64decode(notes_blob)
        decompressed = zlib.decompress(decoded).decode()
        return decompressed
    except Exception as e:
        logger.error(f"Decompression failed: {e}")
        return None

# Start of script 
for subreddit_name in SUBREDDITS_LIST:
    print(f"Fetching modnotes from r/{subreddit_name}...")
    wiki_content = save_usernotes(reddit, subreddit_name)
    if wiki_content:
        try:
            toolbox_notes = json.loads(wiki_content)
            blob = toolbox_notes.get('blob')
            if blob:
                print("Decompressing modnotes blob...")
                decompressed_text = decompress_notes(blob)
                if decompressed_text:
                    with open(DECOMPRESSED_NOTES_PATH, 'w', encoding='utf-8') as f:
                        f.write(decompressed_text)
                    print(f"Decompressed notes saved to {DECOMPRESSED_NOTES_PATH}")
                else:
                    logger.info("Failed to decompress blob.")
            else:
                logger.info("No blob found in usernotes.")
        except Exception as e:
            logger.error(f"Error processing wiki content: {e}")
    else:
        logger.info(f"No content found for r/{subreddit_name}")
