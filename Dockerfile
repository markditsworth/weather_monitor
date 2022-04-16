FROM python:3.9-slim-buster

# setup user and fs
RUN groupadd -r python-user \
    && useradd -r -g python-user python-user \
    && mkdir -p /home/python-user \
    && chown -R python-user:python-user /home/python-user

ENV APP_HOME /home/python-user
WORKDIR $APP_HOME

# setup python environment
ENV PYTHONUNBUFFERED True
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip \
    && pip3 install -r /tmp/requirements.txt \ 
    && rm -f /tmp/requirements.txt

USER python-user

ENTRYPOINT ["python3", "main.py", "--config", "config.json"]