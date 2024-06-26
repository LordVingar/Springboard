import unittest
from app import create_app
from models import db, User


class BloglyTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and sample data."""
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
        self.app.config['SQLALCHEMY_ECHO'] = False
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            user = User(first_name="Test", last_name="User", image_url="https://via.placeholder.com/150")
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_list_users(self):
        """Test listing users."""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Test User", resp.data)

    def test_show_user(self):
        """Test showing a user."""
        with self.client as c:
            resp = c.get("/users/1")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Test User", resp.data)

    def test_add_user(self):
        """Test adding a user."""
        with self.client as c:
            data = {"first_name": "New", "last_name": "User", "image_url": "https://via.placeholder.com/150"}
            resp = c.post("/users/new", data=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"New User", resp.data)

    def test_edit_user(self):
        """Test editing a user."""
        with self.client as c:
            data = {"first_name": "Updated", "last_name": "User", "image_url": "https://via.placeholder.com/150"}
            resp = c.post("/users/1/edit", data=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Updated User", resp.data)

if __name__ == "__main__":
    unittest.main()
