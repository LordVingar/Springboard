import unittest
from sqlalchemy.sql import text
from app import create_app, db
from models import User, Post, Tag
from datetime import datetime

class BloglyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
        self.client = self.app.test_client()

        with self.app.app_context():
            self.pre_test_teardown()
            db.create_all()
            self.create_sample_data()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def pre_test_teardown(self):
        """Clean up any existing data before setting up the test environment."""
        db.session.remove()
        db.session.execute(text("DROP TABLE IF EXISTS post_tags CASCADE;"))
        db.session.execute(text("DROP TABLE IF EXISTS posts CASCADE;"))
        db.session.execute(text("DROP TABLE IF EXISTS tags CASCADE;"))
        db.session.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
        db.session.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE;"))
        db.session.commit()

    def create_sample_data(self):
        # Create a sample user
        user = User(first_name="Test", last_name="User", image_url="https://via.placeholder.com/150")
        db.session.add(user)
        db.session.commit()

        # Create a sample post
        post = Post(title="Test Post", content="This is a test post", user_id=user.id, created_at=datetime.utcnow())
        db.session.add(post)
        db.session.commit()

        # Create a sample tag
        tag = Tag(name="TestTag")
        db.session.add(tag)
        db.session.commit()

        # Associate the tag with the post
        post.tags.append(tag)
        db.session.commit()

        # Verify that the sample data was created
        print("Sample Data Created:")
        print("Users:", User.query.all())
        print("Posts:", Post.query.all())
        print("Tags:", Tag.query.all())

    def test_homepage(self):
        """Test homepage displays recent posts."""
        with self.client as c:
            resp = c.get("/")
            print("Homepage Response Data:", resp.data.decode())  # Debug print
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Test Post", resp.data)
            self.assertIn(b"By Test User on", resp.data)

    def test_add_user(self):
        """Test adding a user."""
        with self.client as c:
            data = {"first_name": "New", "last_name": "User", "image_url": "https://via.placeholder.com/150"}
            resp = c.post("/users/new", data=data, follow_redirects=True)
            print("Add User Response Data:", resp.data.decode())  # Debug print
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"New User", resp.data)

    def test_add_post(self):
        """Test adding a post."""
        with self.client as c:
            data = {"title": "New Post", "content": "New content"}
            resp = c.post(f"/users/1/posts/new", data=data, follow_redirects=True)
            print("Add Post Response Data:", resp.data.decode())  # Debug print
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"New Post", resp.data)

    def test_friendly_date(self):
        """Test friendly date display."""
        with self.client as c:
            resp = c.get("/")
            print("Friendly Date Response Data:", resp.data.decode())  # Debug print
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Test Post", resp.data)
            self.assertIn(b"By Test User on", resp.data)
            # Check for friendly date format
            self.assertIn(b"on", resp.data)

    def test_flash_messages(self):
        """Test flash messages."""
        with self.client as c:
            data = {"first_name": "", "last_name": "User", "image_url": "https://via.placeholder.com/150"}
            resp = c.post("/users/new", data=data, follow_redirects=True)
            print("Flash Messages Response Data:", resp.data.decode())  # Debug print
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"First name and last name are required.", resp.data)

    def test_custom_404(self):
        """Test custom 404 error page."""
        with self.client as c:
            resp = c.get("/nonexistent")
            print("Custom 404 Response Data:", resp.data.decode())  # Debug print
            self.assertEqual(resp.status_code, 404)
            self.assertIn(b"Sorry, this is not the page you're looking for.", resp.data)

    def test_cascade_delete(self):
        """Test cascading delete of user and their posts."""
        with self.client as c:
            # Delete the user
            resp = c.post("/users/1/delete", follow_redirects=True)
            print("Cascade Delete User Response Data:", resp.data.decode())  # Debug print
            self.assertEqual(resp.status_code, 200)
            # Ensure the user and posts are deleted
            self.assertNotIn(b"Test User", resp.data)
            post_resp = c.get("/posts/1")
            print("Cascade Delete Post Response Data:", post_resp.data.decode())  # Debug print
            self.assertEqual(post_resp.status_code, 404)

    def test_add_tag(self):
        """Test adding a tag."""
        with self.client as c:
            data = {"name": "NewTag"}
            resp = c.post("/tags/new", data=data, follow_redirects=True)
            print("Add Tag Response Data:", resp.data.decode())  # Debug print
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"NewTag", resp.data)

    def test_edit_tag(self):
        """Test editing a tag."""
        with self.client as c:
            data = {"name": "UpdatedTag"}
            resp = c.post(f"/tags/1/edit", data=data, follow_redirects=True)
            print("Edit Tag Response Data:", resp.data.decode())  # Debug print
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"UpdatedTag", resp.data)

if __name__ == "__main__":
    unittest.main()
