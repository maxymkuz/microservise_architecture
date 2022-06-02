import hazelcast
from flask import Flask, jsonify, request
import requests
import uuid
from pyconfig import FACADE_PORT, MESSAGES_PORT
import random

app = Flask(__name__)

# consul:
import consul

host_name = "localhost"
host_port = 9000
service_name = "facade-service"

cs = consul.Consul(host=host_name, port=8500)
cs.agent.service.register(service_name,
                            port=host_port,
                            service_id=f"{service_name}:{host_port}"
                        )


def update_consul():
    logging_service = []
    message_service = []
    for key, val in cs.agent.services().items():
        if key.startswith("logging_service"):
            logging_service.append(f"http://localhost:{val['Port']}")
        elif key.startswith("messages_service"):
            message_service.append(
                f"http://localhost:{val['Port']}")
    return message_service, logging_service

MESSAGES_PORTS, LOGGING_PORTS = update_consul()

print(LOGGING_PORTS)
print(MESSAGES_PORTS)


client = hazelcast.HazelcastClient()

queue = client.get_queue(cs.kv.get("hazelcast_queue")[1]["Value"].decode("utf-8")).blocking()


@app.route('/', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        logging_port = random.choice(LOGGING_PORTS)
        print("senging request to LOGGING port:", logging_port)

        try:
            logging_reqs = "logging default"
            logging_reqs = requests.get(logging_port)
        except:
            print("ERROR: Was not able to reach the", logging_port)
            return "ERROR, Didn't reach the port", logging_port

        messages_port = random.choice(MESSAGES_PORTS)
        print("senging request to MESSAGES port:", messages_port)

        try:
            msgs_reqs = requests.get(messages_port)
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
            requests.post(port,
                        json={'UUID': str(uuid_),
                            'msg': request.json['msg']})
            return "Message SENT"
        except:
            print("ERROR: Was not able to reach the", port)
            return "ERROR, Didn't reach the port", port


if __name__ == '__main__':
    app.run(debug=True, port=FACADE_PORT)
