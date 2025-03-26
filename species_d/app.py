from flask import Flask, request, jsonify
from service.Modals import db, SensorData
from datetime import datetime, date, timedelta
import numpy as np
from service.prediction_service import  start_predict

from flask_cors import CORS

APP_NAME = 'orchid_species'

app = Flask(APP_NAME)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/plant_two'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/api/days', methods=['GET'])
def predict():
    # today = datetime.now().date()
    today = datetime.strptime('2024-12-27', '%Y-%m-%d').date()
    day1 = today
    day2 = today - timedelta(days=1)
    day3 = today - timedelta(days=2)
    day4 = today - timedelta(days=3)
    day5 = today - timedelta(days=4)
    day6 = today - timedelta(days=5)
    day7 = today - timedelta(days=6)

    print("Day 1:", day1)
    print("Day 2:", day2)
    print("Day 3:", day3)
    print("Day 4:", day4)
    print("Day 5:", day5)
    print("Day 6:", day6)
    print("Day 7:", day7)

    date_list = [day1,day2,day3,day4,day5,day6,day7]
    date_string = ["Day 01" , "Day 02" , "Day 03" , "Day 04", "Day 05", "Day 06" , "Day 07"]

    Morning = "Morning"
    Evening = "Evening"

    humidity = 0
    temperature = 0
    light = 0

    day_body = []

    for date, date_label in zip(date_list, date_string):
        # Query for morning data
        day_morning = SensorData.query.filter(SensorData.timestamp >= date,
                                              SensorData.timestamp < date + timedelta(days=1),
                                              SensorData.timeofday == Morning).first()

        # Query for evening data
        day_evening = SensorData.query.filter(SensorData.timestamp >= date,
                                              SensorData.timestamp < date + timedelta(days=1),
                                              SensorData.timeofday == Evening).first()



        # Ensure both records exist
        if day_morning and day_evening:
            h = (day_morning.humidity + day_evening.humidity) / 2
            t = (day_morning.temperature + day_evening.temperature) / 2
            l = (day_morning.light + day_evening.light) / 2


            humidity = humidity + h
            temperature = temperature + t
            light = light + l

            day_body.append(
                {
                    "day": date_label,
                    "date": date.strftime('%Y/%m/%d'),
                    "Humidity1": str(day_morning.humidity),
                    "Humidity2": str(day_evening.humidity),
                    "Temp1": str(day_morning.temperature),
                    "Temp2": str(day_evening.temperature),
                    "Light1": str(day_morning.light),
                    "Light2": str(day_evening.light),
                }
            )
        else:
            humidity = humidity + 0
            temperature = temperature + 0
            light = light + 0

            day_body.append(
                {
                    "day": date_label,
                    "date": date.strftime('%Y/%m/%d'),
                    "Humidity1": 0,
                    "Humidity2": 0,
                    "Temp1": 0,
                    "Temp2":0,
                    "Light1": 0,
                    "Light2": 0,
                }
            )

    humidity = humidity / 7
    temperature = temperature / 7
    light = light / 7


    print(humidity , temperature, light)

    new_data = np.array([[humidity, temperature, light]])

    prediction = start_predict(new_data)

    if humidity == 0 or temperature == 0 or light == 0:
        prediction = "ERROR"

    avgResults = {
        "average_humidity": f"{round(humidity, 2)}%",
        "average_Temp": f"{round(temperature, 2)} Celsius",
        "average_Light": f"{round(light, 2)}",
        "recommend": prediction.get("class", "ERROR") if isinstance(prediction, dict) else "ERROR"
    }

    return jsonify({"days": day_body, "avgResults": avgResults})

if __name__ == '__main__':
    if APP_NAME == 'orchid_species':
        app.run(host='0.0.0.0', debug=True, port=5001)

