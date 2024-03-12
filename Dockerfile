FROM python:3.13.0a4-slim-bullseye

EXPOSE 1234

WORKDIR /service
COPY requirements.txt /service
RUN pip install -r requirements.txt
COPY /tracker /service/tracker

CMD ["python", "/service/tracker/manage.py", "runserver", "0.0.0.0:1234"]
