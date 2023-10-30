FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip uninstall urllib3 -y --cert root.pem
RUN pip install urllib3
COPY ./api /app

RUN addgroup --system --gid 1001 python-group
RUN adduser --system --uid 1001 python-user
RUN chown -R python-user /app
USER app-user

EXPOSE 8080
CMD [ "python", "app.py" ]