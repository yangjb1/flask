#!/usr/bin/python
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
import missionbox as mb
import modem as m
import os
from video import VideoCamera
import fnmatch
from datetime import datetime
import psutil

app=Flask(__name__)
video_camera = None
global_frame = None

@app.route('/handle_streaming')
def handle_streaming():
    current_status = request.args.get('streamStatus')
    if current_status == 'False':
        logFile()
        f.write('stream on\n')
        f.flush()
        stream()
        return 'True'
    else:
        stop_stream()
        logFile()
        f.write('stream off\n')
        f.flush()
        return 'False'
    # return 'True' if current_status == 'False' else 'False'

@app.route('/relay1') # modem
def relay1():
    relay1Status = request.args.get('relay1Status')
    mb.relay('6')
    if relay1Status == 'False':
        logFile()
        f.write('modem on\n')
        f.flush()
        return 'True'
    else:
        logFile()
        f.write('modem off\n')
        f.flush()
        return 'False'

@app.route('/relay2') #analog streamer
def relay2():
    relay2Status = request.args.get('relay2Status')
    mb.relay('7')
    if relay2Status == 'False':
        logFile()
        f.write('analog streamer on\n')
        f.flush()
        return 'True'
    else:
        logFile()
        f.write('analog streamer off\n')
        f.flush()
        return 'False'

@app.route('/table')
def table():
    table = mb.status()
    logFile()
    f.write('meters-' + table + '\n')
    f.flush()
    return table

@app.route('/modem')
def modem():
    table = m.modem()
    logFile()
    f.write('modem status-' + table + '\n')
    f.flush()
    return table


@app.route('/')
@app.route('/home')
def hello():
    video_camera = VideoCamera()
    logFile()
    f.write('home page\n')
    f.flush()
    return render_template('home.html', streaming=mb.check_stream())

@app.route('/control_panel', methods=['GET','POST'])
def control_panel():
    status=mb.status()
    logFile()
    f.write('control_panel page\n')
    f.flush()
    return render_template('control_panel.html', status=status)

@app.route("/loadVideo" , methods=['GET', 'POST'])
def loadVideo():
    select = request.form.get('videos')
    mb.load_video(str(select))
    logFile()
    f.write('loadVideo ' + str(select) + '\n')
    f.flush()
    return render_template('home.html', fileNames=fileFilter())
    # return(str(select)) # just to see what select is

@app.route('/handle_stream', methods=["POST"])
def handle_stream():
    json = request.get_json()

    status = json['status']

    if status == "true":
        stream()
        logFile()
        f.write('stream on\n')
        f.flush()
        return jsonify(result="started")
    else:
        stop_stream()
        logFile()
        f.write('stream off\n')
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
        logFile()
        f.write('capture on\n')
        f.flush()
        video_camera.start_record()
        video_on = True
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        logFile()
        f.write('capture off\n')
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

f=open('log', 'a+')
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
