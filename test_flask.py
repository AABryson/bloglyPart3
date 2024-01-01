from unittest import TestCase
from flask import request
from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class userTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""

        User.query.delete()

        user = User(first_name="first", last_name="last", picture="url")
        db.session.add(user)
        db.session.commit()

        self.user = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_add_user(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a user', html)

    def test_submit_form(self):
        with app.test_client() as client:
            d = {"first_name": "first", "last_name": "last", "picture": "url"}
            resp = client.post("/submit_form", data=d)
           

            # self.assertEqual(resp.status_code, 200)
            self.assertEqual(request.form["first_nameß"], "first")
            

  
