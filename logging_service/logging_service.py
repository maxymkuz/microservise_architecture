import hazelcast
import sys

from flask import Flask, jsonify, request
app = Flask(__name__)

# consul:
import consul


LOGGING_PORT = int(sys.argv[1])



host_name = "localhost"
service_name = "logging_service"

cs = consul.Consul(host=host_name, port=8500)
cs.agent.service.register(service_name,
                            port=LOGGING_PORT,
                            service_id=f"{service_name}:{LOGGING_PORT}"
                        )


# Connect to Hazelcast cluster.
client = hazelcast.HazelcastClient()

# Get or create the "distributed-map" on the cluster.
distributed_map = client.get_map(cs.kv.get("hazelcast_map")[1]["Value"].decode("utf-8")).blocking()


def fetch_messages():
    # get all available keys here
    print(distributed_map.values())
    return jsonify(list(distributed_map.values()))


@app.route('/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def add():
    if request.method == 'GET':
        return fetch_messages(), 200

    elif request.method == 'POST':
        # TODO handle exception here maybe?
        data = request.get_json()
        uuid = data["UUID"]
        msg = data["msg"]
        
        # local_hash_table[uuid] = msg
        distributed_map.lock(uuid)

        distributed_map.put(uuid, msg)

        distributed_map.unlock(uuid)


        print(msg)
        return jsonify(msg), 200


if __name__ == '__main__':
    port = int(sys.argv[1])

    print("\n\nCURRENT PORT: ", port)

    app.run(debug=False, port=port)
