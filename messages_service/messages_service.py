import hazelcast
from flask import Flask, jsonify, request
import sys

app = Flask(__name__)


# consul:
import consul


MESSAGES_PORT = int(sys.argv[1])


host_name = "localhost"
service_name = "messages_service"

cs = consul.Consul(host=host_name, port=8500)
cs.agent.service.register(service_name,
                            port=MESSAGES_PORT,
                            service_id=f"{service_name}:{MESSAGES_PORT}"
                        )



client = hazelcast.HazelcastClient()
queue = client.get_queue(cs.kv.get("hazelcast_queue")[1]["Value"].decode("utf-8")).blocking()

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
