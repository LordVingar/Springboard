from flask import Flask, request, redirect, render_template, flash, abort
from models import db, connect_db, User, Post, Tag
import os
from datetime import datetime

def create_app():
    app = Flask(__name__)
    
    # Configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)

    # Initialize extensions
    connect_db(app)

    with app.app_context():
        # Create database tables if they do not exist
        db.create_all()


    @app.route('/')
    def homepage():
        posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
        return render_template('posts/homepage.html', posts=posts)

    @app.route('/users')
    def list_users():
        users = User.query.order_by(User.last_name, User.first_name).all()
        return render_template('users/index.html', users=users)

    @app.route('/users/new', methods=["GET", "POST"])
    def add_user():
        if request.method == "POST":
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            if not first_name or not last_name:
                flash("First name and last name are required.", "error")
            else:
                user = User(first_name=first_name, last_name=last_name)
                db.session.add(user)
                db.session.commit()
                flash("User added successfully!", "success")
                return redirect("/users")

        return render_template("users/new.html")

    @app.route('/users/<int:user_id>')
    def show_user(user_id):
        user = db.session.get(User, user_id)
        if not user:
            abort(404)
        posts = Post.query.filter_by(user_id=user_id).all()
        return render_template('users/show.html', user=user, posts=posts)

    @app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
    def edit_user(user_id):
        user = db.session.get(User, user_id)
        if not user:
            abort(404)

        if request.method == "POST":
            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.image_url = request.form['image_url']

            db.session.commit()
            flash("User updated successfully!", "success")
            return redirect(f'/users/{user_id}')
        else:
            return render_template('users/edit.html', user=user)

    @app.route('/users/<int:user_id>/delete', methods=["POST"])
    def delete_user(user_id):
        user = db.session.get(User, user_id)
        if not user:
            abort(404)
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully!", "success")
        return redirect("/")

    @app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])
    def add_post(user_id):
        user = db.session.get(User, user_id)
        if not user:
            abort(404)

        if request.method == "POST":
            title = request.form['title']
            content = request.form['content']
            created_at = datetime.utcnow()

            new_post = Post(title=title, content=content, user_id=user_id, created_at=created_at)
            db.session.add(new_post)
            db.session.commit()
            flash("Post added successfully!", "success")
            return redirect(f"/users/{user_id}")

        return render_template("posts/new.html", user=user)

    @app.route('/posts/<int:post_id>')
    def show_post(post_id):
        post = db.session.get(Post, post_id)
        if not post:
            abort(404)
        user = db.session.get(User, post.user_id)
        if not user:
            abort(404)
        return render_template('posts/show.html', post=post, user=user)

    @app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
    def edit_post(post_id):
        post = db.session.get(Post, post_id)
        if not post:
            abort(404)
        if request.method == "POST":
            post.title = request.form['title']
            post.content = request.form['content']
            tag_ids = request.form.getlist('tags')

            post.tags = []
            for tag_id in tag_ids:
                tag = db.session.get(Tag, tag_id)
                if tag:
                    post.tags.append(tag)

            db.session.commit()
            flash("Post updated successfully!", "success")
            return redirect(f'/posts/{post_id}')
        else:
            tags = Tag.query.all()
            return render_template('posts/edit.html', post=post, tags=tags)

    @app.route('/posts/<int:post_id>/delete', methods=["POST"])
    def delete_post(post_id):
        post = db.session.get(Post, post_id)
        if not post:
            abort(404)
        user_id = post.user_id
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully!", "success")
        return redirect(f'/users/{user_id}')

    @app.route('/tags')
    def show_tags():
        print("Request received at /tags")  # Debug print
        tags = Tag.query.all()
        print(f"Tags fetched: {tags}")  # Debug print
        return render_template('tags/index.html', tags=tags)

    
    @app.route('/tags/<int:tag_id>')
    def show_tag(tag_id):
        print(f"Request received at /tags/{tag_id}")  # Debug print
        tag = db.session.get(Tag, tag_id)
        if not tag:
            print(f"Tag with id {tag_id} not found")  # Debug print
            abort(404)
        print(f"Tag fetched: {tag}")  # Debug print
        return render_template('tags/show.html', tag=tag)


    @app.route('/tags/new', methods=["GET", "POST"])
    def add_tag():
        if request.method == "POST":
            print("POST request received at /tags/new")  # Debug print
            name = request.form['name']
            new_tag = Tag(name=name)
            db.session.add(new_tag)
            db.session.commit()
            flash("Tag added successfully!", "success")
            return redirect('/tags')
        else:
            print("GET request received at /tags/new")  # Debug print
            return render_template('tags/new.html')

    @app.route('/tags/<int:tag_id>/edit', methods=["GET", "POST"])
    def edit_tag(tag_id):
        print(f"Accessing /tags/{tag_id}/edit")  # Debug print
        tag = db.session.get(Tag, tag_id)
        if not tag:
            abort(404)

        if request.method == "POST":
            print(f"POST request received at /tags/{tag_id}/edit")  # Debug print
            tag.name = request.form['name']
            db.session.add(tag)
            db.session.commit()
            flash("Tag updated successfully!", "success")
            return redirect("/tags")
        else:
            print(f"GET request received at /tags/{tag_id}/edit")  # Debug print
            return render_template("tags/edit.html", tag=tag)

    @app.route('/tags/<int:tag_id>/delete', methods=["POST"])
    def delete_tag(tag_id):
        tag = db.session.get(Tag, tag_id)
        if not tag:
            abort(404)
        db.session.delete(tag)
        db.session.commit()
        flash("Tag deleted successfully!", "success")
        return redirect('/tags')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)