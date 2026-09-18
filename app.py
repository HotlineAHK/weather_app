import datetime
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather", methods=["POST"])
def weather():
    city = request.form.get("city")
    g_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    g_res = requests.get(g_url).json()
    
    if not g_res.get("results"):
        return "Город не найден", 404
        
    loc = g_res["results"][0]
    lat, lon = loc["latitude"], loc["longitude"]
    name, country = loc["name"], loc.get("country", "")
    
    w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    w_res = requests.get(w_url).json()
    cur = w_res["current"]
    
    data = {
        "name": name,
        "country": country,
        "temp": cur["temperature_2m"],
        "wind": cur["wind_speed_10m"],
        "humidity": cur["relative_humidity_2m"],
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return render_template("result.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
