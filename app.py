from flask import Flask, jsonify, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
# Modify this string with the appropriate database connection settings you have set up in your machine.
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://aro1914:passsword@localhost:5432/tododb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class TodoList(db.Model):
    # Table name
    __tablename__ = 'todolist'
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='todolist',
                            lazy=True, cascade='all, delete', passive_deletes=True)

    # Object Representation
    def __repr__(self):
        return f"\n<TodoList id:{self.id} name:{self.name}>"


class Todo(db.Model):
    # Table name
    __tablename__ = 'todo'
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    todolist_id = db.Column(db.Integer, db.ForeignKey(
        "todolist.id", ondelete="CASCADE"), nullable=False)

    # Object Representation
    def __repr__(self):
        return f"\n<Todo id:{self.id}, description:{self.description} completed:{self.completed}>"

# Commented due to our use of migrations
# db.create_all()


@app.route('/todo/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todolist_id = request.get_json()['todolist_id']
        todo = Todo(description=description, todolist_id=todolist_id)
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route('/todo/create-list', methods=['POST'])
def create_list():
    error = False
    body = {}
    try:
        name = request.get_json()['name']
        list = TodoList(name=name)
        db.session.add(list)
        db.session.commit()
        body['id'] = list.id
        body['name'] = list.name
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route('/todo/<todo_id>/update', methods=['POST'])
def update_todo(todo_id):
    error = False
    body = {}
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
        body['completed'] = todo.completed
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route('/todo/update-all', methods=['POST'])
def update_all():
    error = False
    body = {}
    try:
        todos = Todo.query.all()
        for todo in todos:
            todo.completed = True
        db.session.commit()
        body['successful'] = not error
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route('/todo/<todo_id>/delete', methods=["DELETE"])
def delete_todo(todo_id):
    error = False
    body = {}
    try:
        # Alternative way
        # todo = Todo.query.get(todo_id)
        # db.session.delete(todo)
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
        body['successful'] = not error
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route('/todo/todo-list/<list_id>/delete', methods=["DELETE"])
def delete_list(list_id):
    error = False
    body = {}
    try:
        # Alternative way
        # todo = Todo.query.get(todo_id)
        # db.session.delete(todo)
        TodoList.query.filter_by(id=list_id).delete()
        db.session.commit()
        body['successful'] = not error
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route('/todo-list/<list_id>')
def get_todo_list(list_id):
    dummyTodoList = [
        {
            'id': 1,
            'description': 'Create a Todo'
        }, {
            'id': 2,
            'description': 'Accomplish the task'
        }, {
            'id': 3,
            'description': 'Remove the Todo',
        },
    ]

    dummyList = [
        {
            'id': 'welcome',
            'name': 'Starter Task',
        }
    ]

    name = dummyList[0]['name']
    newList_id = dummyList[0]['id']

    if not list_id == 'welcome':
        return render_template('index.html', data=Todo.query.filter_by(todolist_id=list_id).order_by('id').all(), list_id=list_id, list=TodoList.query.order_by('id').all(), name=TodoList.query.get(list_id).name)
    else:
        return render_template('index.html', data=dummyTodoList, list_id=newList_id, list=dummyList, name=name)


@app.route('/')
def index():
    return redirect(url_for('get_todo_list', list_id=TodoList.query.first().id if len(TodoList.query.all()) > 0 else 'welcome'))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
