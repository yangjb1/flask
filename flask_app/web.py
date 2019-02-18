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

@app.route('/')
@app.route('/home')
def hello():
    f.write('home page\n')
    return render_template('home.html', fileNames=fileFilter())

@app.route('/control_panel', methods=['GET','POST'])
def control_panel():
    #status=mb.status()
    #gps=mb.gps()
    f.write('control_panel page\n')
    return render_template('control_panel.html', table=table)

@app.route("/loadVideo" , methods=['GET', 'POST'])
def loadVideo():
    select = request.form.get('videos')
    mb.load_video(str(select))
    f.write('loadVideo ' + str(select) + '\n')
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
# itemList=mb.status()[0:4]
items = [Item('PC Voltage', 'Description1'),
         Item('Current', 'Description2')]
         # Item('Name3', 'Description3'),
         # Item('Name3', 'Description3')]


# Populate the table
table = ItemTable(items)

def tableValue():
    itemList = mb.status()
    itemList = itemList.spilt(',')
    items = [Item('PC Voltage', itemList[0]),
             Item('Current', itemList[1])]
    table = ItemTable(items)
    return table

@app.route('/handle_stream', methods=["POST"])
def handle_stream():
    json = request.get_json()

    status = json['status']

    if status == "true":
        stream()
        f.write('stream on')
        f.flush()
        return jsonify(result="started")
    else:
        stop_stream()
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
    return render_template('load_video.html')

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
        f.write('capture on')
        f.flush()
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        f.write('capture off')
        f.flush()
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
    f.write(status)
    f.flush()
    return render_template('/control_panel.html', status=status)

@app.route('/relay2')
def relay2():
    mb.relay('7')
    status = mb.status()
    f.write(status)
    f.flush()
    return render_template('/control_panel.html', status=status)

@app.route('/relay3')
def relay3():
    mb.relay('8')
    status = mb.status()
    f.write(status)
    f.flush()
    return render_template('/control_panel.html', status=status)

@app.route('/relay4')
def relay4():
    mb.relay('9')
    status = mb.status()
    f.write(status)
    f.flush()
    return render_template('/control_panel.html', status=status)


f=open('logFile', 'a+')
f.write('----------------------------------------\n')
f.write(str(datetime.now()) + '\n')
f.flush()


def logFile():
    timeNow = (str(datetime.now()))
    cpu = str(psutil.cpu_percent(interval=1))
    f.write(timeNow + ',' + cpu)
    f.flush()


if __name__ == '__main__':
    app.run(debug=True)
