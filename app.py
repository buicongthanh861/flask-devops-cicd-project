import time
from flask import Flask, render_template, request, Response
import requests
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# --- KHAI BÁO METRICS ---
SEARCH_COUNTER = Counter("weather_searches_total", "Total number of weather searches")
SEARCH_FAILED_COUNTER = Counter(
    "weather_searches_failed_total", "Total number of failed weather searches"
)
SEARCH_BY_CITY_COUNTER = Counter(
    "weather_searches_by_city_total",
    "Total number of weather searches by city",
    ["city"],
)
# Gauge để đo số request đang xử lý đồng thời
IN_PROGRESS_REQUESTS = Gauge(
    "weather_app_in_progress", "Number of in-progress weather requests"
)
# Summary để đo thời gian xử lý request
REQUEST_DURATION = Histogram(
    "weather_request_duration_seconds", "Duration of weather request processing in seconds",
    buckets=[0.5, 1, 2, 3, 5, 10]
)
API_KEY = "ef9a3d31837bf5a5ea1f5085a43aab92"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    if request.method == "POST":
        # Bắt đầu xử lý: Tăng Gauge và Counter tổng
        IN_PROGRESS_REQUESTS.inc()
        SEARCH_COUNTER.inc()
        start_time = time.time()  # Lưu thời điểm bắt đầu xử lý

        try:
            city = request.form.get("city")
            if city:
                # Tăng Counter theo label city
                SEARCH_BY_CITY_COUNTER.labels(city=city).inc()

                # Giả lập thời gian trễ để bạn kịp soi Gauge trên Prometheus
                time.sleep(2)

                response = requests.get(
                    f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
                )

                if response.status_code == 200:
                    weather_data = response.json()
                else:
                    SEARCH_FAILED_COUNTER.inc()
                    weather_data = {"error": "City not found!"}
        finally:
            duration = time.time() - start_time  # Lấy thời gian đã trôi qua
            REQUEST_DURATION.observe(duration)
            # Kết thúc xử lý: Luôn luôn giảm Gauge (dù thành công hay lỗi)
            IN_PROGRESS_REQUESTS.dec()

    return render_template("index.html", weather_data=weather_data)


@app.route("/health")
def health_check():
    return {"status": "healthy"}, 200


@app.route("/metrics")
def metrics_endpoint():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
