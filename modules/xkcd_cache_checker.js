const cache = require('./xkcd_cache.json');
var latest = cache[cache.length - 1];

var difference = 1;
for (var i=0; i <= latest.int; i++) {
    if (!cache[i]) {
        continue;
    }
    var expected = i + difference;
    if (cache[i].int == expected) continue;
    else {
        console.log(`Error: Found ${cache[i].int}, expected ${expected}`);
        difference += 1;
    }
}