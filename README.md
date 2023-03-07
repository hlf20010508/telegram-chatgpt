# telegram-chatgpt
> A telegram bot based using chatgpt.

Support text and voice input.

## bot command
- `/start` to start with bot
- `/forget` to remove all memory
- `/reset A SENTENCE ABOUT BOT'S CHARACTER` to reset character background
- `/help` for help

## launch through docker
```sh
# install docker-compose
sudo apt-get install docker-compose
# modify environment args in docker-compose.yml
# telegram: token
# openai: api_key
# optional:
# start_text (a message sent to user after using /start)
# model (chatgpt version)，preset (self introduction, eg: You're my friend), memory_length (default 100, < 0 for unlimit)
# in preset, the subject is chatgpt, eg: I'm Marry, You're Mike. so chatgpt is Marry, you are Mkie.
# don't use quotation marks for preset in docker-compose.yml, but in system environmant setting.
vim docker-compose.yml
# launch
sudo docker-compose up -d
```

build your docker image
```sh
sudo docker build -t YOUR_HOST_NAME/wechat-chatgpt --no-cache .
```

## launch directly
```sh
# install pipenv
pip install pipenv
# install dependences
pipenv sync
# set environment args
export token=$token
export api_key=$api_key
# optional
export preset=$preset
# launch
pipenv run python bot.py
```
