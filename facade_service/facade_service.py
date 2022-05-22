import hazelcast
from flask import Flask, jsonify, request
import requests
import uuid
from pyconfig import FACADE_PORT, MESSAGES_PORT
import random
LOGGING_PORTS = [5005, 5006, 5007]
MESSAGES_PORTS = [5010, 5011]
app = Flask(__name__)

client = hazelcast.HazelcastClient()
queue = client.get_queue("my-queue").blocking()


@app.route('/', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        logging_port = random.choice(LOGGING_PORTS)
        print("senging request to LOGGING port:", logging_port)

        try:
            logging_reqs = "logging default"
            logging_reqs = requests.get(f'http://127.0.0.1:{logging_port}/')
        except:
            print("ERROR: Was not able to reach the", logging_port)
            return "ERROR, Didn't reach the port", logging_port

        messages_port = random.choice(MESSAGES_PORTS)
        print("senging request to MESSAGES port:", messages_port)

        try:
            msgs_reqs = requests.get(f'http://127.0.0.1:{messages_port}/')
        except:
            print("ERROR: Was not able to reach the", messages_port)
            return "ERROR, Didn't reach the port", messages_port        



        lst_logging_str = ','.join(logging_reqs.json())
        msgs_reqs_str = msgs_reqs.content.decode('ascii')

        res_str = f'LOGGING: {lst_logging_str}\n MESSAGES_REQ: {msgs_reqs_str}'
        print(res_str)
        return res_str
        return '<p>Logging: ' + logging_reqs.content.decode('ascii') + '</p>' #+ \
            #    '<p>Msgs:' + msgs_reqs.content.decode('ascii') + '</p>'

    elif request.method == 'POST':
        uuid_ = uuid.uuid1()

        port = random.choice(LOGGING_PORTS)
        print("senging request to port:", port)

        queue.put(request.json['msg'])
        print("putted")

        try:
            requests.post(f'http://127.0.0.1:{port}/',
                        json={'UUID': str(uuid_),
                            'msg': request.json['msg']})
            return "Message SENT"
        except:
            print("ERROR: Was not able to reach the", port)
            return "ERROR, Didn't reach the port", port


if __name__ == '__main__':
    app.run(debug=True, port=FACADE_PORT)
