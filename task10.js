# UI Kit для итогового проекта

## 📁 Структура проекта

```
ui-kit/
├── index.html                # Документация с примерами компонентов
├── css/
│   ├── reset.css
│   ├── variables.css         # Цвета, размеры, шрифты
│   └── styles.css            # Общие и компонентные стили
├── scss/
│   ├── _variables.scss
│   ├── _buttons.scss
│   ├── _inputs.scss
│   ├── _cards.scss
│   ├── _navbar.scss
│   └── main.scss             # Основной файл импорта
├── components/
│   ├── button.html
│   ├── input.html
│   ├── card.html
│   ├── navbar.html
│   └── grid.html
└── assets/
    └── images/               # Изображения для карточек
```

---

## ✅ Реализованные компоненты

### 🔘 Кнопки

* Варианты: `primary`, `secondary`, `disabled`
* Размеры: `small`, `medium`, `large`
* Состояния: `hover`, `active`, `focus`
* БЭМ: `button`, `button--primary`, `button--disabled`, `button--large`

### 📝 Поле ввода

* Состояния: `normal`, `focus`, `error`
* Возможность вставки иконки слева или справа
* Сообщение об ошибке отображается под полем
* БЭМ: `input`, `input--error`, `input__icon`

### 🃏 Карточки

* Содержат: заголовок, изображение (опционально), описание
* Модификаторы: `card--small`, `card--with-image`, `card--no-image`
* Используются внутри сетки

### 📚 Навигация

* Горизонтальное меню (десктоп)
* Гамбургер-меню (мобильное)
* Включает иконки и выпадающие секции
* БЭМ: `navbar`, `navbar__item`, `navbar--mobile`

### 📐 Макеты

* Контейнер с центровкой по горизонтали и вертикали (Flexbox)
* Галерея карточек с помощью CSS Grid

---

## 🎨 SCSS и CSS

* Все переменные вынесены в `variables.scss`
* Использован `normalize.css`
* Каждый компонент — отдельный файл с именованием по БЭМ

---

## 📄 Документация (index.html)

На странице `index.html` представлены:

* Все компоненты UI Kit с заголовками и подписями;
* Кнопки в трёх размерах и состояниях;
* Поля ввода с и без ошибок;
* Карточки с изображением и без;
* Навигационное меню в двух режимах;
* Flex и Grid-сетки с примерами использования.

---

## 🔗 Репозиторий

[https://github.com/your-username/ui-kit-final](https://github.com/your-username/ui-kit-final)
