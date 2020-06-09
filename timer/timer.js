
const el = (id) => document.getElementById(id);

const timeSpan = el("timer");


function startTimer() {
    const mins = 0.5;
    const now = Date.now();
    const deadline = mins * 60 * 1000 + now;

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
    timeSpan.innerHTML = "30";
}

el("startButton").onclick = startTimer;
