# Task Tracker Bot

**Task Tracker** — это Telegram-бот для управления задачами, с возможностью выгрузки данных в Google Sheets.  



## Функционал

- Добавление, просмотр и фильтрация задач по категориям
- Асинхронная выгрузка задач пользователя в Google Sheets
- Админская панель для управления экспортом
- Интеграция с PostgreSQL для хранения данных
- Использует Docker и Docker Compose для быстрого запуска



## Технологии

- Python 3.11
- Aiogram 3
- SQLAlchemy (асинхронный режим)
- PostgreSQL
- Google Sheets API
- Docker / Docker Compose
- RapidFuzz (поиск с учетом опечаток)
- Transliterate (генерация команд из названий задач)



## Структура проекта

bot/
├─ app/
│ ├─ auth.py
│ ├─ config.py
│ ├─ main.py
│ ├─ utils.py
│ ├─ backgound/
│ ├─ handlers/
│ ├─ keyboards/ 
│ ├─ db/ 
│ ├─ page/
│ └─ states/
├─ ... .json           #GoogleSheets API файл
├─ requirements.txt
└─ Dockerfile
docker-compose.yml
README.md
LICENSE
.gitignore
.env



## Запуск

### 1. Подготовьте .env файл с переменными:

BOT_TOKEN=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=
DATABASE_URL=

GOOGLE_SERVICE_ACCOUNT_JSON=                     !!! имя JSON файла GoogleSheets API, предварительно положить в bot/

ADMINS=[...]                                     !!! Список Телеграм ID админов

SPREADSHEET_ID=                                  !!! ID таблицы из URL


### 2. Разрешите боту изменять Вашу GoogleSheets

В скаченном файле JSON, по ключу "client_email" имя Вашего бота для GoogleSheets


### 3. Настройки поиска задач

bot/app/config.py


### 4. Команды

docker compose build
docker compose up



# Контакты

Telegram: @Xo4y_KyIIIaTb