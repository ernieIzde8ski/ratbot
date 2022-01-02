// Note: use npm install node-fetch@2 to install
const fetch = require("node-fetch");
const fs = require('fs');
const range = require('./javascript/range');


get_xkcd = async int => {
    if (int == -1) {
        url = "https://xkcd.com/info.0.json";
    } else {
        url = `https://xkcd.com/${int}/info.0.json`;
    }
    try {
        resp = await fetch(url);
    } catch (e) {
        console.log(`Error on ${url}`);
        return {
            error: e
        };
    }

    try {
        resp = await resp.json();
    } catch (e) {
        resp = {
            error: e
        };
    }
    return resp;
};

get_xkcds = async () => {
    const latest = await get_xkcd(-1);
    console.log("Going up to", latest.num);
    const xkcd_range = range(stop = latest.num + 1);
    let arr_0 = [];

    // Populate the array
    for (const i of xkcd_range) {
        arr_0.push(get_xkcd(i).then(comic => {
            if (comic.num % 50 == 0) console.log(comic.num + ":", comic.title);
            return comic;
        }));
    }

    // Wait for the array to Finish
    arr_0 = await Promise.all(arr_0);

    // Return the filtered array
    return arr_0.filter(comic => !comic.error).map(comic => {
        return {
            name: comic.title,
            alt: comic.alt,
            int: comic.num,
        }
    });
};

if (require.main === module) {
    get_xkcds()
        .then(list => {
            list = JSON.stringify(list);
            fs.writeFile("./data/xkcd.json", list, err => console.error);
        });
}