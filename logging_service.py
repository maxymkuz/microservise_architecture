from flask import Flask, jsonify, request

app = Flask(__name__)

local_hash_table = {}


def fetch_messages():
    return jsonify([local_hash_table[uuid] for uuid in local_hash_table])


@app.route('/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def add():
    if request.method == 'GET':
        return fetch_messages(), 200

    elif request.method == 'POST':
        # TODO handle exception here maybe?
        data = request.get_json()
        uuid = int(data["UUID"])
        msg = data["msg"]
        local_hash_table[uuid] = msg
        print(msg)
        return jsonify(msg), 200


if __name__ == '__main__':
    app.run(debug=True)
