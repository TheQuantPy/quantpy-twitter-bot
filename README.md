# quantpy-twitter-bot

This project automates the Twitter Feed of [QuantPy](https://twitter.com/TheQuantPy) using the OpenAI and Twitter API's.

<img src="https://github.com/TheQuantPy/quantpy-twitter-bot/blob/62a65c8480ca0da5410a7164b495a7392e8c9afd/data/images/raspberrypi_bot.jpg" width="30%"></img><img src="https://github.com/TheQuantPy/quantpy-twitter-bot/blob/a27da0ec7b7f078c089d12ae62a0b5000b770b11/data/images/quantpy_twitter_bot.png" width="30%"></img><img src="https://github.com/TheQuantPy/quantpy-twitter-bot/blob/3f7a351d7f7da2b70c96b94cdd76aaf1bf1b1c05/data/images/quantpy_twitter_console.png" width="30%"></img>
<img src="https://github.com/TheQuantPy/quantpy-twitter-bot/blob/3f7a351d7f7da2b70c96b94cdd76aaf1bf1b1c05/data/images/twitter_bot_logs.png" width="30%"></img><img src="https://github.com/TheQuantPy/quantpy-twitter-bot/blob/3f7a351d7f7da2b70c96b94cdd76aaf1bf1b1c05/data/images/twitter_jupyter_notebook.png" width="30%"></img><img src="https://github.com/TheQuantPy/quantpy-twitter-bot/blob/3f7a351d7f7da2b70c96b94cdd76aaf1bf1b1c05/data/images/twitter_prompt_engineering.png" width="30%"></img>

## :pushpin: Current Features

- utilises OpenAI Chat GPT to generate twitter (X) posts from a list of quantitative python ideas with a specific template file
- tweets are posted to twitter (using <i>tweepy</i>) every 12 hours with the <i>apscheduler</i> module in python
- scripts are run using the operating system service and therefore from the command line of our remote server we can: check the status, stop or start the twitter bot service
- we also have access to the logs generated from the twitter bot

## :mountain: Task List

- [x] <b>Project 1:</b> QuantPy Main Twitter Feed Automation
  - [x] Generate Quantitative Finance Twitter Content using OpenAI ChatGPT
  - [x] Schedule & Send Tweets using Raspberry Pi Headless Server
- [ ] <b>Project 2:</b> Automate scraping & publishing of top quality news on Quantitative Finance Topics
- [ ] <b>Project 3:</b> Train & Publish specific Quantitative Finance ChatGPT Model
- [ ] <b>Project 4:</b> Allow users to interact with trained model by tagging @TheQuantPy twitter handle on quant finance twitter posts :tada: :champagne:

## :hammer_and_wrench: Deployment Steps

These steps are to be followed to create a clone of the twitter bot and run it on a remote server or rapsberry pi (as I have done here).

### :gear: Pre-Steps:

1. Create [OpenAI Account for API](https://platform.openai.com/apps)
2. Create API key for [ChatGPT API](https://platform.openai.com/account/api-keys)
3. Create Twitter Account for your bot
4. Create [Developer Account](https://developer.twitter.com/en/portal/dashboard), this can be done for free, however there is a 250 word explanation of use case required.
5. Add environment variables to a .env file, and have this where you host your app. List of environment variables required and naming convention below:
   - OPENAI_API_KEY
   - TWITTER_API_KEY
   - TWITTER_API_SECRET
   - TWITTER_ACCESS_TOKEN
   - TWITTER_ACCESS_TOKEN_SECRET
   - TWITTER_BEARER_TOKEN

### Step 0 (Raspberry Pi): Setup Raspberry Pi

[Setup Raspberry Pi in Headless mode](https://www.hackster.io/435738/how-to-setup-your-raspberry-pi-headless-8a905f), so you can access it like a remote server.

### Step 1: Python3.11+ and Git

Ensure python 3.11 is installed, and download git.

```
sudo apt update
sudo apt install git
```

### Step 2: download github repo to remote server

```
git clone https://github.com/TheQuantPy/quantpy-twitter-bot.git
```

### Step 3: create & activate virtual env

### 3a. Enter the github project main folder

```
cd quantpy-twitter-bot
```

### 3b. create and activate virtual env

```
python -m venv env
source env/bin/activate
```

### 3c. download requirements

```
pip install -r requirements.txt
```

### Step 4: setup twitter bot service using `systemctl`

> [!NOTE]
> Important that twitter_bot.service file is [installed properly](https://gist.github.com/emxsys/a507f3cad928e66f6410e7ac28e2990f) on host server

We will run out twitter bot script as a service in the operating system so it can hva the following functionality:

- start,
- stop,
- restart, and
- status.

We will setup our bot script as a service using [linux operating system sysemd](https://wiki.archlinux.org/title/systemd), which can be commanded using <i>systemctl</i>.

#### 4a. Setting up the service to run our script in daemon mode on the server:

```
cd /lib/systemd/system/
sudo nano twitter_bot.service
```

#### 4b. Add the Following Text and save the service file:

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

#### 4c. Now that we have our service we need to activate it:

```
sudo chmod 644 /lib/systemd/system/twitter_bot.service
chmod +x /home/quantpy/quantpy-twitter-bot/main.py
sudo systemctl daemon-reload
sudo systemctl enable twitter_bot.service

```

#### 4d. Now we can access the following commands

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

## The MIT License (MIT)

Copyright © 2023 QuantPy Pty Ltd

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
