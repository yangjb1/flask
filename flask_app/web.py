#!/usr/bin/python
from flask import Flask, render_template
import missionbox as mb
import os

app=Flask(__name__)

@app.route('/')
@app.route('/home')
def hello():
    return render_template('home.html')

@app.route('/control_panel', methods=['GET','POST'])
def control_panel():
    stream= mb.check_stream()
    status=mb.status();
    return render_template('control_panel.html',stream=stream, status=status)

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

'''
@app.route('/relay')
def relay(x):
    mb.relay(x)

@app.route('/meter')
def relay():
    mb.meter()

@app.route('/load_video')
def load_video():
    return render_template('load_video.html')
'''

if __name__ == '__main__':
    app.run(debug=True)
