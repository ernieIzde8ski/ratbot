const cache = require('../data/xkcd.json');
var latest = cache[cache.length - 1];

var difference = 1;
var errors = 0;

for (var i = 0; i <= latest.int; i++) {
    if (!cache[i]) {
        continue;
    }
    var expected = i + difference;
    if (cache[i].int == expected) continue;
    else {
        difference += 1;
        if (expected == 404) continue;
        console.log(`Error: Found ${cache[i].int}, expected ${expected}`);
        errors += 1;
    }
}

console.log(`${errors} error(s) found in XKCD cache`);
