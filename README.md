# Devman_santa_bot

Telegram bot for Secret Santa. 
The bot allows you to create a link to the game, which can be sent to any Telegram user.
The user follows the link and registers in the game, filling in the necessary data. After the registration for the game is closed (this is a certain date specified in the game), there is a random selection of a secret Santa for each participant.


## Enviroments

- create new bot in Telegram and get the token   
  (you can obtain bot from @BotFather in Telegram, [See example](https://telegra.ph/Awesome-Telegram-Bot-11-11))
- create the file .env and fill in this data:
  - TELEGRAM_TOKEN
  - DEBUG
  - SECRET_KEY
  - ALLOWED_HOSTS


## Installing

To get started go to terminal(mac os) or CMD (Windows)
- create virtualenv, [See example](https://python-scripts.com/virtualenv)

- clone github repository or download the code

```bash
$git clone https://github.com/konakov-ds/devman_santa_bot.git
```

- install packages

```bash
$pip install -r requirements.txt
```
  
- set up Database as it described below

- for Admin access to create super user 

```bash
$python manage.py createsuperuser"
```

- run the local server and pass to `http://127.0.0.1:8000/admin` to login to admin webpage
```bash
python manage.py runserver
```

- run the bot with command below and pass to your bot chat in Telegram

```bash
$python manage.py tg_bot
```

## Working with Database 
- Go to the app folder

```bash
$cd santa_bot
```

- run the following commands to migrate models into DB:
```bash
python3 manage.py makemigrations
```

```bash
$python manage.py migrate 
```


P.S: Please note that the code in the bot.py file has the names that you wrote on the admin page.

## Authors

* **Mark** - [Mark](https://github.com/konakov-ds)
* **Rostislav** - [Rostislav](https://github.com/Rostwik)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


