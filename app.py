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
    #port = connect_serial()
    th = threading.Thread(target=test_insert, args=(connection,), daemon=True)
    #th = threading.Thread(target=insert_sensors, args=(port, connection), daemon=True)
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
        user='root',
        password='root',
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
        data = port.readline()

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO sensors (temperature, humidity, pm1_0, pm2_5, pm10, voc) VALUES (%s, %s, %s, %s, %s, %s)", (data))

        connection.commit()
        time.sleep(1)


def get_sensors(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM sensors ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()

    return row


def test_insert(connection):
    while True:
        with connection.cursor() as cursor:
            random_float = round(random.uniform(1, 100), 2)
            random_int = random.randint(1, 100)
            data = (random_float, random_float, random_int, random_int, random_int, random_int)
            print(data)
            cursor.execute("INSERT INTO sensors (temperature, humidity, pm1_0, pm2_5, pm10, voc) VALUES (%s, %s, %s, %s, %s, %s)", (random_float, random_float, random_int, random_int, random_int, random_int))

        connection.commit()
        time.sleep(1)


def connect_serial():
    port = serial.Serial('/dev/ttyACM0', '9600')

    return port


def close_serial(port):
    if port is not None:
        port.close()


if __name__ == '__main__':
    app.run()

