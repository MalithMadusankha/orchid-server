from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Flower(db.Model):
    __tablename__ = 'flower'

    fid = db.Column(db.Integer, primary_key=True)

    def to_dict(self):
        return {"fid": self.fid}


class Mode(db.Model):
    __tablename__ = 'mode'

    modeid = db.Column(db.Integer, primary_key=True)

    def to_dict(self):
        return {"modeid": self.modeid}


class SensorData(db.Model):
    __tablename__ = 'sensor_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flowerid = db.Column(db.Integer)
    humidity = db.Column(db.Float)
    temperature = db.Column(db.Float)
    light = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "flowerid": self.flowerid,
            "humidity": self.humidity,
            "temperature": self.temperature,
            "light": self.light,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S") if self.timestamp else None
        }


class SensorDataTest(db.Model):
    __tablename__ = 'sensor_data_test'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flowerid = db.Column(db.Integer)
    humidity = db.Column(db.Float)
    temperature = db.Column(db.Float)
    light = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "flowerid": self.flowerid,
            "humidity": self.humidity,
            "temperature": self.temperature,
            "light": self.light,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S") if self.timestamp else None
        }
