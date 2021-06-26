const fetch = require("node-fetch");
const fs = require('fs');
const range = require('./javascript/range');


var data = [];

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
        return { error: e };
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

get_xkcds = async int => {
    var list = [];
    var latest = await get_xkcd(-1);
    var xkcds = range(stop = latest.num + 1);

    for (var xkcd of xkcds) {
        xkcd = await get_xkcd(xkcd);
        if (xkcd.error) continue;
        list.push(xkcd);
        console.log(xkcd.num, xkcd.title);
    }
    return list.map(item => {
        return {
            name: item.title,
            alt: item.alt,
            int: item.num

        };
    });
};

if (require.main === module) {
    console.log('called directly');

    get_xkcds()
        .then(list => {
            list = JSON.stringify(list);
            fs.writeFile("../data/xkcd.json", list, callback => "");
        });

}