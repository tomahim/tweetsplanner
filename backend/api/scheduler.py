
####################
###### Tweet Scheduler
####################
import datetime


def send_planned_tweets():
    print(datetime.utcnow())

    # TODO:
    # - retrieve matching tweets for current date
    # - Send the found tweets using specific user oauth tokens

# schedule.every(10).minutes.do(job)
# schedule.every(1).seconds.do(send_planned_tweets)

# while True:
#     schedule.run_pending()
#     time.sleep(1)