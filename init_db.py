from app import create_app, db
from app.models import User, Book, Borrow, Plan
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all() 

    # create demo user
    u = User(username='demo', email='demo@example.com', password_hash=generate_password_hash('password'))
    db.session.add(u)
    db.session.commit()

    # sample books
    books = [
        Book(title='活着', author='余华', total_copies=3, available_copies=3, isbn='9787229100605'),
        Book(title='小王子', author='圣埃克苏佩里', total_copies=2, available_copies=2, isbn='9787530219857'),
        Book(title='Python编程：从入门到实践', author='Eric Matthes', total_copies=2, available_copies=2, isbn='9787115428028'),
        Book(title='数据结构与算法分析', author='Mark Allen Weiss', total_copies=1, available_copies=1, isbn='9787111234567'),
    ]
    for b in books:
        db.session.add(b)
    db.session.commit()

    # sample borrow
    borrow = Borrow(user_id=u.id, book_id=books[0].id, borrow_date=datetime.utcnow()-timedelta(days=3), due_date=datetime.utcnow()+timedelta(days=11), returned=False)
    books[0].available_copies -= 1
    db.session.add(borrow)
    db.session.commit()

    # sample plan
    plan = Plan(user_id=u.id, title='阅读挑战：每月一本', target_books=4, completed_books=0)
    db.session.add(plan)
    db.session.commit()

    print('Initialized database with demo user (demo@example.com / password) and sample data.')
