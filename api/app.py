import os
from flask import Flask
import requests
from dotenv import load_dotenv
from waitress import serve
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
load_dotenv()
API_KEY = os.getenv("OWM_API_KEY")


@app.route("/")
def index():
    return "App Works!"


@app.route("/<country>/<city>")
def weather_by_city(country: str, city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}"
    params = dict(
        appid=API_KEY,
    )

    response = requests.get(url=url, params=params)
    data = response.json()
    return data


# serve(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8080)
    serve(app, host="0.0.0.0", port=8080)
