FROM alpine:3.10

ADD ["docker/annotation/requirements.txt", "/requirements.txt"]
RUN apk upgrade --update && \
	apk add --update python3 build-base python3-dev py3-psycopg2 && \
	pip3 install -r /requirements.txt && rm /requirements.txt
WORKDIR /annotation
EXPOSE 80

ENTRYPOINT ["python3", "manage.py"]
ADD ["django_unchained", "/annotation"]

CMD ["runserver", "0.0.0.0:80"]