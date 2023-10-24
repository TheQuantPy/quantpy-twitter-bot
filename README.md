# quantpy-twitter-bot

This project utilises Chat GPT to generate twitter (X) posts from a list of quantitative python ideas with a specific template file. Tweets will be posted every 12 hours using apscheduler module in python, callable from the server daemon services.

## To Run on Server

Setting up the service to run our script in daemon mode on the server:

```
cd /lib/systemd/system/
sudo nano twitter_bot.service
```

Add the Following Text and save the service file:

```
[Unit]
Description=QuantPy Twitter Bot Service
After=multi-user.target

[Service]
Type=simple
ExecStart=/home/quantpy/quantpy-twitter-bot/env/bin/python /home/quantpy/quantpy-twitter-bot/main.py
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

Now that we have our service we need to activate it:

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
