from flask import Flask, jsonify, request
import requests
import uuid
from pyconfig import LOGGING_PORT, FACADE_PORT, MESSAGES_PORT


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        logging_reqs = requests.get(f'http://127.0.0.1:{LOGGING_PORT}/')
        msgs_reqs = requests.get(f'http://127.0.0.1:{MESSAGES_PORT}/')
        # print(logging_reqs.json())
        # print(type(logging_reqs.json()))
        lst_logging_str = ','.join(logging_reqs.json())
        msgs_reqs_str = msgs_reqs.content.decode('ascii')

        res_str = f'LOGGING: {lst_logging_str}\n MESSAGES_REQ: {msgs_reqs_str}'
        print(res_str)

        return '<p>Logging: ' + logging_reqs.content.decode('ascii') + '</p>' + \
               '<p>Msgs:' + msgs_reqs.content.decode('ascii') + '</p>'
    elif request.method == 'POST':
        uuid_ = uuid.uuid1()

        requests.post(f'http://127.0.0.1:{LOGGING_PORT}/',
                      json={'UUID': str(uuid_),
                            'msg': request.json['msg']})
        return "Message sent"


if __name__ == '__main__':
    app.run(debug=True, port=FACADE_PORT)
