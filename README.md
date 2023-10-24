# quantpy-twitter-bot

[QuantPy Twitter Feed](https://twitter.com/TheQuantPy)

This project utilises OpenAI Chat GPT to generate twitter (X) posts from a list of quantitative python ideas with a specific template file.

Tweets will be posted every 12 hours using apscheduler module in python, callable from the the linux operating system services.

We can check the status, stop or start the service from the command line, and we also have access to the logs generated from the twitter bot.

## :mountain: Task List

- [x] Project 1: QuantPy Main Twitter Feed Automation
  - [x] Generate Quantitative Finance Twitter Content using OpenAI ChatGPT
  - [x] Schedule & Send Tweets using Raspberry Pi Headless Server
- [ ] Project 2: Automate scraping & publishing of top quality news on Quantitative Finance Topics
- [ ] Project 3: Train & Publish specific Quantitative Finance ChatGPT Model
- [ ] Project 4: Allow users to interact with trained model by tagging @TheQuantPy twitter handle on quant finance twitter posts :tada: :champagne:

## :hammer_and_wrench: To Run on Remote Server / Raspberry Pi

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

### Step 3: setup twitter bot service using `systemctl`

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
