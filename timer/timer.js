// NB check out:
// https://medium.com/@abhi9bakshi/why-javascript-timer-is-unreliable-and-how-
// can-you-fix-it-9ff5e6d34ee0

// CLIENT SIDE
const el = (id) => document.getElementById(id);

const timeSpan = el("timer");

// SERVER SIDE
const mins = 0.5;
const now = Date.now(); // difference between .getTime() and .now() ??
const deadline = mins * 60 * 1000 + now;

// why use var here?
var timerID = setInterval(function () {
    var currentTime = Date.now();
    var distance = deadline - currentTime;
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    if (parseInt(seconds) === 0) {
        clearInterval(timerID);
        // send message that timer has run out here
    }
    timeSpan.innerHTML = seconds;
    // rather than change html, the server will send
    // JSON.stringify({"timer": seconds})
}, 500);

