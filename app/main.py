from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Book, Borrow, Plan, User
from datetime import datetime, timedelta
from sqlalchemy import or_

bp = Blueprint('main', __name__, template_folder='templates')

@bp.route('/')
@login_required
def index():
    # statistics
    total_books = Book.query.count()
    borrowed = Borrow.query.filter_by(returned=False).count()
    plans = Plan.query.filter_by(user_id=current_user.id).all()
    # top books by total borrows (simple)
    top = db.session.query(Book, db.func.count(Borrow.id).label('cnt')).join(Borrow).group_by(Book.id).order_by(db.desc('cnt')).limit(5).all()
    top_books = [{'title': t[0].title, 'count': t[1]} for t in top]
    return render_template('index.html', total_books=total_books, borrowed=borrowed, plans=plans, top_books=top_books)

@bp.route('/books')
@login_required
def books():
    q = request.args.get('q','')
    page = int(request.args.get('page',1))
    per = current_app.config.get('ITEMS_PER_PAGE',8)
    if q:
        items = Book.query.filter(or_(Book.title.contains(q), Book.author.contains(q))).paginate(page=page, per_page=per)
    else:
        items = Book.query.paginate(page=page, per_page=per)
    return render_template('books.html', items=items, q=q)

@bp.route('/book/add', methods=['GET','POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        total = int(request.form.get('total',1))
        b = Book(title=title, author=author, total_copies=total, available_copies=total)
        db.session.add(b)
        db.session.commit()
        flash('图书已添加', 'success')
        return redirect(url_for('main.books'))
    return render_template('book_form.html')

@bp.route('/book/<int:book_id>/edit', methods=['GET','POST'])
@login_required
def edit_book(book_id):
    b = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        b.title = request.form.get('title')
        b.author = request.form.get('author')
        b.total_copies = int(request.form.get('total', b.total_copies))
        b.available_copies = int(request.form.get('available', b.available_copies))
        db.session.commit()
        flash('更新成功', 'success')
        return redirect(url_for('main.books'))
    return render_template('book_form.html', book=b)

@bp.route('/book/<int:book_id>/delete', methods=['POST'])
@login_required
def delete_book(book_id):
    b = Book.query.get_or_404(book_id)
    db.session.delete(b)
    db.session.commit()
    flash('已删除', 'success')
    return redirect(url_for('main.books'))

@bp.route('/book/<int:book_id>')
@login_required
def book_detail(book_id):
    b = Book.query.get_or_404(book_id)
    borrows = Borrow.query.filter_by(book_id=book_id).order_by(Borrow.borrow_date.desc()).all()
    return render_template('book_detail.html', book=b, borrows=borrows)

@bp.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    b = Book.query.get_or_404(book_id)
    if b.available_copies <= 0:
        flash('无可借副本', 'warning')
        return redirect(url_for('main.book_detail', book_id=book_id))
    due_days = int(request.form.get('days',14))
    due = datetime.utcnow() + timedelta(days=due_days)
    borrow = Borrow(user_id=current_user.id, book_id=book_id, due_date=due)
    b.available_copies -= 1
    db.session.add(borrow)
    db.session.commit()
    flash('借阅成功', 'success')
    return redirect(url_for('main.book_detail', book_id=book_id))

@bp.route('/return/<int:borrow_id>', methods=['POST'])
@login_required
def return_book(borrow_id):
    br = Borrow.query.get_or_404(borrow_id)
    if br.returned:
        flash('已归还', 'info')
        return redirect(url_for('main.index'))
    br.returned = True
    br.returned_at = datetime.utcnow()
    br.book.available_copies += 1
    db.session.commit()
    flash('归还成功', 'success')
    return redirect(url_for('main.index'))

@bp.route('/plans')
@login_required
def plans():
    plans = Plan.query.filter_by(user_id=current_user.id).all()
    return render_template('plans.html', plans=plans)

@bp.route('/plan/add', methods=['GET','POST'])
@login_required
def add_plan():
    if request.method == 'POST':
        title = request.form.get('title')
        target = int(request.form.get('target',1))
        end = request.form.get('end_date') or None
        p = Plan(user_id=current_user.id, title=title, target_books=target, end_date=end)
        db.session.add(p)
        db.session.commit()
        flash('读书计划已创建', 'success')
        return redirect(url_for('main.plans'))
    return render_template('plan_form.html')

@bp.route('/api/stats')
@login_required
def api_stats():
    total_books = Book.query.count()
    borrowed = Borrow.query.filter_by(returned=False).count()
    # plans progress
    plans = Plan.query.filter_by(user_id=current_user.id).all()
    data = {
        'total_books': total_books,
        'borrowed': borrowed,
        'plans': [{'title':p.title, 'target':p.target_books, 'completed':p.completed_books} for p in plans]
    }
    return jsonify(data)
