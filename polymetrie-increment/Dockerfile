FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

RUN virtualenv venv

RUN . venv/bin/activate

EXPOSE 5000

CMD [ "flask", "--app", "service", "run", "--host=0.0.0.0"]