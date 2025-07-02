<!-- Стартовая точка проекта -->
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Приложение с авторизацией и Service Worker</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header>
    <span id="auth-status">Вы не авторизованы</span>
    <button id="logout-btn" hidden>Выйти</button>
  </header>

  <main>
    <form id="login-form">
      <input type="email" id="email" placeholder="Email" required />
      <input type="password" id="password" placeholder="Пароль" required minlength="6" />
      <button type="submit">Войти</button>
    </form>
    <div id="offline-message" hidden>Вы в офлайн-режиме</div>
  </main>

  <script src="app.js"></script>
  <script>
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js')
          .then(reg => console.log('SW зарегистрирован:', reg.scope))
          .catch(err => console.error('SW ошибка:', err));
      });
    }
  </script>
</body>
</html>
