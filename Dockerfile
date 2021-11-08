FROM python:latest

RUN apt-get update && apt upgrade -y
RUN cd /
COPY . /ehelper/
RUN cd ehelper
WORKDIR /ehelper
RUN pip install -r requirements.txt
CMD [ "python", "bot.py"]