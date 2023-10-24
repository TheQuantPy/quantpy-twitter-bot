# quantpy-twitter-bot

This project utilises Chat GPT to generate twitter (X) posts from a list of quantitative python ideas with a specific template file. Tweets will be posted daily.

## To Run on Server

Some basic Git commands are:

```
sudo chmod 644 /lib/systemd/system/twitter_bot.service
chmod +x /home/quantpy/quantpy-twitter-bot/main.py
sudo systemctl daemon-reload
sudo systemctl enable twitter_bot.service
sudo systemctl start twitter_bot.service
```

To check status:

```
sudo systemctl status twitter_bot.service
```

To stop service:

```
sudo systemctl stop twitter_bot.service
```

To check service logs:

```
sudo journalctl -f -u twitter_bot.service
```

> [!NOTE]
> Important that twitter_bot.service file is [installed properly](https://gist.github.com/emxsys/a507f3cad928e66f6410e7ac28e2990f) on host server
