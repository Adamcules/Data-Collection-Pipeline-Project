FROM python:3.10

COPY . .

RUN apt-get update -y 
RUN apt-get -y install libpq-dev gcc
RUN apt-get -y install wget
RUN apt-get -y install gnupg

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

RUN apt-get install -yqq unzip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

RUN pip install -r requirements.txt

CMD ["python", "main.py"]