# ratbot

welcome to rat bot

inquire support here: <https://discord.gg/VH9vshpXAv>

## setup

requirements: `python`/`pip` >= 3.12, `git`. Windows and other non-Linux systems
are not intentionally supported, but if they do work, nice

```sh
$ git clone "https://github.com/ernieIzde8ski/ratbot.git" -b 2024-rewrite
$ cd ratbot
  # optional, stops you from cluttering your usual site-packages
$ python -m venv venv; . venv/bin/activate
$ python -m pip install -r requirements.txt
```

### environment variables

```sh
# Optional: directory containing a .env file and/or config.yaml
# Has no effect if set within .env file
RATBOT_CONFIG_DIR="$XDG_CONFIG_DIR/ratbot"

# Required; a Discord bot token with messages intents.
RATBOT_TOKEN_DISCORD=""
# Optional; `logging` level.
# Options: DEBUG, INFO, WARNING, ERROR
RATBOT_LOG_LEVEL="INFO"
```

### config.yaml

Optional file.

## running

**After doing all of the above**, run `python .` to start the bot.
