from werkzeug.datastructures import FileStorage
import os
import time
import torch
from flask import Flask, render_template, \
    send_from_directory, request, redirect, url_for, Response
from static.main import predict
from static.detection_part.test_PE_analytics import get_result_frame
import cv2 as cv
app = Flask(__name__)


@app.route('/')
def home():
    return '<a href="home">GO TO HOME PAGE</a>'


UPLOAD_FOLDER = r"static/output"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # # # model define
# pull model on github
# model = torch.hub.load('ultralytics/yolov5', 'custom', path=r"static/detection_part/weight/best_4classes.pt",
#                        force_reload=True)
# local repo model
model = torch.hub.load('static/custom_train_model/yolov5', 'custom',
                       path="static/detection_part/weight/best_4classes.pt", source='local', force_reload=True)
model.conf = 0.9


@app.route('/home', methods=["GET", "POST"])
def index():
    response = False
    file = request.files.get("fileUpload")
    if request.method == "POST" and request is not None:
        filepath = 'static/input/' + \
                   str(time.ctime(time.time())).replace(':', '-') + '.mp4'
        file.save(filepath)
        # predict process
        response = predict(filepath, model, total_pallet=0)
    if response:
        print("res : ", response)
        return render_template('result.html', name=response)
        # return send_from_directory(app.config["UPLOAD_FOLDER"], response)
        # return redirect(url_for('.uploads_to_client',name=response))
    return render_template('home.html')


def gen():
    while True:
        frame = get_result_frame()
        # print(f'frame : {frame}')
        if isinstance(frame, str):
            # if type(frame)== str or frame == 'nopic':
            frame = cv.imread(r'static/style/loading.jpg')
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        frame = cv.resize(frame, (0, 0), fx=0.5, fy=0.5)
        frame = cv.imencode('.jpg', frame)[1].tobytes()
        # cv.imshow('Yolo', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.001)
        # if cv.waitKey(25) == 27:
        #     break


# stream !!
@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/uploads/<name>')
def uploads_to_client(name):
    # print(f'name : {name}')
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


if __name__ == ('__main__'):
    print(f'is_UseCuda ? : {torch.cuda.is_available()}')
    app.run()
    # app.run(debug=True)
