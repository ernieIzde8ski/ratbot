// I stole this code from myself
// what you gon do about it, Punk

const isInteger = number => number == Math.floor(number);

module.exports = (start = 0, stop = null, step = null) => {
    if (stop == null) {
        stop = start;
        start = 0;
    } if (step == null) {
        if (start < stop) step = 1;
        else step = -1;
    }

    if (!isInteger(start) || !isInteger(stop)) throw Error("Range values must be integers");
    if (!isInteger(step) || step == 0) throw Error("Step value must be an integer other than 0");

    var list = [];
    if (step > 0) {
        for (i = start; i < stop; i += step) {
            list.push(i);
        }
    } else {
        for (i = start; i > stop; i += step) {
            list.push(i);
        }
    }
    return list;
};