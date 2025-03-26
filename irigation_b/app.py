from flask import Flask, request, jsonify
from Modals import db, Mode, Flower, SensorData

from flask_cors import CORS

APP_NAME = 'orchid_irrigation'

app = Flask(APP_NAME)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/plant_one'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

MODE_TEST = 8
MODE_LIVE = 9

DENDROBIUM = "Dendrobium"
VANDA = "Vanda"
PHALAENOPSIS = "Phalaenopsis"


@app.route('/emergency-water', methods=['POST'])
def predict():
    data = request.get_json()
    flower = data.get('flower')
    amount = data.get('amount')

    if not flower or not amount:
        return jsonify({"error": "Invalid data"}), 400

    db.session.query(Mode).delete()

    # Create a new Mode entry
    new_mode = Mode(modeid=MODE_TEST)

    # Add to session and commit
    db.session.add(new_mode)
    db.session.commit()

    print(f"Flower: {flower}, Amount: {amount}ml")
    return jsonify({"message": "Data received", "flower": flower, "amount": amount}), 200


@app.route('/schedule', methods=['POST'])
def schedule_watering():
    data = request.json
    selected_flower = data.get('flower')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    db.session.query(Mode).delete()

    # Create a new Mode entry
    new_mode = Mode(modeid=MODE_LIVE)

    # Add to session and commit
    db.session.add(new_mode)
    db.session.commit()

    # update flower type
    db.session.query(Flower).delete()

    f_id = 0

    if selected_flower == DENDROBIUM:
        f_id = 1
    elif selected_flower == VANDA:
        f_id = 2
    elif selected_flower == PHALAENOPSIS:
        f_id = 3
    else:
        pass

    # Create a new Mode entry
    new_flower = Flower(fid=f_id)

    # Add to session and commit
    db.session.add(new_flower)
    db.session.commit()

    # Process the data as needed
    print(data)
    return jsonify({"message": "Schedule received", "data": data}), 200

@app.route('/api/wateringHistory', methods=['GET'])
def get_wateringHistory():

    flower_map = {1: "DENDROBIUM", 2: "VANDA", 3: "PHALAENOPSIS"}

    # Query all data
    sensor_data = SensorData.query.all()

    result = []
    for data in sensor_data:
        data_dict = data.to_dict()

        # Map flower ID to flower name
        data_dict["flowerName"] = flower_map.get(data_dict["flowerid"], data_dict["flowerid"])
        del data_dict["flowerid"]

        # Convert all values to strings with formatting
        string_dict = {}
        for key, value in data_dict.items():
            if isinstance(value, float):
                # Format floats to 2 decimal places
                string_dict[key] = f"{value:.2f}"
            elif isinstance(value, int):
                # Simple conversion for integers
                string_dict[key] = str(value)
            else:
                # Default string conversion for other types
                string_dict[key] = str(value)

        result.append(string_dict)


    return jsonify({"wateringHistory": result,})


if __name__ == '__main__':
    if APP_NAME == 'orchid_irrigation':
        app.run(host='0.0.0.0', debug=True, port=5006)

