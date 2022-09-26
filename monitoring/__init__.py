import serial
import pymysql
from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    connection = connect_db()
    port = connect_serial()

    #while True:
    #    db.get_sensors()
    #    sleep(1.0)

    @app.route('/')
    def index():
        sensors = get_sensors()
        return render_template('index.html', title='Monitoring', sensors=sensors)

    return app


def connect_db():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        db='conception',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection


def connect_serial():
    port = serial.Serial('/dev/ttyACM0', '9600')

    return port


def insert_sensors(port, connection):
    data = port.readline()

    with connection.cursor() as cursor:
        cursor.execute("""INSERT INTO sensors VALUES (%s)""", (data))
    
    connection.commit()


def get_sensors(connection):
    with connection.cursor() as cursor:
        row = cursor.execute(
            'SELECT * FROM sensors ORDER BY id DESC LIMIT 1'
        ).fetchone()

    return row


def close_serial(port):
    if port is not None:
        port.close()


def close_db(connection):
    if connection is not None:
        connection.close()