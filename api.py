from flask import Flask, request, Response, send_from_directory
import jsonpickle
import numpy as np
import cv2
import io
import os
from flask_cors import CORS
from werkzeug import secure_filename

from match import Match
from frame import Frame
from exception import InvalidUsage

# Initialize the Flask application
app = Flask(__name__, static_url_path='')

CORS(app)

match = Match()
frame = Frame()

# route http posts to this method


@app.route('/api/image/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, 0)
    # cv2.imshow('image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/api/image/recog', methods=['POST'])
def test2():
    r = request
    photo = r.files['photo']
    in_memory_file = io.BytesIO()
    photo.save(in_memory_file)

    nparr = np.fromstring(in_memory_file.getvalue(), np.uint8)
    # decode image
    img = cv2.imdecode(nparr, 0)

    match_result = match.match_image(img)

    response_pickled = jsonpickle.encode(match_result)

    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/match/<path:path>')
def send_js(path):
    return send_from_directory('ref_image', path)


@app.route('/sprite/<path:path>')
def send_js_1(path):
    return send_from_directory('web', path)


@app.route('/hello')
def hello():
    a = 1/0
    return Response('hello')


@app.route('/api/video', methods=['POST'])
def process_video():
    video = request.files['video']
    filename = secure_filename(video.filename)
    final_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video.save(final_path)
    match_result = frame.read_video(final_path)
    os.remove(final_path)
    response_pickled = jsonpickle.encode(match_result)

    return Response(response=response_pickled, status=200, mimetype="application/json")

    # start flask app


@app.errorhandler(Exception)
def handle_error(error):
    return Response(status=500, mimetype="application/json")


app.config['UPLOAD_FOLDER'] = 'uploads'

# app.run(host="0.0.0.0", port=5000, ssl_context=('cert.pem', 'key.pem'))

app.run(host="0.0.0.0", port=5000)
