from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/')
def index():
    return jsonify(message="rctm")


if __name__ == '__main__':
    app.run(port=3000, debug=True)
