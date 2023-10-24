# quantpy-twitter-bot

This project utilises Chat GPT to generate twitter (X) posts from a list of quantitative python ideas with a specific template file.

Tweets will be posted every 12 hours using apscheduler module in python, callable from the the linux operating system services.

We can check the status, stop or start the service from the command line, and we also have access to the logs generated from the twitter bot.

## To Run on Server/Raspberry Pi

### Step 1: download github repo to server or raspberry pi

```
git clone https://github.com/TheQuantPy/quantpy-twitter-bot.git
```

### Step 2: setup

> [!NOTE]
> Important that twitter_bot.service file is [installed properly](https://gist.github.com/emxsys/a507f3cad928e66f6410e7ac28e2990f) on host server

We will run out twitter bot script as a service in the operating system so it can hva the following functionality:

- start,
- stop,
- restart, and
- status.

We will setup our bot script as a service using [linux operating system sysemd](https://wiki.archlinux.org/title/systemd), which can be commanded using <i>systemctl</i>.

#### 2a. Setting up the service to run our script in daemon mode on the server:

```
cd /lib/systemd/system/
sudo nano twitter_bot.service
```

#### 2b. Add the Following Text and save the service file:

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

#### 2c. Now that we have our service we need to activate it:

```
sudo chmod 644 /lib/systemd/system/twitter_bot.service
chmod +x /home/quantpy/quantpy-twitter-bot/main.py
sudo systemctl daemon-reload
sudo systemctl enable twitter_bot.service

```

#### 2d. Now we can access the following commands

To start service:

```
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
