FROM python:3-onbuild
COPY . /usr/src/app

# needed to  have this fix : https://github.com/tweepy/tweepy/pull/1042
RUN pip install git+https://github.com/tweepy/tweepy

CMD ["python", "app.py"]