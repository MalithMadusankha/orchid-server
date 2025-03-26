from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class SensorData(db.Model):
    __tablename__ = 'sensor_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timeofday = db.Column(db.String(12))
    humidity = db.Column(db.Float)
    temperature = db.Column(db.Float)
    light = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert SQLAlchemy object to dictionary."""
        return {
            "id": self.id,
            "timeofday": self.timeofday,
            "humidity": self.humidity,
            "temperature": self.temperature,
            "light": self.light,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
