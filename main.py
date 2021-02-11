from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.route('/')
def index():
    return jsonify(message="rctm")


if __name__ == '__main__':
    app.run(port=3000, debug=True)
