# ensure the logging format works, firstly
from discord.utils import setup_logging

setup_logging()

# start imports
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from utils import RatBot

# loading secrets
denv_path = Path(__file__).parent / ".env"
if denv_path.exists():
    load_dotenv(denv_path, override=True, verbose=True)

TOKEN = getenv("RATBOT_TOKEN")
if not TOKEN:
    raise RuntimeError("RATBOT_TOKEN is not set")

# instantiating client
from settings import settings

rat = RatBot(command_prefix=settings.get_prefix)

rat.run(TOKEN)
