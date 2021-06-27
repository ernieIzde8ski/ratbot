# ratbot.py

The main Pythonic rat, a Discord bot developed by ernieIzde8ski

## Requirements

- Python, pip
- Node.js (Optional)

## Running the code

- OS:
  - Windows: `bash`; continue
    - if this doesn't work, good luck
  - Linux: continue
  - Mac: No lmao
- `git clone https://github.com/ernieIzde8ski/ratbot.git rat.py -b rewrite`
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

<!--
commented out until i actually make CONFIGS.md Lol 
#### See CONFIGS.md for the various files generated in data/ 
-->
