import os
from flask import Flask, render_template, request, redirect
import requests
from dotenv import load_dotenv
from prometheus_flask_exporter import PrometheusMetrics
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
metrics = PrometheusMetrics(app)
load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRES_DATABASE_URI")
API_KEY = os.getenv("OWM_API_KEY")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# with app.app_context():
#     db.create_all()


class Weather(db.Model):
    __tablename__ = "weather"
    id = db.Column(db.Integer(), primary_key=True)
    city = db.Column(db.String(40))

    def __init__(self, city) -> None:
        self.city = city


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/add-favorite/<city>", methods=["POST"])
def add_favorite(city: str):
    weather = Weather(city)
    db.session.add(weather)
    db.session.commit()
    favoritesFromDb = db.session.query(Weather)
    return render_template("index.html", favorites=favoritesFromDb)


@app.route("/delete-favorite/<id>", methods=["POST"])
def delete_favorite(id: str):
    deleteSession = Weather.query.filter(Weather.id == id).one()
    db.session.delete(deleteSession)
    db.session.commit()
    return redirect("/")


@app.route("/", methods=["GET", "POST"])
def index():
    favoritesFromDb = db.session.query(Weather)
    if request.method == "POST":
        city_name = request.form["name"]
        print(city_name)

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&APPID={API_KEY}"
        response = requests.get(url).json()
        try:
            temp = response["main"]["temp"]
            weather = response["weather"][0]["description"]
            min_temp = response["main"]["temp_min"]
            max_temp = response["main"]["temp_max"]
            icon = response["weather"][0]["icon"]
            return render_template(
                "index.html",
                temp=temp,
                weather=weather,
                min_temp=min_temp,
                max_temp=max_temp,
                icon=icon,
                city_name=city_name,
                favorites=favoritesFromDb,
            )
        except:
            return render_template("index.html", favorites=favoritesFromDb)
    else:
        return render_template("index.html", favorites=favoritesFromDb)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(host="0.0.0.0", port=8080, debug=True)

    # with app.app_context():
