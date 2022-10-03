from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for users"""

    def setUp(self):
        """Add sample user"""
        User.query.delete()

        user = User(first_name="Test_first", last_name="Test_last", image_url="http://test.com")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 302)
            # self.assertIn('Test_first Test_last', html)

    def test_user_detail(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1 class="name">{self.user.first_name} {self.user.last_name}</h1>', html)

    def test_redirect_home(self):
        with app.test_client() as client:
            resp = client.get('/', follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test_first Test_last', html) 

    def test_add_new_user(self):
        with app.test_client() as client:
            d = {"first_name": "first-2", "last_name": "last-2", "image_url": "http://test.com"}
            resp = client.post('/users/new', data = d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<li><a href="users/{self.user_id}">', html)

    

