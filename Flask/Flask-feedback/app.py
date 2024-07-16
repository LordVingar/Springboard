from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, FeedbackForm
from models import db, connect_db, User, Feedback

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def root():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data)
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User(username=username, password=password, email=email,
                        first_name=first_name, last_name=last_name)

        db.session.add(new_user)
        db.session.commit()

        session['username'] = new_user.username

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['username'] = user.username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('user_profile', username=user.username))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html', form=form)

@app.route('/users/<username>')
def user_profile(username):
    if 'username' not in session or session['username'] != username:
        flash('You are not authorized to view this page.', 'danger')
        return redirect(url_for('login'))

    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('root'))

    feedbacks = Feedback.query.filter_by(username=username).all()
    return render_template('user_profile.html', user=user, feedbacks=feedbacks)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if 'username' not in session or session['username'] != username:
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('login'))

    user = User.query.filter_by(username=username).first()
    if user:
        Feedback.query.filter_by(username=username).delete()
        db.session.delete(user)
        db.session.commit()
        session.pop('username', None)
        flash('User deleted successfully.', 'success')
    return redirect(url_for('root'))

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    if 'username' not in session or session['username'] != username:
        flash('You are not authorized to view this page.', 'danger')
        return redirect(url_for('login'))

    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Feedback added successfully!', 'success')
        return redirect(url_for('user_profile', username=username))

    return render_template('add_feedback.html', form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'username' not in session or session['username'] != feedback.username:
        flash('You are not authorized to view this page.', 'danger')
        return redirect(url_for('login'))

    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        flash('Feedback updated successfully!', 'success')
        return redirect(url_for('user_profile', username=feedback.username))

    return render_template('update_feedback.html', form=form, feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'username' not in session or session['username'] != feedback.username:
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('login'))

    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback deleted successfully!', 'success')
    return redirect(url_for('user_profile', username=feedback.username))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('root'))

if __name__ == '__main__':
    app.run(debug=True)