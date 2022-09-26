import serial
import pymysql
from . import db, serials
from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    connection = db.connect_db()
    #port = serials.connect_serial()

    #while True:
    #    db.get_sensors()
    #    sleep(1.0)

    @app.route('/')
    def index():
        sensors = db.get_sensors(connection)
        return render_template('index.html', title='Monitoring', sensors=sensors)

    return app
