# ratbot.py

The main Pythonic rat, a Discord bot developed by ernieIzde8ski

## Requirements

- Python, pip
- Node.js (Optional)

## Running the code

- OS:
  - Windows: run `bash`; continue
    - if this doesn't work, good luck
  - Linux, Mac: continue
- `git clone https://github.com/ernieIzde8ski/ratbot.git rat.py`
- `cd rat.py`
- `./initialize.sh`
- `nano config.json` (Highly recommended)
  - format below
  - edit loaded cogs with `nano enabled_extensions.json`
- `python bot.py`

### config.json

```JSONC
{   
    // Prefix to interpret commands with
    // either list[str] or str 
    "prefix": ["r.", "r!"],
    // status used in initialization, where {} becomes the prefix
    // used in cogs/events/stati.py
    "default_status": "{}help",
    // PYTZ-compatible timezone
    // see https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
    "preferred_timezone": "EST",
    // link to a repo
    // used in cogs/commands/info.py
    "github": "https://github.com/ernieIzde8ski/ratbot",
    // invite to a server
    // used in cogs/commands/info.py
    "invite": "https://discord.gg/3gfP2kYPp4",
    // id of the server that cogs/events/weather_updates.py checks
    "main_guild": 488475203303768065,
    // Channel IDs to send various messages to
    "channels": {
        "BMs": 762166605458964510,
        "DMs": 715297562613121084,
        "Status": 708882977202896957,
        "Guilds": 841863106996338699
    }
}
```

#### See [CONFIGS.md](CONFIGS.md) for the various files generated in ./data/
