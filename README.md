# Telegram чат-бот для отправки уведомлений о проверке работ на онлайн-курсе для веб-разработчиков Devman

Бот отправляет уведомления о проверке работ на онлайн-курсе [dvmn.org](https://dvmn.org/). Используется технология long polling для проверки наличия новой информации на сервере. Коммуникация между ботом и сайтом с помощью API. Обработаны исключительные ситуации - бот присылает трейсбек в Telegram. 


### Как установить

1. Обзаведитесь сервером, для этого зарегистрируйте приложение на сайте [Heroku](https://id.heroku.com/login).
2. Скопируйте репозиторий в Ваш аккаунт [GitHub](https://github.com/).
3. Привяжите Ваш аккаунт [GitHub](https://github.com/) к аккаунту [Heroku](https://id.heroku.com/login). Привязать можно на вкладке `Deploy`. Потом найти свой репозиторий с помощью поиска и подключите его к `Heroku`. Нажать `Deploy Branch` внизу страницы, в итоге загорятся зелёные галочки справа.

4. Для работы бота потребуются следующие переменные:
   - `TELEGRAM_BOT_TOKEN` — `API` ключ бота;
   - `TELEGRAM_CHAT_ID` — `id` номер Вашего `Telegram` аккаунта;
   - `DEVMAN_AUTHORIZATION_TOKEN` — токен авторизации к сайту [Devman](https://dvmn.org/).
   
   Зарегистрируйте бота в `Telegram`. Для этого напишите [Отцу ботов](https://telegram.me/BotFather). Используйте команды: `/start` и `/newbot`.
   Чтобы получить свой `id` номер `Telegram` аккаунта, напишите в Telegram специальному боту: `@userinfobot`.
   Токен авторизации к сайту [Devman](https://dvmn.org/) находится в документации к [API Devman](https://dvmn.org/api/docs/).
   Переменные окружения задайте во вкладке `Settings` на сайте [Heroku](https://id.heroku.com/login), заполнив `Config Vars`.

5. Python3 должен быть уже установлен. 
   Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
   ```
   pip install -r requirements.txt
   ```

Для запуска бота нажмите кнопку `Open app` в верхнем правом углу сайта [Heroku](https://id.heroku.com/login).


### Пример запуска скрипта

Команда запуска: `python manage.py`

Пример результата:

![](https://github.com/Piar1986/devman_notifications_bot/raw/master/result_example.png)


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).