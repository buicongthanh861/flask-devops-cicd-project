from flask import Flask, render_template, request, Response
import requests
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

metrics = PrometheusMetrics(app)

SEARCH_COUNTER = Counter("weather_searches_total", "Total number of weather searches")
SEARCH_FAILED_COUNTER = Counter("weather_searches_failed_total", "Total number of failed weather searches")
SEARCH_BY_CITY_COUNTER = Counter("weather_searches_by_city_total", "Total number of weather searches by city", ["city"])

API_KEY = "ef9a3d31837bf5a5ea1f5085a43aab92"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    if request.method == "POST":
        SEARCH_COUNTER.inc()
        city = request.form["city"]
        SEARCH_BY_CITY_COUNTER.labels(city=city).inc()
        response = requests.get(f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric")
        if response.status_code == 200:
            weather_data = response.json()
        else:
            SEARCH_FAILED_COUNTER.inc()
            weather_data = {"error": "City not found!"}

    return render_template("index.html", weather_data=weather_data)


@app.route("/health")
def health_check():
    return {"status": "healthy"}, 200

@app.route("/metrics")
def metrics_endpoint():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
