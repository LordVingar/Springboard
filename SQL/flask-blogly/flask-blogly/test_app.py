import unittest
from app import create_app, db
from models import User, Post
from datetime import datetime

class BloglyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self.create_sample_data()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def create_sample_data(self):
        user = User(first_name="Test", last_name="User", image_url="https://via.placeholder.com/150")
        db.session.add(user)
        db.session.commit()

        post = Post(title="Test Post", content="This is a test post", user_id=user.id, created_at=datetime.utcnow())
        db.session.add(post)
        db.session.commit()

    def test_homepage(self):
        """Test homepage displays recent posts."""
        with self.client as c:
            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Test Post", resp.data)

    def test_add_user(self):
        """Test adding a user."""
        with self.client as c:
            data = {"first_name": "New", "last_name": "User", "image_url": "https://via.placeholder.com/150"}
            resp = c.post("/users/new", data=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"New User", resp.data)

    def test_add_post(self):
        """Test adding a post."""
        with self.client as c:
            data = {"title": "New Post", "content": "New content"}
            resp = c.post(f"/users/1/posts/new", data=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"New Post", resp.data)

    def test_friendly_date(self):
        """Test friendly date display."""
        with self.client as c:
            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Test Post", resp.data)
            # Check for friendly date format
            self.assertIn(b"on", resp.data)

    def test_flash_messages(self):
        """Test flash messages."""
        with self.client as c:
            data = {"first_name": "", "last_name": "User", "image_url": "https://via.placeholder.com/150"}
            resp = c.post("/users/new", data=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"First name and last name are required.", resp.data)

    def test_custom_404(self):
        """Test custom 404 error page."""
        with self.client as c:
            resp = c.get("/nonexistent")
            self.assertEqual(resp.status_code, 404)
            self.assertIn(b"Page Not Found", resp.data)  # Adjust according to your 404 template

    def test_cascade_delete(self):
        """Test cascading delete of user and their posts."""
        with self.client as c:
            # Delete the user
            resp = c.post("/users/1/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            # Ensure the user and posts are deleted
            self.assertNotIn(b"Test User", resp.data)
            post_resp = c.get("/posts/1")
            self.assertEqual(post_resp.status_code, 404)

if __name__ == "__main__":
    unittest.main()
