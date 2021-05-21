# ratbot

Source code for ratbot, programmed by ernieIzde8ski; contributions also made by myerfire

## Support

- [Discord (ernieizde8ski#4571)](https://discord.gg/cHZYahK)

## How to run it the code

- `git clone https://github.com/ernieIzde8ski/ratbot.git`
- `cd ratbot`
- `pip install -r requirements.txt` (or `pip3` if applicable)
- Create a configs/secrets.py file in with the parameters listed below
- Modify `configs/config.py`, `configs/enabled_cogs.py` [optional, recommended]
- `python bot.py`

## secrets.py Parameters

Create a `secrets.py` file in the configs directory. List of current variables:

```python
token = ""
tenor_api_key = ""
hypixel_api_key = ""
weather_api_key = ""
```

- `token` is a Discord bot token; required
  - retrieve from discord developer panel, do not forget to enable all intents
- `tenor_api_key` is a Tenor.com API key.
  - used only in cogs/tenor.py
- `hypixel_api_key` is a Hypixel API key.
  - used only in cogs/hypixel.py
- `weather_api_key` is an openweathermap.org API key.
  - used only in cogs/on_member_update/Armenium.py

#### *All variables other than `token` are optional if not loading the respective cog*
