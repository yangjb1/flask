#!/usr/bin/python
from flask import Flask, render_template, Response, request, jsonify
import missionbox as mb
import os
from video import VideoCamera

app=Flask(__name__)
video_camera = None
global_frame = None

@app.route('/')
@app.route('/home')
def hello():
    return render_template('home.html')

@app.route('/control_panel', methods=['GET','POST'])
def control_panel():
    stream= mb.check_stream()
    status=mb.status()
    gps=mb.gps()
    return render_template('control_panel.html',stream=stream,status=status,gps=gps)

'''
@app.route('/check_stream',methods=['get'])
def check_stream():
    stream= mb.check_stream()
    return render_template('control_panel.html', stream=stream)
'''

@app.route('/handle_stream',methods=['get'])
def handle_stream():
    if mb.check_stream():
        stop_stream()
    else:
        stream()

@app.route('/stream',methods=['GET'])
def stream():
    mb.start_stream()
    stream=mb.check_stream()
    return render_template('control_panel.html', stream=stream)

@app.route('/stop_stream',methods=['GET'])
def stop_stream():
    os.system('pkill ffserver')
    stream=mb.check_stream()
    return render_template('control_panel.html', stream=stream)

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
        return jsonify(result="started")
    else:
        video_camera.stop_record()
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

if __name__ == '__main__':
    app.run(debug=True)
