from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
from config import get_config

app = Flask(__name__)
app.config.from_object(get_config())
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    priority = db.Column(db.String(20), default='Medium')
    category = db.Column(db.String(50), default='General')
    due_date = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    position = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'{self.sno} - {self.title}'

class Subtask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.sno'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'Subtask {self.id}: {self.text[:20]}...'

with app.app_context():
    db.create_all()

migrate = Migrate(app, db)


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    # Provide the current datetime to templates for due date comparisons
    now = datetime.utcnow
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        priority = request.form.get('priority', 'Medium')
        category = request.form.get('category', 'General')
        due_date_str = request.form.get('due_date', '')
        
        if title == '':
            return redirect("/")
            
        todo = Todo(
            title=title,
            desc=desc if desc else "description not available",
            priority=priority,
            category=category
        )
        
        # Handle due date if provided
        if due_date_str:
            try:
                todo.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except:
                pass
        
        # Set position for new task (at the end)
        max_position = db.session.query(db.func.max(Todo.position)).scalar() or 0
        todo.position = max_position + 1
        
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
      # Get sort parameter and filter parameters from URL
    sort_by = request.args.get('sort', 'position')
    filter_status = request.args.get('status', 'all')  # all, completed, active
    filter_priority = request.args.get('priority', 'all')  # all, high, medium, low
    filter_due = request.args.get('due', 'all')  # all, overdue, today, upcoming, none
    
    # Start with a base query
    query = Todo.query
    
    # Apply status filter
    if filter_status == 'completed':
        query = query.filter_by(completed=True)
    elif filter_status == 'active':
        query = query.filter_by(completed=False)
    
    # Apply priority filter
    if filter_priority != 'all':
        query = query.filter(Todo.priority.ilike(filter_priority))
    
    # Apply due date filter
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    if filter_due == 'overdue':
        query = query.filter(Todo.due_date < today, Todo.due_date != None)
    elif filter_due == 'today':
        tomorrow = today.replace(day=today.day + 1)
        query = query.filter(Todo.due_date >= today, Todo.due_date < tomorrow)
    elif filter_due == 'upcoming':
        query = query.filter(Todo.due_date >= today)
    elif filter_due == 'none':
        query = query.filter(Todo.due_date == None)
    
    # Apply sorting
    if sort_by == 'priority':
        # Custom priority order: High, Medium, Low
        query = query.order_by(
            db.case(
                (Todo.priority == 'High', 1),
                (Todo.priority == 'Medium', 2),
                else_=3
            ),
            Todo.position
        )
    elif sort_by == 'due_date':
        query = query.order_by(db.case((Todo.due_date == None, 1), else_=0), Todo.due_date, Todo.position)
    elif sort_by == 'category':
        query = query.order_by(Todo.category, Todo.position)
    else:
        # Default sort by position
        query = query.order_by(Todo.position)
    
    # Execute the query
    allTodo = query.all()
    
    # Calculate statistics for dashboard
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    stats = {
        'total': Todo.query.count(),
        'completed': Todo.query.filter_by(completed=True).count(),
        'today': Todo.query.filter(
            Todo.due_date >= today, 
            Todo.due_date < today.replace(day=today.day + 1),
            Todo.completed == False
        ).count(),
        'overdue': Todo.query.filter(
            Todo.due_date < today, 
            Todo.due_date != None, 
            Todo.completed == False
        ).count()
    }
    
    return render_template('index.html', allTodo=allTodo, stats=stats)
  
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
            db.session.commit()
            return redirect("/")
            
        todo.desc = request.form['desc']
        if todo.desc == '':
            todo.desc = "description not available"
        
        # Update new fields
        todo.priority = request.form.get('priority', 'Medium')
        todo.category = request.form.get('category', 'General')
        
        # Handle completed status
        todo.completed = 'completed' in request.form
        
        # Handle due date
        due_date_str = request.form.get('due_date', '')
        if due_date_str:
            try:
                todo.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except:
                todo.due_date = None
        else:
            todo.due_date = None
            
        db.session.commit()
        return redirect("/")
    
    return render_template('update.html', todo=todo)


@app.route("/search", methods=['GET'])
def search():
    search_str = request.args.get('search_str', '')
    
    if search_str:
        # Perform a case-insensitive search with partial match on title or description
        allTodo = Todo.query.filter(
            db.or_(
                Todo.title.ilike(f'%{search_str}%'),
                Todo.desc.ilike(f'%{search_str}%')
            )
        ).all()
        
        # Calculate statistics for dashboard
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        stats = {
            'total': Todo.query.count(),
            'completed': Todo.query.filter_by(completed=True).count(),
            'today': Todo.query.filter(
                Todo.due_date >= today, 
                Todo.due_date < today.replace(day=today.day + 1),
                Todo.completed == False
            ).count(),
            'overdue': Todo.query.filter(
                Todo.due_date < today, 
                Todo.due_date != None, 
                Todo.completed == False
            ).count()
        }
        
        return render_template('search.html', allTodo=allTodo, search_query=search_str, stats=stats)
    else:
        return redirect("/")

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/toggle_complete/<int:sno>")
def toggle_complete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if todo:
        todo.completed = not todo.completed
        db.session.commit()
    return redirect("/")

