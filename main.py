from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<USERNAME>:<PASSWORD>@localhost:5432/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    __tablename__ = 'todo'
    pk_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    desc = db.Column(db.String(100))
    complete_status = db.Column(db.Boolean)


@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        baslik = request.form["baslik"]
        aciklama = request.form["aciklama"]
        status = bool(request.form.get('status'))
        todo = Todo(title=baslik, desc=aciklama, complete_status=status)
        db.session.add(todo)
        db.session.commit()
    return redirect("/")


@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect("/")

@app.route('/status/<int:todo_id>/<int:current_status>', methods=['POST'])
def status(todo_id, current_status):
    todo = Todo.query.get(todo_id)
    if todo:
        todo.complete_status = not current_status
        db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)