FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app

RUN \
 apk add --no-cache bash && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip uninstall urllib3 -y --cert root.pem
RUN pip install urllib3
COPY ./api /app
RUN chmod +x start-weather-app.sh

RUN addgroup --system --gid 1001 python-group
RUN adduser --system --uid 1001 python-user
RUN chown -R python-user /app
USER python-user

EXPOSE 8080
ENTRYPOINT [ "/app/start-weather-app.sh" ]
# CMD [ "python", "app.py" ]