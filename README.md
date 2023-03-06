# telegram-chatgpt
> A telegram bot based using chatgpt.

## bot command
- `/start` to start with bot
- `/forget` to remove all memory
- `/reset A SENTENCE ABOUT BOT'S CHARACTER` reset character background

## launch through docker
```sh
# install docker-compose
sudo apt-get install docker-compose
# modify environment args in docker-compose.yml
# telegram: token
# openai: api_key
# optional:
# start_text (a message sent to user after using /start)
# model (chatgpt version)，preset (background, eg: "You're my assistant."), memory_length (default 100, < 0 for unlimit)
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
# launch
pipenv run python bot.py
```
