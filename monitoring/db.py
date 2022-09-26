import click
import serial
import pymysql
from flask import current_app, g


def connect_serial():
    g.port = serial.Serial('/dev/ttyACM0', '9600')


def connect_db():
    if 'connection' not in g:
        g.connection = pymysql.connect(
            host='localhost',
            user='root',
            db='conception',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )


def close_serial(e=None):
    port = g.pop('port', None)

    if port is not None:
        port.close()


def close_db(e=None):
    connection = g.pop('connection', None)

    if connection is not None:
        connection.close()


def insert_sensors():
    data = g.port.readline()

    with g.connection.cursor() as cursor:
        cursor.execute("""INSERT INTO sensors VALUES (%s)""", (data))
    
    g.connection.commit()


def get_sensors():
    with g.connection.cursor() as cursor:
        g.row = cursor.execute(
            'SELECT * FROM sensors ORDER BY id DESC LIMIT 1'
        ).fetchone()

    return g.row
