#!/usr/bin/python
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
import missionbox as mb
import os
from video import VideoCamera
import fnmatch
from flask_table import Table, Col
from datetime import datetime
import psutil


app=Flask(__name__)
video_camera = None
global_frame = None
video_on = False

@app.route('/handle_streaming')
def handle_streaming():
    current_status = request.args.get('streamStatus')
    if current_status == 'False':
        stream()
        return 'True'
    else:
        stop_stream()
        return 'False'
    return 'True' if current_status == 'False' else 'False'

@app.route('/')
@app.route('/home')
def hello():
    video_camera = VideoCamera()
    print video_camera.get_is_record()
    logFile()
    f.write('home page\n')
    f.flush()
    tables='1,1,1,1,1,1,1,1'
    return render_template('home.html', fileNames=fileFilter(), table=tableValue(tables))

@app.route('/control_panel', methods=['GET','POST'])
def control_panel():
    status=mb.status()
    #gps=mb.gps()
    logFile()
    f.write('control_panel page\n')
    f.flush()
    return render_template('control_panel.html', status=status, table=tableValue(status))

@app.route("/loadVideo" , methods=['GET', 'POST'])
def loadVideo():
    select = request.form.get('videos')
    mb.load_video(str(select))
    logFile()
    f.write('loadVideo ' + str(select) + '\n')
    f.flush()
    return render_template('home.html', fileNames=fileFilter())
    # return(str(select)) # just to see what select is

'''
@app.route('/check_stream',methods=['get'])
def check_stream():
    stream= mb.check_stream()
    return render_template('control_panel.html', stream=stream)
'''

def fileFilter():
    return fnmatch.filter(os.listdir('static'), '*.mp4')

class ItemTable(Table):
    name = Col('Attribute')
    description = Col('Value')

# Get some objects
class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

def tableValue(itemList):
    # itemList = mb.status()
    itemList = itemList.split(',')
    items = [Item('PC Voltage', itemList[0]),
             Item('Current', itemList[1]),
             Item('PC Voltage', itemList[0]),
             Item('Current', itemList[1])]
    table = ItemTable(items)
    return table

@app.route('/handle_stream', methods=["POST"])
def handle_stream():
    json = request.get_json()

    status = json['status']

    if status == "true":
        stream()
        logFile()
        f.write('stream on')
        f.flush()
        return jsonify(result="started")
    else:
        stop_stream()
        logFile()
        f.write('stream off')
        f.flush()
        return jsonify(result="stoped")

@app.route('/stream')
def stream():
    mb.start_stream()
    return render_template('control_panel.html')

@app.route('/stop_stream')
def stop_stream():
    os.system('pkill ffserver')
    return render_template('control_panel.html')

@app.route('/load_video')
def load_video():
    return render_template('load_video.html', streaming=mb.check_stream())

@app.route('/shutdown')
def shutdown():
    mb.shutdown()

@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera
    if video_camera == None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']

    if status == "true":
        video_camera.start_record()
        print video_camera.get_is_record()
        logFile()
        f.write('capture on')
        f.flush()
        video_on = True
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        print video_camera.get_is_record()
        logFile()
        f.write('capture off')
        f.flush()
        video_on = False
        return jsonify(result="stopped")

def video_stream():
    global video_camera
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()

    while True:
        frame = video_camera.get_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/relay1')
def relay1():
    mb.relay('6')
    status = mb.status()
    logFile()
    f.write(status)
    f.flush()
    return render_template('/home=.html', status=status, table=tableValue(status))

@app.route('/relay2')
def relay2():
    mb.relay('7')
    status = mb.status()
    logFile()
    f.write(status)
    f.flush()
    return render_template('/home.html', status=status, table=tableValue(status))

@app.route('/relay3')
def relay3():
    mb.relay('8')
    status = mb.status()
    logFile()
    f.write(status)
    f.flush()
    return render_template('/home.html', status=status, table=tableValue(status))

@app.route('/relay4')
def relay4():
    mb.relay('9')
    status = mb.status()
    logFile()
    f.write(status)
    f.flush()
    return render_template('/home.html', status=status, table=tableValue(satus))


f=open('logFile', 'a+')
f.write('----------------------------------------\n')
f.write(str(datetime.now()) + '\n')
f.flush()


def logFile():
    timeNow = (str(datetime.now()))
    cpu = str(psutil.cpu_percent(interval=1))
    f.write(timeNow + ',' + cpu + ',')
    f.flush()


if __name__ == '__main__':
    app.run(debug=True)
