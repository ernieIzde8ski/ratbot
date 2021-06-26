# ratbot.py

The main Pythonic rat, a Discord bot developed by ernieIzde8ski

## Requirements

- Python & Pip
  - The next section installs the required modules
- Node.js (Optional)

## Running the code

- OS:
  - Windows: `bash`; continue
  - Linux: continue
  - Mac: No lmao
- `git clone https://github.com/ernieIzde8ski/ratbot.git rat.py -b rewrite`
- `cd rat.py`
- `mkdir data`
- `mkdir data/temporary`
- `nano .env`
  - Copypaste, format, and save the .env format below
- `nano config.json` (Highly recommended)
  - Edit configs & change channel IDs to channels your bot application has access to
- `node modules/xkcd_cache_generator` (Optional, will spam logs)
  - For whatever reason, the code occasionally times out, depending on your luck; thus:
  - `node modules/xkcd_cache_checker` to see what XKCDs didn't get cached (not finding 404 is normal)
- `pip install -r requirements.txt` (or `pip3` on certain systems)
- `python bot.py`

### .env file

```Shell
# Token for a Discord bot application: https://discord.com/developers/applications
# Ensure all intents are enabled
DISCORD_TOKEN=token
# API key from https://openweathermap.org/api
# This is required in the weather cog, but that can be
# disabled like any other extension in enabled_extensions.json
WEATHER_TOKEN=apikey
```

### config.json

```JSONC
{   
    // Prefix to interpret commands with
    // either list[str] or str 
    "prefix": ["r.", "r!"],
    // PYTZ-compatible timezone
    // see https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
    "preferred_timezone": "EST",
    // Channel IDs to send various messages to
    "channels": {
        "BMs": 762166605458964510,
        "DMs": 715297562613121084,
        "Status": 708882977202896957,
        "Guilds": 841863106996338699
    }
}
```

#### See CONFIGS.md for the various files generated in data/
