FROM python:latest

RUN apt-get update && apt upgrade -y && \
    adduser --disabled-password --gecos "" --shell /bin/bash ehelper && \
    mkdir /data && \
    chown ehelper:ehelper /data

USER ehelper
WORKDIR /ehelper
ENV PATH="/home/ehelper/.local/bin:${PATH}"
COPY --chown=ehelper . ./

RUN pip install --user -r requirements.txt
CMD [ "python", "/ehelper/bot.py"]