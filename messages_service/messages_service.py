import hazelcast
from flask import Flask, jsonify, request
from pyconfig import MESSAGES_PORT
import sys

app = Flask(__name__)
client = hazelcast.HazelcastClient()
queue = client.get_queue("my-queue").blocking()
data = []

@app.route('/', methods=['GET'])
def add():
    while not queue.is_empty():
        data.append(queue.take())
        print(f"Consumed {data[-1]}")
    return str(data)


if __name__ == '__main__':
    port = int(sys.argv[1])

    app.run(debug=True, port=port)