@app.route("/move/<int:sno>/<direction>")
def move_task(sno, direction):
    todo = Todo.query.filter_by(sno=sno).first()
    if not todo:
        return redirect("/")
        
    if direction == "up" and todo.position > 1:
        # Find the task above this one
        above_task = Todo.query.filter(Todo.position < todo.position).order_by(Todo.position.desc()).first()
        if above_task:
            # Swap positions
            temp_pos = above_task.position
            above_task.position = todo.position
            todo.position = temp_pos
            db.session.commit()
    
    elif direction == "down":
        # Find the task below this one
        below_task = Todo.query.filter(Todo.position > todo.position).order_by(Todo.position).first()
        if below_task:
            # Swap positions
            temp_pos = below_task.position
            below_task.position = todo.position
            todo.position = temp_pos
            db.session.commit()
    
    return redirect("/")
    
@app.route("/categories")
def list_categories():
    categories = db.session.query(Todo.category).distinct().all()
    return render_template('categories.html', categories=[cat[0] for cat in categories])

@app.route("/filter/<category>")
def filter_by_category(category):
    allTodo = Todo.query.filter_by(category=category).order_by(Todo.position).all()
    
    # Calculate statistics for dashboard
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    stats = {
        'total': Todo.query.count(),
        'completed': Todo.query.filter_by(completed=True).count(),
        'today': Todo.query.filter(
            Todo.due_date >= today, 
            Todo.due_date < today.replace(day=today.day + 1),
            Todo.completed == False
        ).count(),
        'overdue': Todo.query.filter(
            Todo.due_date < today, 
            Todo.due_date != None, 
            Todo.completed == False
        ).count()
    }
    
    return render_template('index.html', allTodo=allTodo, filtered_category=category, stats=stats)

@app.route("/filter_priority/<priority>")
def filter_by_priority(priority):
    allTodo = Todo.query.filter_by(priority=priority).order_by(Todo.position).all()
    
    # Calculate statistics for dashboard
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    stats = {
        'total': Todo.query.count(),
        'completed': Todo.query.filter_by(completed=True).count(),
        'today': Todo.query.filter(
            Todo.due_date >= today, 
            Todo.due_date < today.replace(day=today.day + 1),
            Todo.completed == False
        ).count(),
        'overdue': Todo.query.filter(
            Todo.due_date < today, 
            Todo.due_date != None, 
            Todo.completed == False
        ).count()
    }
    
    return render_template('index.html', allTodo=allTodo, stats=stats)

@app.route("/bulk_action", methods=['POST'])
def bulk_action():
    action = request.form.get('bulk_action')
    selected_tasks = request.form.getlist('selected_tasks')
    
    if not selected_tasks:
        return redirect("/")
        
    if action == "delete":
        for task_id in selected_tasks:
            todo = Todo.query.get(int(task_id))
            if todo:
                db.session.delete(todo)
    
    elif action == "mark_complete":
        for task_id in selected_tasks:
            todo = Todo.query.get(int(task_id))
            if todo:
                todo.completed = True
    
    elif action == "mark_incomplete":
        for task_id in selected_tasks:
            todo = Todo.query.get(int(task_id))
            if todo:
                todo.completed = False
    
    elif action == "set_priority":
        priority = request.form.get('priority', 'Medium')
        for task_id in selected_tasks:
            todo = Todo.query.get(int(task_id))
            if todo:
                todo.priority = priority
    
    elif action == "set_category":
        category = request.form.get('category', 'General')
        for task_id in selected_tasks:
            todo = Todo.query.get(int(task_id))
            if todo:
                todo.category = category
    
    db.session.commit()
    return redirect("/")

@app.route("/statistics")
def statistics():
    # Total task count
    total_tasks = Todo.query.count()
    completed_tasks = Todo.query.filter_by(completed=True).count()
    active_tasks = total_tasks - completed_tasks
    
    # Priority distribution
    high_priority = Todo.query.filter_by(priority='High').count()
    medium_priority = Todo.query.filter_by(priority='Medium').count()
    low_priority = Todo.query.filter_by(priority='Low').count()
      # Due date statistics
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    overdue_tasks = Todo.query.filter(Todo.due_date < today, Todo.due_date != None, Todo.completed == False).count()
    
    # Safer way to calculate "due today" without potential day overflow
    tomorrow = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    import datetime as dt
    tomorrow = today + dt.timedelta(days=1)
    
    due_today = Todo.query.filter(
        Todo.due_date >= today, 
        Todo.due_date < tomorrow,
        Todo.completed == False
    ).count()
    
    # Category distribution
    categories = db.session.query(Todo.category, db.func.count(Todo.sno)).group_by(Todo.category).all()
    
    return render_template('statistics.html', 
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        active_tasks=active_tasks,
        high_priority=high_priority,
        medium_priority=medium_priority,
        low_priority=low_priority,
        overdue_tasks=overdue_tasks,
        due_today=due_today,
        categories=categories
    )

@app.route("/add_subtask/<int:todo_id>", methods=['POST'])
def add_subtask(todo_id):
    todo = Todo.query.filter_by(sno=todo_id).first()
    if not todo:
        return redirect("/")
        
    text = request.form.get('subtask_text', '')
    if text:
        subtask = Subtask(todo_id=todo_id, text=text)
        db.session.add(subtask)
        db.session.commit()
    
    return redirect(f"/update/{todo_id}")

@app.route("/toggle_subtask/<int:subtask_id>")
def toggle_subtask(subtask_id):
    subtask = Subtask.query.get(subtask_id)
    if subtask:
        subtask.completed = not subtask.completed
        db.session.commit()
        return redirect(f"/update/{subtask.todo_id}")
    return redirect("/")

@app.route("/delete_subtask/<int:subtask_id>")
def delete_subtask(subtask_id):
    subtask = Subtask.query.get(subtask_id)
    if subtask:
        todo_id = subtask.todo_id
        db.session.delete(subtask)
        db.session.commit()
        return redirect(f"/update/{todo_id}")
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
