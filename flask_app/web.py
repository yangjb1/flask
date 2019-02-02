#!/usr/bin/python
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
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
    #gps=mb.gps()
    return render_template('control_panel.html',stream=stream, status=status)

'''
@app.route('/check_stream',methods=['get'])
def check_stream():
    stream= mb.check_stream()
    return render_template('control_panel.html', stream=stream)
'''

@app.route('/handle_stream', methods=["POST"])
def handle_stream():
    json = request.get_json()

    status = json['status']

    if status == "true":
        stream()
        return jsonify(result="started")
    else:
        stop_stream()
        return jsonify(result="stoped")

@app.route('/stream')
def stream():
    mb.start_stream()
    stream=mb.check_stream()
    return render_template('control_panel.html', stream=stream)

@app.route('/stop_stream')
def stop_stream():
    os.system('pkill ffserver')
    stream=mb.check_stream()
    return render_template('control_panel.html', stream=stream)

@app.route('/load_video')
def load_video():
    return render_template('load_video.html')
#mb.load_video('static/missionboxVideo_2018-12-29-1-51-55.avi')

@app.route('/load_video_post', methods=['GET','POST'])
def load_video_post():
    if request.method == 'POST':
        video_file = request.form['f']
        #mb.load_video(video_file)
        return
    else:
        video_file = request.args.get('f')
        #mb.load_video(video_file)
        return

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

@app.route('/relay1', methods = ['GET'])
def relay1():
    mb.relay(6)

@app.route('/relay2')
def relay2():
    mb.relay(7)

@app.route('/relay3')
def relay3():
    mb.relay(8)

@app.route('/relay4')
def relay4():
    mb.relay(9)

if __name__ == '__main__':
    app.run(debug=True)
