from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/falsk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


# MODELS


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100), nullable=False)

    def __init__(self, title, description):
        self.title = title
        self.description = description


db.create_all()


class TodoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Todo

    id = ma.auto_field()
    title = fields.String(required=True)
    description = fields.String(required=True)


todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)


@app.route('/todos', methods=['POST'])
def create_todo():
    try:
        data = request.get_json()
        todo = Todo(data['title'], data['description'])
        db.session.add(todo)
        db.session.commit()
        return todo_schema.dump(todo)
    except KeyError:
        return jsonify(message='envia la data completa')


@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    result = todos_schema.dump(todos)
    return jsonify(result)


@app.route('/todos/<id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)

    if todo is None:
        return jsonify(message='tarea no encontrada')

    db.session.delete(todo)
    db.session.commit()

    return jsonify(message=f'se eliminó la tarea con id {id}')


@app.route('/todos/<id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    todo = Todo.query.get(id)

    if todo is None:
        return jsonify(message='tarea no encontrada')

    todo.title = data['title']
    todo.description = data['description']

    db.session.commit()

    return todo_schema.dump(todo)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
