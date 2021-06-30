const fs = require('fs');

const weather_resps = {
    "greetings": ["Good morning {},", "Dzień dobry {},"],
    "temperature_resps": [
        [0, "It is below 0 degrees celsius."],
        [100, "It is below 100 degrees celsius."],
        [1000, "At this temperature, water boils."]
    ]
};

const songs = {
    "dQw4w9WgXcQ": "Rick Astley — Never Gonna Give You Up"
};

writeWeatherResps = () => {
    fs.writeFile("./data/weather_resps.json", JSON.stringify(weather_resps), err => console.error);
    fs.writeFile("./data/songs.json", JSON.stringify(songs), err => console.error);
};

if (require.main === module) {
    writeWeatherResps();
}

module.exports = writeWeatherResps;