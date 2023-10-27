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
EXPOSE 8080
CMD [ "python", "app.py" ]