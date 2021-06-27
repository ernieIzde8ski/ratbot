#!/bin/bash
git pull

echo ".env variables:"

echo "Ensure all intents are enabled under https://discord.com/developers"
read -p "Discord bot token:  " TOKEN
if [ -n "$TOKEN" ] ; then
    echo "DISCORD_TOKEN=$TOKEN" > .env
    echo "Set DISCORD_TOKEN to '$TOKEN'"
else
    echo "Error: DISCORD_TOKEN is a required value"
    exit 1
fi

echo "A weather token is an API key from https://openweathermap.org/api"
echo "Type nothing to skip"
read -p "Weather token:  " TOKEN
if [ -n "$TOKEN" ] ; then
    echo "WEATHER_TOKEN=$TOKEN" >> .env
    echo "Set WEATHER_TOKEN to $TOKEN"
else
    echo "Not setting WEATHER_TOKEN value"
    echo "Remember to remove on_member_update.weather_updates from enabled_extensions.json"
fi

mkdir data
mkdir data/temporary

echo "Generating the XKCD cache will spam the console & requires node.js"
read -p "Generate XKCD cache?  " BOOL
if [ -z "$BOOL" ] ; then
    echo "No input; continuing"
else
    CHARACTER=${BOOL:0:1}
    if [[ "$CHARACTER" == "y" || "$CHARACTER" == "Y" ]]; then
        node modules/xkcd_cache_generator.js
        node modules/xkcd_cache_checker.js
    else
        echo "Continuing"
    fi
fi

pip install -r requirements.txt

if (( $? == 0 )); then
    echo 'Installed modules successfully'
else
	pip3 install -r requirements.txt
    if (( $? == 0 )); then
        echo 'Installed modules successfully'
    else
        echo 'An error occurred in installing modules'
        echo 'Ensure pip is installed and run \"pip install -r requirements.txt\" afterwards'
    fi
fi
