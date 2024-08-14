class PomodoroTimer {
    constructor() {
        this.root = document.getElementById("pomodoro-app");
        this.workTime = 25 * 60;
        this.shortBreakTime = 5 * 60;
        this.longBreakTime = 15 * 60;
        this.isWorkTime = true;
        this.pomodorosCompleted = 0;
        this.isRunning = false;
        this.timerInterval = null;

        this.timerLabel = document.createElement("div");
        this.timerLabel.style.fontSize = "40px";
        this.root.appendChild(this.timerLabel);

        this.startButton = document.createElement("button");
        this.startButton.innerHTML = '<i class="material-icons">play_arrow</i>';
        this.startButton.onclick = () => this.startTimer();
        this.root.appendChild(this.startButton);

        this.stopButton = document.createElement("button");
        this.stopButton.innerHTML = '<i class="material-icons">stop</i>';
        this.stopButton.disabled = true;
        this.stopButton.onclick = () => this.stopTimer();
        this.root.appendChild(this.stopButton);

        this.extractButton = document.createElement("button");
        this.extractButton.innerHTML = '<i class="material-icons">open_in_new</i>';
        this.extractButton.onclick = () => this.extractTimer();
        this.root.appendChild(this.extractButton);

        this.updateTimer();
    }

    startTimer() {
        this.startButton.disabled = true;
        this.stopButton.disabled = false;
        this.isRunning = true;
        if (!this.timerInterval) {
            this.timerInterval = setInterval(() => this.updateTimer(), 1000);
        }
    }

    stopTimer() {
        this.startButton.disabled = false;
        this.stopButton.disabled = true;
        this.isRunning = false;
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }

    updateTimer() {
        const time = this.isWorkTime ? this.workTime : this.breakTime;
        const minutes = Math.floor(time / 60);
        const seconds = time % 60;
        this.timerLabel.innerText = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

        if (this.isRunning) {
            if (this.isWorkTime) {
                this.workTime -= 1;
                if (this.workTime === 0) {
                    this.isWorkTime = false;
                    this.pomodorosCompleted += 1;
                    this.breakTime = this.pomodorosCompleted % 4 === 0 ? this.longBreakTime : this.shortBreakTime;
                    alert(this.pomodorosCompleted % 4 === 0 ? "Take a long break!" : "Take a short break!");
                }
            } else {
                this.breakTime -= 1;
                if (this.breakTime === 0) {
                    this.isWorkTime = true;
                    this.workTime = 25 * 60;
                    alert("Work time!");
                }
            }
        }
    }

    extractTimer() {
        const floatingTimer = document.createElement("div");
        floatingTimer.style.position = "fixed";
        floatingTimer.style.bottom = "10px";
        floatingTimer.style.right = "10px";
        floatingTimer.style.padding = "10px";
        floatingTimer.style.backgroundColor = "black";
        floatingTimer.style.color = "white";
        floatingTimer.style.fontSize = "20px";
        floatingTimer.style.borderRadius = "5px";
        floatingTimer.style.zIndex = 1000;

        const timerLabel = document.createElement("div");
        timerLabel.innerText = this.timerLabel.innerText;
        floatingTimer.appendChild(timerLabel);

        const closeButton = document.createElement("button");
        closeButton.innerHTML = "&times;";
        closeButton.style.marginLeft = "10px";
        closeButton.onclick = () => floatingTimer.remove();
        floatingTimer.appendChild(closeButton);

        document.body.appendChild(floatingTimer);

        this.timerInterval = setInterval(() => {
            timerLabel.innerText = this.timerLabel.innerText;
        }, 1000);
    }
}

document.addEventListener("DOMContentLoaded", () => new PomodoroTimer());

// Individual timer functions
function startITimer(timerId) {
    console.log(`Starting timer ${timerId}`);
    // Implement the start logic for individual timers
}

function pauseITimer(timerId) {
    console.log(`Pausing timer ${timerId}`);
    // Implement the pause logic for individual timers
}

function resetITimer(timerId) {
    console.log(`Resetting timer ${timerId}`);
    // Implement the reset logic for individual timers
}
