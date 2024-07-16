import unittest
from app import app, db
from models import User, Feedback
from werkzeug.security import generate_password_hash

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_feedback'
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            # Create a test user
            user = User(username='testuser', 
                        password=generate_password_hash('password'), 
                        email='testuser@example.com', 
                        first_name='Test', 
                        last_name='User')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user(self):
        with app.app_context():
            response = self.client.post('/register', data=dict(
                username='testuser2',
                password='password2',
                email='testuser2@example.com',
                first_name='Test2',
                last_name='User2'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login', response.data)
            user = User.query.filter_by(username='testuser2').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'testuser2@example.com')

    def test_login_user(self):
        with app.app_context():
            # Test successful login
            response = self.client.post('/login', data=dict(
                username='testuser',
                password='password'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"testuser's Profile", response.data)

            # Test unsuccessful login
            response = self.client.post('/login', data=dict(
                username='testuser',
                password='wrongpassword'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Invalid username or password.', response.data)

    def test_user_profile(self):
        with app.app_context():
            self.client.post('/login', data=dict(
                username='testuser',
                password='password'
            ), follow_redirects=True)
            response = self.client.get('/users/testuser')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"testuser's Profile", response.data)

            response = self.client.get('/users/testuser2', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You are not authorized to view this page.', response.data)

    def test_delete_user(self):
        with app.app_context():
            self.client.post('/login', data=dict(
                username='testuser',
                password='password'
            ), follow_redirects=True)
            response = self.client.post('/users/testuser/delete', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'User deleted successfully.', response.data)
            user = User.query.filter_by(username='testuser').first()
            self.assertIsNone(user)

    def test_add_feedback(self):
        with app.app_context():
            self.client.post('/login', data=dict(
                username='testuser',
                password='password'
            ), follow_redirects=True)
            response = self.client.post('/users/testuser/feedback/add', data=dict(
                title='Test Feedback',
                content='This is a test feedback.'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Feedback added successfully!', response.data)
            feedback = Feedback.query.filter_by(username='testuser').first()
            self.assertIsNotNone(feedback)
            self.assertEqual(feedback.title, 'Test Feedback')

    def test_update_feedback(self):
        with app.app_context():
            feedback = Feedback(title='Old Title', content='Old Content', username='testuser')
            db.session.add(feedback)
            db.session.commit()

            self.client.post('/login', data=dict(
                username='testuser',
                password='password'
            ), follow_redirects=True)
            feedback = Feedback.query.filter_by(username='testuser').first()
            response = self.client.post(f'/feedback/{feedback.id}/update', data=dict(
                title='New Title',
                content='New Content'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Feedback updated successfully!', response.data)
            feedback = Feedback.query.filter_by(username='testuser').first()
            self.assertEqual(feedback.title, 'New Title')

    def test_delete_feedback(self):
        with app.app_context():
            feedback = Feedback(title='Title', content='Content', username='testuser')
            db.session.add(feedback)
            db.session.commit()

            self.client.post('/login', data=dict(
                username='testuser',
                password='password'
            ), follow_redirects=True)
            feedback = Feedback.query.filter_by(username='testuser').first()
            response = self.client.post(f'/feedback/{feedback.id}/delete', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Feedback deleted successfully!', response.data)
            feedback = Feedback.query.filter_by(username='testuser').first()
            self.assertIsNone(feedback)

    def test_logout(self):
        with app.app_context():
            self.client.post('/login', data=dict(
                username='testuser',
                password='password'
            ), follow_redirects=True)
            response = self.client.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You have been logged out.', response.data)

if __name__ == '__main__':
    unittest.main()
