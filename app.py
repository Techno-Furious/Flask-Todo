from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os


POSTGRES_URL_SQL=os.environ.get('POSTGRES_URL_SQL')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URL_SQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'{self.sno} - {self.title}'

with app.app_context():
    db.create_all()

migrate = Migrate(app, db)


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if title == '':
                return redirect("/")
        if desc== '' :
            todo = Todo(title=title, desc="description not available")
            db.session.add(todo)
            db.session.commit()
            return redirect("/")
        
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)
  
@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/update.html")
def Update_Page():
    return render_template('update.html')

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    
    if request.method == 'POST':
        todo.title = request.form['title']
        if todo.title == '': 
            db.session.delete(todo)
        todo.desc = request.form['desc']
        if todo.desc == '':
            todo.desc = "description not available"
        db.session.commit()
        return redirect("/")
    
    return render_template('update.html', todo=todo)


@app.route("/search", methods=['GET'])
def search():
    search_str = request.args.get('search_str', '')
    
    if search_str:
        # Perform a case-insensitive search with partial match
        allTodo = Todo.query.filter(Todo.title.ilike(f'%{search_str}%')).all()
        return render_template('search.html', allTodo=allTodo)
    else:
        return redirect("/")

@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
