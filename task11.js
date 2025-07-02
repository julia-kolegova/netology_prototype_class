// Задание 1. Демонстрация Event Loop
console.log("1. Синхронный лог #1");

setTimeout(() => {
    console.log("4. setTimeout (macrotask queue)");
}, 0);

Promise.resolve()
    .then(() => console.log("2. Promise.then #1 (microtask queue)"))
    .then(() => console.log("3. Promise.then #2 (microtask queue)"));

console.log("5. Синхронный лог #2");


// Задание 2. Работа с Promise
function fetchData(url) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (url === "users") {
                resolve([{ id: 1, name: "Alice" }, { id: 2, name: "Bob" }]);
            } else if (url === "user/1") {
                resolve({ id: 1, name: "Alice", age: 25 });
            } else {
                reject("URL not found");
            }
        }, 2000);
    });
}

fetchData("users")
    .then(users => {
        console.log("Users:", users);
        return fetchData("user/1");
    })
    .then(user => console.log("User info:", user))
    .catch(err => console.error("Error:", err));


// Задание 3. Async/Await + delay
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function loadUserData() {
    try {
        await delay(2000);
        const users = await fetchData("users");
        console.log("Users (async):", users);

        await delay(1000);
        const user = await fetchData("user/1");
        console.log("User info (async):", user);
    } catch (err) {
        console.error("Async Error:", err);
    }
}

loadUserData();


// Задание 4. Прогресс-бар (HTML и JS нужно подключить в index.html)
// HTML:
// <div id="progress-container" style="width: 100%; background: #eee; height: 30px">
//   <div id="progress-bar" style="width: 0%; background: green; height: 100%"></div>
// </div>
// <p id="status"></p>

function startProgressBar() {
    const bar = document.getElementById("progress-bar");
    const status = document.getElementById("status");
    let percent = 0;

    const interval = setInterval(() => {
        percent += 20;
        bar.style.width = percent + "%";

        if (percent === 100) {
            clearInterval(interval);
            status.textContent = "Готово!";
        }
    }, 1000);
}

// вызов функции из JS, когда DOM готов
// window.onload = startProgressBar;


// Задание 5. Игра с таймерами (по желанию)
// HTML:
// <button id="reaction-btn" disabled>Нажми меня</button>
// <p id="reaction-status"></p>

let activationTime;
function startReactionGame() {
    const button = document.getElementById("reaction-btn");
    const status = document.getElementById("reaction-status");
    status.textContent = "Нажмите кнопку через 3 секунды...";

    const randomDelay = Math.floor(Math.random() * 5000) + 1000;

    setTimeout(() => {
        button.disabled = false;
        button.textContent = "Жми!";
        activationTime = Date.now();
    }, randomDelay);

    button.onclick = () => {
        if (!button.disabled) {
            const reactionTime = Date.now() - activationTime;
            status.textContent = `Ваша реакция: ${reactionTime} мс`;
            button.disabled = true;
            button.textContent = "Нажми меня";
        }
    };
}

// вызов функции: window.onload = startReactionGame;
