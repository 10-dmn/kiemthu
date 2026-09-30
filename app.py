# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User, Student
from werkzeug.security import check_password_hash
import re

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'
    db.init_app(app)

    @app.route('/')
    def index():
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username','').strip()
            password = request.form.get('password','').strip()
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                session['username'] = user.username
                flash('Đăng nhập thành công!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Tên đăng nhập hoặc mật khẩu không chính xác.', 'danger')
        return render_template('login.html')

    def login_required(f):
        from functools import wraps
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated

    @app.route('/logout')
    def logout():
        session.clear()
        flash('Đã đăng xuất khỏi hệ thống.', 'info')
        return redirect(url_for('login'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        q = request.args.get('q', '').strip()
        branch = request.args.get('branch', '').strip()
        year = request.args.get('year', '').strip()
        
        students_query = Student.query
        if q:
            students_query = students_query.filter((Student.name.ilike(f'%{q}%')) | (Student.usn.ilike(f'%{q}%')))
        if branch:
            students_query = students_query.filter_by(branch=branch)
        if year:
            try:
                y = int(year)
                students_query = students_query.filter_by(year=y)
            except:
                pass
                
        students = students_query.order_by(Student.id.asc()).all()
        all_students = Student.query.all()
        branches = sorted(list({s.branch for s in all_students if s.branch}))
        years = sorted(list({s.year for s in all_students if s.year}))
        total_count = len(all_students)
        match_count = len(students)
        
        return render_template(
            'dashboard.html',
            students=students,
            branches=branches,
            years=years,
            q=q,
            sel_branch=branch,
            sel_year=year,
            total_count=total_count,
            match_count=match_count
        )

    @app.route('/student/add', methods=['GET', 'POST'])
    @login_required
    def add_student():
        if request.method == 'POST':
            name = request.form.get('name','').strip()
            usn = request.form.get('usn','').strip()
            branch = request.form.get('branch','').strip()
            year = request.form.get('year','').strip()
            email = request.form.get('email','').strip()
            phone = request.form.get('phone','').strip()

            # validations:
            if not name or not usn or not branch or not year:
                flash('Vui lòng điền đầy đủ Họ tên, Mã sinh viên, Chuyên ngành và Năm học.', 'danger')
                return redirect(url_for('add_student'))
                
            if email and not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
                flash('Định dạng email không hợp lệ.', 'danger')
                return redirect(url_for('add_student'))

            existing = Student.query.filter_by(usn=usn).first()
            if existing:
                flash('Mã sinh viên này đã tồn tại trong hệ thống.', 'danger')
                return redirect(url_for('add_student'))

            try:
                year_val = int(year)
            except ValueError:
                flash('Năm học phải là số nguyên hợp lệ.', 'danger')
                return redirect(url_for('add_student'))

            s = Student(name=name, usn=usn, branch=branch, year=year_val, email=email, phone=phone)
            db.session.add(s)
            db.session.commit()
            flash('Thêm hồ sơ sinh viên thành công!', 'success')
            return redirect(url_for('dashboard'))
            
        return render_template('student_form.html', action='Thêm')

    @app.route('/student/edit/<int:sid>', methods=['GET', 'POST'])
    @login_required
    def edit_student(sid):
        s = Student.query.get_or_404(sid)
        if request.method == 'POST':
            name = request.form.get('name','').strip()
            usn = request.form.get('usn','').strip()
            branch = request.form.get('branch','').strip()
            year_str = request.form.get('year','').strip()
            email = request.form.get('email','').strip()
            phone = request.form.get('phone','').strip()
            
            if not name or not usn:
                flash('Họ tên và Mã sinh viên là bắt buộc.', 'danger')
                return redirect(url_for('edit_student', sid=sid))
                
            if email and not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
                flash('Định dạng email không hợp lệ.', 'danger')
                return redirect(url_for('edit_student', sid=sid))

            # Check duplicate USN with another student
            duplicate = Student.query.filter(Student.usn == usn, Student.id != sid).first()
            if duplicate:
                flash('Mã sinh viên này đã được sử dụng bởi sinh viên khác.', 'danger')
                return redirect(url_for('edit_student', sid=sid))

            s.name = name
            s.usn = usn
            s.branch = branch
            if year_str:
                try:
                    s.year = int(year_str)
                except ValueError:
                    pass
            s.email = email
            s.phone = phone
            db.session.commit()
            flash('Cập nhật hồ sơ sinh viên thành công!', 'success')
            return redirect(url_for('dashboard'))
            
        return render_template('student_form.html', action='Sửa', student=s)

    @app.route('/student/delete/<int:sid>', methods=['POST'])
    @login_required
    def delete_student(sid):
        s = Student.query.get_or_404(sid)
        db.session.delete(s)
        db.session.commit()
        flash('Đã xóa hồ sơ sinh viên thành công!', 'success')
        return redirect(url_for('dashboard'))

    @app.route('/student/<int:sid>')
    @login_required
    def view_student(sid):
        s = Student.query.get_or_404(sid)
        return render_template('view_student.html', student=s)

    @app.route('/api/students')
    def api_students():
        students = Student.query.all()
        data = [{"id": s.id, "name": s.name, "usn": s.usn, "branch": s.branch, "year": s.year} for s in students]
        return jsonify(data)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
