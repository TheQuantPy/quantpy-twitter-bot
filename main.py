import time
import logging
from twitter_bot import run_quantpy_feed_bot
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

# set up logging to file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%y-%m-%d %H:%M",
    filename="twitter-bot.log",
    filemode="a",
)

if __name__ == "__main__":
    # Creates a default Background Scheduler
    sched = BackgroundScheduler(daemon=True)

    # run once to publish
    run_quantpy_feed_bot()

    # then add to scheduler
    sched.add_job(run_quantpy_feed_bot,'interval', hours=12)

    # start scheduler
    sched.start()

    while True:
        time.sleep(60)
