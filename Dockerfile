FROM alpine:3.4
MAINTAINER Antonio Juliano "antonio.m.juliano@gmail.com"
RUN apk add --no-cache bash uwsgi uwsgi-python py-pip \
  && pip install --upgrade pip \
  && pip install flask \
  && pip install trueskill
COPY . /app
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["app.py"]
