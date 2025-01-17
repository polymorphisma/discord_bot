# Discord Bot

### Set up
```
poetry shell
poetry install
```

### Set Variable in .env
1. Create `.env` file
2. Copy All variable from `.env.example` and paste it in `.env`
3. Enter valid values in `.env`

### Run script
```python
python discord_bot.py
```

Right now this is just for the custom use. I have created another file for my use case to generate message(`find_who_is_out.py`). if you just want to build bot to send message change `MESSAGE` portion on `discord_bot.py` line `19`.
