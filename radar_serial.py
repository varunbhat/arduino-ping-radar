from random import random
import threading
# import serial
import traceback
from bottle import Bottle, run, template, static_file

app = Bottle()
# ser = serial.Serial('COM4', 115200, timeout=0)
maxdist = 300
angle_interval = 5

serialData = [maxdist for i in range(360 / angle_interval)]


def getSerialData():
    gRun = True
    test_index = 0
    global serialData
    while gRun:
        # line = ser.readline()
        line = str(int(random() * 200)) + ',' + str(test_index)
        test_index = (test_index + 1) % 360
        try:
            if len(line) > 0:
                data = dict(zip(['distance', 'angle'], line.split(',')))
                index = (int(data['angle']) / angle_interval)
                serialData[index] = int(data['distance'])
                for i in range(len(serialData)):
                    if (i > (index + int(25 * len(serialData) / 100))) or (i < (index - int(25 * len(serialData) / 100))):
                        serialData[i] = 0
        except KeyboardInterrupt:
            gRun = False
            return
        except:
            print traceback.print_stack()
            pass


SerialThread = threading.Thread(target=getSerialData, name='SerialThread')
SerialThread.start()


@app.route('/static/<path:path>')
def staticpaths(path):
    return static_file(path, 'static')


@app.route('/json_data')
def jsondata():
    global serialData
    return str(serialData)


@app.route('/')
def index_path():
    return template('index', interval=angle_interval)


run(app, host='localhost', port=8000)