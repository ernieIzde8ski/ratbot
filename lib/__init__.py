import logging
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from .bot import *
from .converters import *
from .settings import *
from .setup import load_environment, load_extensions, setup_logging
from .temporary_attachment_holder import TemporaryAttachmentHolder
