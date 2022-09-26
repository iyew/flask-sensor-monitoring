import serial


def connect_serial():
    port = serial.Serial('/dev/ttyACM0', '9600')

    return port


def close_serial(port):
    if port is not None:
        port.close()
