from flask import Flask, request, Response, send_from_directory
import jsonpickle
import numpy as np
import cv2


from match import Match

# Initialize the Flask application
app = Flask(__name__, static_url_path='')


match = Match()

# route http posts to this method


@app.route('/api/image/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, 0)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # do some fancy processing here....

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/match/<path:path>')
def send_js(path):
    return send_from_directory('ref_image', path)


@app.route('/api/image/recog', methods=['POST'])
def test2():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, 0)

    match_result = match.match_image(img)

    response_pickled = jsonpickle.encode(match_result)

    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000)
