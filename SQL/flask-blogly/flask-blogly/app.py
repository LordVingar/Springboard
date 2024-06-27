from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, connect_db, User, Post
from datetime import datetime
import humanize

def friendly_date(value):
    return humanize.naturaltime(value)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.secret_key = 'your_secret_key'  # Needed for flash messages

    connect_db(app)
    with app.app_context():
        db.create_all()

    # Register the custom filter
    app.jinja_env.filters['friendly_date'] = friendly_date

    @app.route('/')
    def homepage():
        """Show 5 most recent posts"""
        posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
        return render_template('homepage.html', posts=posts, humanize=humanize)
    
    @app.route('/users')
    def list_users():
        users = User.query.order_by(User.last_name, User.first_name).all()
        return render_template('users/list.html', users=users)

    @app.route('/users/new', methods=["GET", "POST"])
    def add_user():
        if request.method == "POST":
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            image_url = request.form['image_url']

            if not first_name or not last_name:
                flash("First name and last name are required.", "error")
                return redirect(url_for('add_user'))

            new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
            db.session.add(new_user)
            db.session.commit()

            flash("User added successfully!", "success")
            return redirect(url_for('list_users'))
        else:
            return render_template('users/new.html')

    @app.route('/users/<int:user_id>')
    def show_user(user_id):
        user = User.query.get_or_404(user_id)
        posts = Post.query.filter_by(user_id=user_id).all()
        return render_template('users/detail.html', user=user, posts=posts, humanize=humanize)

    @app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
    def edit_user(user_id):
        user = User.query.get_or_404(user_id)

        if request.method == "POST":
            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.image_url = request.form['image_url']

            db.session.commit()
            flash("User updated successfully!", "success")
            return redirect(url_for('show_user', user_id=user_id))
        else:
            return render_template('users/edit.html', user=user)

    @app.route('/users/<int:user_id>/delete', methods=["POST"])
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash("User and related posts deleted successfully!", "success")
        return redirect(url_for('list_users'))

    @app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])
    def add_post(user_id):
        if request.method == "POST":
            title = request.form['title']
            content = request.form['content']

            new_post = Post(title=title, content=content, user_id=user_id, created_at=datetime.utcnow())
            db.session.add(new_post)
            db.session.commit()

            flash("Post added successfully!", "success")
            return redirect(url_for('show_user', user_id=user_id))
        else:
            user = User.query.get_or_404(user_id)
            return render_template('posts/new.html', user=user)

    @app.route('/posts/<int:post_id>')
    def show_post(post_id):
        post = Post.query.get_or_404(post_id)
        user = User.query.get_or_404(post.user_id)
        return render_template('posts/detail.html', post=post, user=user, humanize=humanize)

    @app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
    def edit_post(post_id):
        post = Post.query.get_or_404(post_id)

        if request.method == "POST":
            post.title = request.form['title']
            post.content = request.form['content']

            db.session.commit()
            flash("Post updated successfully!", "success")
            return redirect(url_for('show_post', post_id=post_id))
        else:
            return render_template('posts/edit.html', post=post)

    @app.route('/posts/<int:post_id>/delete', methods=["POST"])
    def delete_post(post_id):
        post = Post.query.get_or_404(post_id)
        user_id = post.user_id
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully!", "success")
        return redirect(url_for('show_user', user_id=user_id))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
