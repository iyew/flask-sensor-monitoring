import time
import random
import serial
import pymysql
import threading
from flask import Flask, render_template, jsonify


app = Flask(__name__)


@app.route("/")
def index():
    connection = connect_db()
    port = connect_serial()
    th = threading.Thread(target=insert_sensors, args=(port, connection), daemon=True)
    th.start()

    return render_template('index.html')
    
    
@app.route("/update", methods=['POST'])
def update():
    connection = connect_db()
    row = get_sensors(connection)
    return jsonify(row)


def connect_db():
    connection = pymysql.connect(
        host='localhost',
        user='admin',
        password='admin',
        db='conception',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection


def close_db(connection):
    if connection is not None:
        connection.close()


def insert_sensors(port, connection):
    while True:
        # data format: "float float int int int int"
        # You must write 'Serial.print(sensor_1); Serial.print(" "); ... Serial.println(sensor_n);' in Arduino
        # ex) "11.0 22.0 33 44 55 66"
        data = port.readline()
        sensors = data.decode('utf-8').split()

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO sensors (temperature, humidity, pm1_0, pm2_5, pm10, voc) VALUES (%s, %s, %s, %s, %s, %s)", sensors)

        connection.commit()
        time.sleep(1)


def get_sensors(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM sensors ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()

    return row


def connect_serial():
    port = serial.Serial('/dev/ttyACM0', '115200')

    return port


def close_serial(port):
    if port is not None:
        port.close()


if __name__ == '__main__':
    app.run()

