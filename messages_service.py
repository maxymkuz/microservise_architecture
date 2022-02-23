from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def add():
    if request.method == 'GET':
        return "sample_message", 200


if __name__ == '__main__':
    app.run(debug=True)
