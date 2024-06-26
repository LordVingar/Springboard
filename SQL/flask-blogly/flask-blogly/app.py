"""Blogly application."""

from flask import Flask, render_template, redirect, url_for, request
from models import db, connect_db, User

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    connect_db(app)
    with app.app_context():
        db.create_all()

    @app.route('/')
    def root():
        return redirect('/users')

    @app.route('/users')
    def list_users():
        users = User.query.order_by(User.last_name, User.first_name).all()
        return render_template('list.html', users=users)

    @app.route('/users/new', methods=["GET", "POST"])
    def add_user():
        if request.method == "POST":
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            image_url = request.form['image_url']

            new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('list_users'))
        else:
            return render_template('new.html')

    @app.route('/users/<int:user_id>')
    def show_user(user_id):
        user = User.query.get_or_404(user_id)
        return render_template('detail.html', user=user)

    @app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
    def edit_user(user_id):
        user = User.query.get_or_404(user_id)

        if request.method == "POST":
            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.image_url = request.form['image_url']

            db.session.commit()
            return redirect(url_for('list_users'))
        else:
            return render_template('edit.html', user=user)

    @app.route('/users/<int:user_id>/delete', methods=["POST"])
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('list_users'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)