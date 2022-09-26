import pymysql


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
    data = port.readline()

    with connection.cursor() as cursor:
        cursor.execute("""INSERT INTO sensors VALUES (%s)""", (data))
    
    connection.commit()


def get_sensors(connection):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM sensors ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()

    return row
