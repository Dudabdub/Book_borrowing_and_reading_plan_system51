from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models import Course, Task
from app import db
from app.utils.progress_calculator import calculate_course_progress
from datetime import datetime

bp = Blueprint('main', __name__)
 
@bp.route('/')
def index():
    courses = Course.query.limit(10).all()
    # compute simple stats
    total_courses = len(courses)
    pending_tasks = Task.query.filter_by(status='pending').count()
    completed_tasks = Task.query.filter_by(status='completed').count()
    # upcoming tasks (simple)
    upcoming_tasks = Task.query.filter(Task.due_date!=None).order_by(Task.due_date.asc()).limit(5).all()
    return render_template('index.html',
                           courses=courses,
                           total_courses=total_courses,
                           pending_tasks=pending_tasks,
                           completed_tasks=completed_tasks,
                           upcoming_tasks=upcoming_tasks)

@bp.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

@bp.route('/course/add', methods=['GET','POST'])
def add_course():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            return "name required", 400
        c = Course(name=name)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('main.courses'))
    return render_template('add_course.html')

# Simple API endpoints
@bp.route('/api/courses')
def api_courses():
    cs = Course.query.all()
    data = []
    for c in cs:
        data.append({'id': c.id, 'name': c.name, 'color': c.color})
    return jsonify(data)

@bp.route('/api/tasks', methods=['GET','POST'])
def api_tasks():
    if request.method == 'GET':
        tasks = Task.query.all()
        data = [{'id':t.id,'title':t.title,'status':t.status,'course_id':t.course_id} for t in tasks]
        return jsonify(data)
    data = request.get_json() or {}
    title = data.get('title')
    if not title:
        return jsonify({'error':'title required'}), 400
    t = Task(title=title, task_type=data.get('task_type'), course_id=data.get('course_id'))
    db.session.add(t)
    db.session.commit()
    return jsonify({'id': t.id}), 201
