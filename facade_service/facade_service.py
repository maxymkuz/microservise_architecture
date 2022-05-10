from flask import Flask, jsonify, request
import requests
import uuid
from pyconfig import FACADE_PORT, MESSAGES_PORT
import random
LOGGING_PORTS = [5005, 5006, 5007]

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        port = random.choice(LOGGING_PORTS)
        print("senging request to port:", port)

        try:
            logging_reqs = requests.get(f'http://127.0.0.1:{port}/')
        except:
            print("ERROR: Was not able to reach the", port)
            return "ERROR, Didn't reach the port", port
        msgs_reqs = requests.get(f'http://127.0.0.1:{MESSAGES_PORT}/')


        lst_logging_str = ','.join(logging_reqs.json())
        msgs_reqs_str = msgs_reqs.content.decode('ascii')

        res_str = f'LOGGING: {lst_logging_str}\n MESSAGES_REQ: {msgs_reqs_str}'
        print(res_str)
        return '<p>Logging: ' + logging_reqs.content.decode('ascii') + '</p>' #+ \
            #    '<p>Msgs:' + msgs_reqs.content.decode('ascii') + '</p>'

    elif request.method == 'POST':
        uuid_ = uuid.uuid1()

        port = random.choice(LOGGING_PORTS)
        print("senging request to port:", port)

        try:
            requests.post(f'http://127.0.0.1:{port}/',
                        json={'UUID': str(uuid_),
                                'msg': request.json['msg']})
            return "Message sent"
        except:
            print("ERROR: Was not able to reach the", port)
            return "ERROR, Didn't reach the port", port


if __name__ == '__main__':
    app.run(debug=True, port=FACADE_PORT)
