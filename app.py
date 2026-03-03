import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import db, Task
from datetime import datetime, timezone, date

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('filter', 'all')
    search_query = request.args.get('search', '')
    
    stmt = db.select(Task)
    
    if search_query:
        stmt = stmt.filter(Task.title.contains(search_query) | Task.description.contains(search_query))
        
    if status_filter == 'completed':
        stmt = stmt.filter_by(completed=True)
    elif status_filter == 'pending':
        stmt = stmt.filter_by(completed=False)
        
    stmt = stmt.order_by(Task.created_at.desc())
    tasks_pagination = db.paginate(stmt, page=page, per_page=10)
    
    return render_template('index.html', 
                           tasks=tasks_pagination.items, 
                           pagination=tasks_pagination, 
                           current_filter=status_filter,
                           search_query=search_query,
                           today=date.today())

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    due_date_str = request.form.get('due_date')
    
    if not title:
        flash('Title is required!', 'error')
        return redirect(url_for('index'))
    
    due_date = None
    if due_date_str:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        
    new_task = Task(title=title, description=description, due_date=due_date)
    db.session.add(new_task)
    db.session.commit()
    
    flash('Task added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/toggle/<int:id>', methods=['POST'])
def toggle_task(id):
    task = db.session.get(Task, id)
    if not task:
        flash('Task not found!', 'error')
        return redirect(url_for('index'))
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = db.session.get(Task, id)
    if not task:
        flash('Task not found!', 'error')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        
        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format!', 'error')
                return render_template('edit.html', task=task)
        else:
            task.due_date = None
            
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('index'))
        
    return render_template('edit.html', task=task)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task = db.session.get(Task, id)
    if not task:
        flash('Task not found!', 'error')
        return redirect(url_for('index'))
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
